#pragma once

#include <cstring>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <vector>
#include "wadas_runtime/crypto.h"
#include "wadas_runtime/system_info.h"

namespace py = pybind11;

namespace wadas_runtime {

/**
 * @brief Loads the contents of a file into a vector of bytes.
 *
 * @param file_path The path to the file to be loaded.
 * @param data A reference to a vector where the file's contents will be stored.
 *             The vector will be resized to match the size of the file.
 * @return true if the file was successfully loaded, false otherwise.
 *
 * @note This function opens the file in binary mode and reads its entire content.
 *       If the file cannot be opened or read, the function returns false.
 */
bool load_file(std::string file_path, std::vector<uint8_t>& data) {
    std::ifstream file(file_path, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        return false;
    }

    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);

    data.resize(size);
    if (!file.read(reinterpret_cast<char*>(data.data()), size)) {
        return false;
    }

    return true;
}

/**
 * @brief Loads and compiles an OpenVINO model.
 *
 * This function reads an OpenVINO model from the specified XML and binary files,
 * optionally decrypts the model weights, and compiles the model for the specified
 * device using the provided configuration.
 *
 * @param model_xml_path The file path to the model's XML file.
 * @param model_bin_path The file path to the model's binary file.
 * @param device_name The target device name for model compilation (e.g., "CPU", "GPU").
 * @param config A map of configuration options for the OpenVINO runtime.
 * @return A compiled OpenVINO model object.
 *
 * @throws std::runtime_error If loading the XML or binary files fails, or if decryption fails.
 */
auto load_and_compile_model(std::string model_xml_path, std::string model_bin_path, std::string device_name,
                            const std::map<std::string, std::string>& config) {
    py::module_ ov = py::module_::import("openvino");

    py::object core = ov.attr("Core")();

    if (model_bin_path.empty()) {
        model_bin_path = model_xml_path.substr(0, model_xml_path.find_last_of('.')) + ".bin";
    }

    std::vector<uint8_t> bin_data, xml_data, decrypted_bin_data;
    if (!load_file(model_xml_path, xml_data)) {
        throw std::runtime_error("Failed to load model XML file: " + model_xml_path);
    }
    if (!load_file(model_bin_path, bin_data)) {
        throw std::runtime_error("Failed to load model binary file: " + model_bin_path);
    }

    // Check for encryption header
    const std::string encryption_header = "WADAS_ENCRYPTED";
    bool is_encrypted = bin_data.size() >= encryption_header.size() &&
                        std::equal(encryption_header.begin(), encryption_header.end(), bin_data.begin());

    py::bytes xml = py::bytes(reinterpret_cast<const char*>(xml_data.data()), xml_data.size());
    py::bytes weights;
    if (is_encrypted) {
        // Remove the header before decryption
        bin_data.erase(bin_data.begin(), bin_data.begin() + encryption_header.size());

        // Decrypt the weights using the provided function
        if (!decrypt_weights(bin_data, decrypted_bin_data)) {
            throw std::runtime_error("Failed to decrypt model weights.");
        }
        weights = py::bytes(reinterpret_cast<const char*>(decrypted_bin_data.data()), decrypted_bin_data.size());
    } else {
        weights = py::bytes(reinterpret_cast<const char*>(bin_data.data()), bin_data.size());
    }

    py::object model = core.attr("read_model")(xml, weights);

    // Compile the model
    py::object compiled_model = core.attr("compile_model")(model, device_name, config);
    return compiled_model;
}

}  // namespace wadas_runtime