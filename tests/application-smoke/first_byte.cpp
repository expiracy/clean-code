#include "first_byte.hpp"

#include <cstdio>
#include <memory>

ReadResult read_first_byte(const char* path) noexcept {
    if (!path) return ReadError::open_failed;
    using File = std::unique_ptr<std::FILE, decltype(&std::fclose)>;
    File file{std::fopen(path, "rb"), &std::fclose};
    if (!file) return ReadError::open_failed;
    const int byte = std::fgetc(file.get());
    if (byte == EOF) {
        return std::ferror(file.get()) ? ReadError::read_failed
                                      : ReadError::empty_file;
    }
    return static_cast<unsigned char>(byte);
}
