#pragma once

#include <pybind11/pybind11.h>
#include <stdexcept>
#include <string>
#include "nlohmann/json.hpp"

namespace wadas_runtime {

using json = nlohmann::json;

class RestClient {
public:
    RestClient() = default;

    ~RestClient() = default;

    /**
     * @brief Sends an HTTP GET request to the specified URL and parses the JSON response.
     *
     * This function performs an HTTP GET request.
     * If the response status code is not 200, it throws a std::runtime_error.
     * The response body is parsed as JSON and returned.
     *
     * @param url The URL to send the GET request to.
     * @return json The parsed JSON response from the server.
     * @throws std::runtime_error If the request fails or the response cannot be parsed as JSON.
     */
    static json get(const std::string& url) {
        auto requests = pybind11::module_::import("requests");
        pybind11::object response = requests.attr("get")(url);
        if (response.attr("status_code").cast<int>() != 200) {
            throw std::runtime_error("GET request failed with status code: " +
                                     std::to_string(response.attr("status_code").cast<int>()));
        }
        json resp_json;
        try {
            resp_json = json::parse(response.attr("text").cast<std::string>());
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Failed to parse server response: ") + e.what());
        }
        return resp_json;
    }

    /**
     * @brief Sends a POST request to the specified URL with the given JSON data.
     *
     * This static method serializes the provided JSON object and sends it as the body of a POST request
     * to the specified URL. The response is expected to be in JSON format and is returned as a json object.
     *
     * @param url The destination URL for the POST request.
     * @param data The JSON object to be sent in the request body.
     * @return json The JSON response received from the server.
     */
    static json post(const std::string& url, const json& data) {
        return post(url, data.dump());
    }

    /**
     * @brief Sends a POST request to the specified URL with the given data using Python's requests library.
     *
     * This function performs a POST request, sending the provided data to the specified URL.
     * It expects a JSON response and parses it into a json object. If the HTTP status code is not 200, or if the
     * response cannot be parsed as JSON, it throws a std::runtime_error with an appropriate error message.
     *
     * @param url The URL to which the POST request will be sent.
     * @param data The data to include in the POST request body.
     * @return json The parsed JSON response from the server.
     * @throws std::runtime_error If the HTTP status code is not 200 or if the response cannot be parsed as JSON.
     */
    static json post(const std::string& url, const std::string& data) {
        auto requests = pybind11::module_::import("requests");
        pybind11::object response = requests.attr("post")(url, pybind11::arg("data") = data);
        if (response.attr("status_code").cast<int>() != 200) {
            throw std::runtime_error("POST request failed with status code: " +
                                     std::to_string(response.attr("status_code").cast<int>()));
        }
        json resp_json;
        try {
            resp_json = json::parse(response.attr("text").cast<std::string>());
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Failed to parse server response: ") + e.what());
        }
        return resp_json;
    }

    /**
     * @brief Retrieves the HTTP status code from a GET request to the specified URL.
     *
     * This static function performs an HTTP GET request to the provided URL
     * and returns the resulting status code.
     *
     * @param url The URL to which the GET request will be sent.
     * @return int The HTTP status code returned by the server.
     *
     * @throws pybind11::error_already_set if the Python 'requests' module is not available
     *         or if the request fails.
     */
    static int get_status_code(const std::string& url) {
        auto requests = pybind11::module_::import("requests");
        pybind11::object response = requests.attr("get")(url);
        return response.attr("status_code").cast<int>();
    }

    /**
     * @brief Downloads a file from the specified URL and saves it to the given file path.
     *
     * This function performs an HTTP GET request to the provided URL,
     * streaming the response content and writing it to the specified file path.
     *
     * @param url The URL from which to download the file.
     * @param file_path The local file path where the downloaded content will be saved.
     * @return int The HTTP status code of the GET request.
     * @throws std::runtime_error If the GET request fails or returns a non-200 status code.
     *
     * @note Requires Python and the 'requests' library to be available in the environment.
     */
    static int download(const std::string& url, const std::string& file_path) {
        auto requests = pybind11::module_::import("requests");
        pybind11::object response = requests.attr("get")(url, pybind11::arg("stream") = true);
        int status_code = response.attr("status_code").cast<int>();
        if (status_code != 200) {
            throw std::runtime_error("GET request failed with status code: " +
                                     std::to_string(response.attr("status_code").cast<int>()));
        }
        response.attr("raise_for_status")();
        pybind11::object file = pybind11::module_::import("builtins").attr("open")(file_path, "wb");
        pybind11::object content = response.attr("iter_content")(1024);
        for (const auto& chunk : content) {
            file.attr("write")(chunk);
        }
        file.attr("close")();

        return status_code;
    }
};

}  // namespace wadas_runtime
