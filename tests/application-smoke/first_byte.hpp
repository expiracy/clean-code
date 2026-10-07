#pragma once

#include <variant>

enum class ReadError { open_failed, empty_file, read_failed };
using ReadResult = std::variant<unsigned char, ReadError>;

// The path is borrowed for the call; a null path returns open_failed.
ReadResult read_first_byte(const char* path) noexcept;
