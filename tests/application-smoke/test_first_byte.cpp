#include "first_byte.hpp"

#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <system_error>

void require(bool condition, const char* message) {
    if (!condition) {
        std::fprintf(stderr, "FAIL: %s\n", message);
        std::exit(EXIT_FAILURE);
    }
}

void require_error(const ReadResult& result, ReadError expected,
                   const char* message) {
    const auto* error = std::get_if<ReadError>(&result);
    require(error && *error == expected, message);
}

void require_byte(const ReadResult& result, unsigned char expected,
                  const char* message) {
    const auto* byte = std::get_if<unsigned char>(&result);
    require(byte && *byte == expected, message);
}

void write_fixture(const char* path, unsigned char first_byte) {
    auto* file = std::fopen(path, "wb");
    require(file != nullptr, "the binary fixture must open");
    const unsigned char bytes[]{first_byte, 0x42};
    require(std::fwrite(bytes, 1, sizeof bytes, file) == sizeof bytes,
            "the binary fixture must write");
    require(std::fclose(file) == 0, "the binary fixture must close");
}

std::size_t open_descriptor_count() {
    std::error_code error;
    auto iterator = std::filesystem::directory_iterator{"/dev/fd", error};
    require(!error, "descriptor enumeration must start");
    const std::filesystem::directory_iterator end;
    std::size_t count = 0;
    for (; iterator != end; iterator.increment(error)) {
        require(!error, "descriptor enumeration must continue");
        ++count;
    }
    require(!error, "descriptor enumeration must finish");
    return count;
}

int main() {
    const char* missing_path = "first-byte-definitely-missing.bin";
    std::remove(missing_path);
    require_error(read_first_byte(missing_path), ReadError::open_failed,
                  "a missing path must report open_failed");
    require_error(read_first_byte(nullptr), ReadError::open_failed,
                  "a null path must report open_failed");
    require_error(read_first_byte(""), ReadError::open_failed,
                  "an empty path must report open_failed");

    const char* empty_path = "first-byte-empty.bin";
    auto* empty = std::fopen(empty_path, "wb");
    require(empty != nullptr, "the empty fixture must open");
    require(std::fclose(empty) == 0, "the empty fixture must close");
    require_error(read_first_byte(empty_path), ReadError::empty_file,
                  "an empty file must report empty_file");
    require_error(read_first_byte("."), ReadError::read_failed,
                  "reading a directory must report read_failed on this host");

    const char* binary_path = "first-byte-binary.bin";
    write_fixture(binary_path, 0x2a);
    require_byte(read_first_byte(binary_path), 0x2a,
                 "only the first binary byte must be returned");
    write_fixture(binary_path, 0x00);
    require_byte(read_first_byte(binary_path), 0x00,
                 "zero must be a successful byte");
    write_fixture(binary_path, 0xff);
    require_byte(read_first_byte(binary_path), 0xff,
                 "0xff must not be confused with EOF");

    const auto descriptors_before = open_descriptor_count();
    for (int i = 0; i < 64; ++i) {
        require_byte(read_first_byte(binary_path), 0xff,
                     "success must survive repeated calls");
        require_error(read_first_byte(empty_path), ReadError::empty_file,
                      "empty-file failure must survive repeated calls");
        require_error(read_first_byte("."), ReadError::read_failed,
                      "read failure must survive repeated calls");
    }
    const auto descriptors_after = open_descriptor_count();
    require(descriptors_before == descriptors_after,
            "successful and failed reads must not leak descriptors");

    require(std::remove(empty_path) == 0, "the empty fixture must be removed");
    require(std::remove(binary_path) == 0, "the binary fixture must be removed");
    std::printf("PASS: 8 cases; descriptors %zu -> %zu after 192 opened reads\n",
                descriptors_before, descriptors_after);
}
