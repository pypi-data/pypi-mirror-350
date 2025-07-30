#pragma once

#include <openssl/sha.h>
#include <pybind11/pybind11.h>
#include <iomanip>
#include <sstream>
#include <string>

namespace wadas_runtime {

/**
 * @brief Retrieves a unique hardware fingerprint for the current system.
 *
 * This function generates a string that uniquely identifies the hardware
 * of the system it is executed on. The fingerprint can be used for purposes
 * such as licensing, authentication, or system identification.
 *
 * @return A std::string containing the hardware fingerprint.
 */
std::string get_hardware_fingerprint() {
    pybind11::module_ hwid = pybind11::module_::import("hwid");
    std::string hwid_value = hwid.attr("get_hwid")().cast<std::string>();

    // Hash the HWID using SHA256
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(hwid_value.c_str()), hwid_value.size(), hash);

    // Convert the hash to a hexadecimal string
    std::ostringstream oss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        oss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(hash[i]);
    }

    return oss.str();
}
}  // namespace wadas_runtime
