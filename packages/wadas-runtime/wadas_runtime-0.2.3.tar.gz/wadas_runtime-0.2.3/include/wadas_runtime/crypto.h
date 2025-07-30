#pragma once

#include <openssl/evp.h>
#include <openssl/rand.h>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "wadas_runtime/system_info.h"

namespace wadas_runtime {

#define ENCRYPTION_HEADER "WADAS_ENCRYPTED"

/**
 * @brief Derives a 256-bit AES key from the hardware fingerprint using PBKDF2.
 *
 * This function generates a cryptographic key by combining a hardware fingerprint
 * with a salt using the PBKDF2 (Password-Based Key Derivation Function 2) algorithm.
 * The derived key can be used for encryption or other cryptographic purposes.
 *
 * @param salt A string used as the salt for the key derivation process.
 *             Defaults to "static-salt" if not provided.
 * @return A vector of 32 bytes representing the derived 256-bit AES key.
 *
 * @note The function uses 100,000 iterations of PBKDF2 with HMAC-SHA256 as the
 *       underlying pseudorandom function.
 * @note The hardware fingerprint is obtained using the `get_hardware_fingerprint()` function.
 */
std::vector<uint8_t> derive_key_from_hw_fingerprint(const std::string& salt = "static-salt") {
    std::vector<uint8_t> key(32);                   // 256-bit AES key
    auto fingerprint = get_hardware_fingerprint();  // Get the hardware fingerprint

    PKCS5_PBKDF2_HMAC(fingerprint.c_str(), static_cast<int>(fingerprint.size()),
                      reinterpret_cast<const unsigned char*>(salt.c_str()), static_cast<int>(salt.size()), 100000,
                      EVP_sha256(), static_cast<int>(key.size()), key.data());

    return key;
}

/**
 * @brief Decrypts encrypted weights using AES-256-GCM with a hardware-derived key.
 *
 * This function decrypts the provided encrypted data using AES-256-GCM. The decryption
 * key is derived from the hardware fingerprint. If no key is available, the function
 * returns the original data without decryption.
 *
 * @param[in] encrypted A vector containing the encrypted data. The first 12 bytes
 *                      are expected to be the nonce, the last 16 bytes are the
 *                      authentication tag, and the remaining bytes are the ciphertext.
 * @param[out] decrypted A vector to store the decrypted data. It will be resized
 *                       to match the length of the plaintext.
 * @return true if decryption is successful or no key is provided (data is returned as-is),
 *         false otherwise.
 * @throws std::runtime_error if decryption fails due to an error or tag mismatch.
 *
 * @note The function uses OpenSSL's EVP API for AES-256-GCM decryption. Ensure that
 *       the OpenSSL library is properly initialized and available in your project.
 */
bool decrypt_weights(std::vector<uint8_t>& encrypted, std::vector<uint8_t>& decrypted) {
    auto key = derive_key_from_hw_fingerprint();  // Get the hardware fingerprint

    if (key.empty()) {
        decrypted = encrypted;  // No key provided, return the original data
        return true;            // No key provided, do not decrypt
    }
    std::vector<uint8_t> nonce(encrypted.begin(), encrypted.begin() + 12);
    const size_t tag_offset = encrypted.size() - 16;
    const size_t cipher_len = encrypted.size() - 12 - 16;

    const uint8_t* ciphertext = encrypted.data() + 12;
    const uint8_t* tag = encrypted.data() + tag_offset;

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        throw std::runtime_error("Failed to create EVP_CIPHER_CTX");
    }
    decrypted.resize(cipher_len);

    int len = 0, decrypted_len = 0;

    EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), nullptr, nullptr, nullptr);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, static_cast<int>(nonce.size()), nullptr);
    EVP_DecryptInit_ex(ctx, nullptr, nullptr, key.data(), nonce.data());

    EVP_DecryptUpdate(ctx, decrypted.data(), &len, ciphertext, static_cast<int>(cipher_len));
    decrypted_len = len;

    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, 16, const_cast<uint8_t*>(tag));

    int ret = EVP_DecryptFinal_ex(ctx, decrypted.data() + len, &len);
    EVP_CIPHER_CTX_free(ctx);

    if (ret > 0) {
        decrypted_len += len;
        decrypted.resize(decrypted_len);
        return true;  // Decryption successful
    } else {
        throw std::runtime_error("Decryption failed or tag mismatch");
    }
}

}  // namespace wadas_runtime