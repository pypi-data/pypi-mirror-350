#pragma once

#include "wadas_runtime/rest.h"
#include "wadas_runtime/system_info.h"

namespace wadas_runtime {

class ModelInfo {
public:
    std::string name;
    std::string released_at;
    std::string expires_on;
    std::string type;
    std::string path;
    bool is_default;

    /**
     * @brief Constructs a ModelInfo object from a JSON representation.
     *
     * Initializes the ModelInfo fields using values from the provided JSON object.
     * Fields not present are initialized with default values.
     *
     * @param model_json The JSON object containing model information.
     */
    ModelInfo(const json& model_json) {
        name = model_json.value("name", "");
        released_at = model_json.value("released_at", "");
        expires_on = model_json.value("expiration_dt", "");
        type = model_json.value("type", "");
        path = model_json.value("path", "");
        is_default = model_json.value("is_default", false);
    }

    /**
     * @brief Converts the model information to a Python dictionary.
     *
     * This method returns a Python dictionary containing:
     * - "name": The name of the model
     * - "released_at": The release date of the model
     * - "expires_on": The expiration date of the model
     * - "type": Type of the model (classification vs detection)
     * - "path": Path of the model within WADAS sub-folder tree
     * - "is_default": True if this model is the default one for its type
     *
     * @return py::dict Python dictionary with the model's metadata.
     */
    py::dict to_dict() const {
        py::dict model_dict;
        model_dict["name"] = name;
        model_dict["released_at"] = released_at;
        model_dict["expires_on"] = expires_on;
        model_dict["type"] = type;
        model_dict["path"] = path;
        model_dict["is_default"] = is_default;
        return model_dict;
    }
};

class WadasModelServer {
private:
    std::string server_url;

    /**
     * @brief Uploads the hardware fingerprint (HWID) to the server for a given organization.
     *
     * This function sends the local hardware fingerprint along with an optional salt to the server,
     * registering or updating the node for the specified organization code. It validates the server's
     * response to ensure the HWID matches, the node is enabled, and not banned.
     *
     * @param org_code The organization code to which the HWID should be uploaded.
     * @param salt Optional salt value to include with the HWID (default is an empty string).
     * @return std::string The ID of the registered node as returned by the server.
     *
     * @throws std::runtime_error If the HWID is missing or mismatched, the node is not enabled,
     *         or the node is banned (including ban reason and timestamp).
     */
    std::string upload_hwid(const std::string org_code, const std::string salt = "") {
        std::string url = server_url + "/orgs/" + org_code + "/nodes";
        json data = {
                {"hwid", get_hardware_fingerprint()},
                {"salt", salt},
        };
        json response = RestClient::post(url, data.dump());

        int id = response.value("id", 0);
        std::string hwid = response.value("hwid", "");
        if (hwid.empty()) {
            throw std::runtime_error("Failed to get HWID from server");
        }
        if (hwid != get_hardware_fingerprint()) {
            throw std::runtime_error("HWID mismatch!");
        }
        bool enabled = response.value("enabled", false);
        if (!enabled) {
            throw std::runtime_error("User is not enabled!");
        }
        if (response.value("is_banned", false)) {
            std::string banned_at = response.value("banned_at", "");
            std::string ban_reason = response.value("ban_reason", "");
            throw std::runtime_error("User is banned! Reason: " + ban_reason + " at " + banned_at);
        }
        return std::to_string(id);
    }

public:
    /**
     * @brief Constructs a WadasModelServer object with the specified server URL and API version.
     *
     * This constructor initializes the server URL for the Wadas model server. If the provided URL ends with a '/',
     * it is removed to ensure proper formatting. The API version is appended to the URL in the form "/api/{version}".
     *
     * @param url The base URL of the Wadas model server.
     * @param version The API version to use (default is "v1").
     */
    WadasModelServer(const std::string url, const std::string version = "v1") {
        server_url = url;
        if (server_url.back() == '/') {
            server_url.pop_back();
        }
        server_url += "/api/" + version;
    }

    ~WadasModelServer() = default;

    /**
     * @brief Authenticates a node with the given username and password.
     *
     * Sends a POST request to the server's "/organizations_login" endpoint with the provided
     * credentials. If authentication is successful, returns the organization code associated
     * with the node.
     *
     * @param username The username of the node attempting to log in.
     * @param password The password of the node.
     * @return std::string The organization code returned by the server upon successful login.
     * @throws std::exception If the server response does not contain "org_code" or if the request fails.
     */
    std::string login(const std::string& username, const std::string& password) {
        std::string url = server_url + "/organizations_login";
        json data = {
                {"username", username},
                {"password", password},
        };
        json response = RestClient::post(url, data.dump());
        return response["org_code"].get<std::string>();
    }

    /**
     * @brief Registers a node with the given username and password.
     *
     * This function attempts to log in with the provided credentials. If the login is successful,
     * it uploads the hardware ID (HWID) associated with the organization code obtained from the login.
     * The function returns the node ID if registration is successful, or an empty string otherwise.
     *
     * @param org_code The organization code of the node to register.
     * @return std::string The node ID if registration is successful, or an empty string on failure.
     */
    std::string register_node(const std::string& org_code) {
        if (org_code.empty()) {
            return "";
        }
        std::string node_id = upload_hwid(org_code);
        return node_id;
    }

    /**
     * @brief Checks if the server is ready.
     *
     * Sends a GET request to the server's "/server_status" endpoint and parses the response.
     * Returns true if the server status is "READY", otherwise returns false.
     *
     * @return true if the server status is "READY", false otherwise.
     */
    bool status() {
        std::string url = server_url + "/server_status";
        json response = RestClient::get(url);
        std::string status = response.value("status", "");
        return status == "READY";
    }

    /**
     * @brief Retrieves a list of models associated with a specific node.
     *
     * This function sends a GET request to the server to fetch all models
     * registered under the given node ID. The server response is expected
     * to be a JSON array, where each element contains information about a model.
     *
     * @param node_id The unique identifier of the node whose models are to be listed.
     * @return std::vector<ModelInfo> A vector containing information about each model.
     */
    std::vector<ModelInfo> list_models(const std::string& node_id) {
        std::string url = server_url + "/nodes/" + node_id + "/models";
        json response = RestClient::get(url);
        std::vector<ModelInfo> models;
        for (const auto& model_json : response) {
            models.emplace_back(model_json);
        }
        return models;
    }

    /**
     * @brief Downloads a model from the server for a specific node.
     *
     * Constructs a URL using the provided node ID and model name, then attempts to download
     * the model file from the server to the specified local path. Throws a std::runtime_error
     * if the download fails (i.e., the HTTP status code is not 200).
     *
     * @param node_id The unique identifier of the node requesting the model.
     * @param model_name The name of the model to download.
     * @param model_path The local filesystem path where the downloaded model will be saved.
     * @return true if the model is downloaded successfully.
     * @throws std::runtime_error if the download fails.
     */
    bool download_model(const std::string& node_id, const std::string& model_name, const std::string& model_path) {
        std::string url = server_url + "/nodes/" + node_id + "/models?model_name=" + model_name;
        int status_code = RestClient::download(url, model_path);
        if (status_code != 200) {
            throw std::runtime_error("Failed to download model: " + std::to_string(status_code));
        }
        return true;
    }
};
}  // namespace wadas_runtime