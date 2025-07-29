//==============================================================================
// Copyright 2025 Vajra Team; Georgia Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//==============================================================================
#pragma once
//==============================================================================
#include <nlohmann/json.hpp>
//==============================================================================
#include "commons/BoostCommon.h"
#include "commons/Constants.h"
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
template <typename T>
concept Printable = requires(const T& t) {
  { t.ToString() } -> std::convertible_to<std::string>;
};  // NOLINT(readability/braces)
//==============================================================================
template <typename T>
struct IsPrintable : std::false_type {};
//==============================================================================
template <Printable T>
struct IsPrintable<T> : std::true_type {};
//==============================================================================
template <typename T>
inline constexpr bool is_printable_v = IsPrintable<T>::value;
//==============================================================================
}  // namespace vajra
//==============================================================================
namespace std {
//==============================================================================
// Formatter for c10::ArrayRef<T> (for printing tensor sizes)
//==============================================================================
template <typename T>
struct formatter<c10::ArrayRef<T>, char> {
  // For simplicity, no custom parse options.
  // The parse method is called to parse format specifiers (e.g., alignment,
  // width) For this example, we don't support any custom format specifiers for
  // ArrayRef. It just needs to find the closing '}'.
  constexpr auto parse(std::format_parse_context& ctx) {
    auto it = ctx.begin();
    auto end = ctx.end();
    if (it != end && *it != '}') {
      // You could add parsing for custom options here if needed
      // For now, just advance to the closing brace or end
      while (it != end && *it != '}') {
        ++it;
      }
    }
    return it;
  }

  // The format method does the actual formatting
  template <typename FormatContext>
  auto format(const c10::ArrayRef<T>& arr_ref, FormatContext& ctx) const {
    auto out = ctx.out();
    out = std::format_to(out, "[");
    if (!arr_ref.empty()) {
      // This relies on T being formattable by std::format
      out = std::format_to(out, "{}", arr_ref[0]);
      for (size_t i = 1; i < arr_ref.size(); ++i) {
        out = std::format_to(out, ", {}", arr_ref[i]);
      }
    }
    out = std::format_to(out, "]");
    return out;
  }
};
//==============================================================================
// Formatter for c10::ScalarType (for printing dtype)
//==============================================================================
template <>
struct formatter<c10::ScalarType, char> {
  // No custom parse options for dtype
  constexpr auto parse(std::format_parse_context& ctx) {
    auto it = ctx.begin(), end = ctx.end();
    if (it != end && *it != '}') {
      // If you wanted to allow specifiers, parse them here.
      // For now, just expect it to be empty or find '}'.
      while (it != end && *it != '}') ++it;
    }
    return it;
  }

  template <typename FormatContext>
  auto format(const c10::ScalarType& dtype, FormatContext& ctx) const {
    // c10::toString(dtype) returns a const char* like "Float" or "Long"
    // To get "torch.float32", we might need a small mapping or use it as is.
    // For now, let's prepend "torch." to the output of c10::toString
    // Note: c10::toString gives "Float", "Double", "Long", etc.
    // PyTorch Python API shows "torch.float32", "torch.int64"
    // We can create a small helper or live with the C++ style names.

    // Let's try to map to Python-like names:
    std::string_view s;
    switch (dtype) {
      case c10::ScalarType::Byte:
        s = "torch.uint8";
        break;
      case c10::ScalarType::Char:
        s = "torch.int8";
        break;
      case c10::ScalarType::Short:
        s = "torch.int16";
        break;
      case c10::ScalarType::Int:
        s = "torch.int32";
        break;
      case c10::ScalarType::Long:
        s = "torch.int64";
        break;
      case c10::ScalarType::Half:
        s = "torch.float16";
        break;
      case c10::ScalarType::Float:
        s = "torch.float32";
        break;
      case c10::ScalarType::Double:
        s = "torch.float64";
        break;
      case c10::ScalarType::ComplexHalf:
        s = "torch.complex32";
        break;
      case c10::ScalarType::ComplexFloat:
        s = "torch.complex64";
        break;
      case c10::ScalarType::ComplexDouble:
        s = "torch.complex128";
        break;
      case c10::ScalarType::Bool:
        s = "torch.bool";
        break;
      case c10::ScalarType::QInt8:
        s = "torch.qint8";
        break;
      case c10::ScalarType::QUInt8:
        s = "torch.quint8";
        break;
      case c10::ScalarType::QInt32:
        s = "torch.qint32";
        break;
      case c10::ScalarType::BFloat16:
        s = "torch.bfloat16";
        break;
      // c10::ScalarType::QUInt4x2, c10::ScalarType::QUInt2x4 might not have
      // direct torch. counterparts or are newer
      default:
        s = c10::toString(dtype);  // Fallback
    }
    return std::format_to(ctx.out(), "{}", s);
  }
};
//==============================================================================
// Formatter for at::Tensor (for printing tensor values)
//==============================================================================
template <>
struct formatter<torch::Tensor, char> : formatter<std::string_view, char> {
 public:
  template <typename ParseContext>
  constexpr auto parse(ParseContext& ctx) {
    return formatter<std::string_view, char>::parse(ctx);
  }

  template <typename FormatContext>
  auto format(const torch::Tensor& tensor, FormatContext& ctx) const {
    std::string tensor_representation;

    std::ostringstream oss;
    if (!tensor.defined()) {
      oss << "[ Tensor (undefined) ]";
    } else {
      oss << tensor;
    }
    tensor_representation = oss.str();

    return formatter<std::string_view, char>::format(tensor_representation,
                                                     ctx);
  }
};
//==============================================================================
// Formatter for nlohmann::json
//==============================================================================
template <>
struct formatter<nlohmann::json, char> {
 private:
  int indent_ = -1;  // -1 for compact, >= 0 for pretty print indent level
  bool pretty_print_ = false;  // Flag to trigger pretty printing

 public:
  // Parses format specifiers like {} (compact), {:p} (pretty default), {:4}
  // (pretty indent 4)
  constexpr auto parse(std::format_parse_context& ctx) {
    auto it = ctx.begin();
    const auto end = ctx.end();

    if (it != end && *it == ':') {
      ++it;  // Consume ':'

      if (it != end && *it == 'p') {
        pretty_print_ = true;
        indent_ = 4;  // Default indent
        ++it;
      }

      if (it != end && std::isdigit(static_cast<unsigned char>(*it))) {
        int parsed_val = 0;
        bool num_found = false;
        while (it != end && std::isdigit(static_cast<unsigned char>(*it))) {
          // Check for overflow before multiplying and adding
          if (parsed_val >
              (std::numeric_limits<int>::max() - (*it - '0')) / 10) {
            // Handle overflow - perhaps throw, or cap.
            // For simplicity here, let's assume it won't overflow reasonable
            // indents. Or, more robustly:
            throw std::format_error(
                "JSON indent value too large, causes overflow.");
          }
          parsed_val = parsed_val * 10 + (*it - '0');
          ++it;
          num_found = true;
        }

        if (num_found) {
          if (parsed_val <
              0) {  // Should not happen with isdigit check, but good for safety
            throw std::format_error("JSON indent value must be non-negative.");
          }
          indent_ = parsed_val;
          pretty_print_ =
              true;  // If an indent is specified, assume pretty printing
        } else if (pretty_print_ && indent_ == 4 && (it != end && *it != '}')) {
          // This case means 'p' was seen, but no number followed it, and it's
          // not the end. It implies an invalid specifier if something other
          // than '}' is next. If 'p' was the only thing, indent_ is already 4.
        }
      }
    }

    if (it != end && *it != '}') {
      throw std::format_error("Invalid format specifier for nlohmann::json.");
    }
    return it;
  }

  // Formats the nlohmann::json object
  template <typename FormatContext>
  auto format(const nlohmann::json& j, FormatContext& ctx) const {
    if (pretty_print_) {
      return std::format_to(ctx.out(), "{}", j.dump(indent_));
    } else {
      return std::format_to(ctx.out(), "{}", j.dump());  // Compact output
    }
  }
};
//==============================================================================
// Formatter for boost::concurrent::sync_queue<T>
// (Handles vajra::Queue<T>)
//==============================================================================
template <typename T>
struct formatter<boost::concurrent::sync_queue<T>, char> {
  // No custom parsing options for sync_queue
  constexpr auto parse(std::format_parse_context& ctx) {
    auto it = ctx.begin(), end = ctx.end();
    if (it != end && *it != '}') {
      // Consume any characters until '}' or end, if any are present.
      // This basic formatter doesn't interpret them.
      while (it != end && *it != '}') {
        ++it;
      }
    }
    return it;
  }

  template <typename FormatContext>
  auto format(const boost::concurrent::sync_queue<T>& q,
              FormatContext& ctx) const {
    // Note: Getting a user-friendly string for type T is non-trivial without
    // RTTI/external libs. The "T" in "Queue<T>" is symbolic here.
    return std::format_to(ctx.out(), "vajra::Queue<T>(status: {}, size: {})",
                          q.closed() ? "closed" : "open",
                          q.size());  // .size() and .closed() are const
  }
};
//==============================================================================
// Formatter for boost::concurrent::sync_priority_queue<Value, Container,
// Compare> (Handles vajra::PriorityQueue<...>)
//==============================================================================
template <typename Value, typename Container, typename Compare>
struct formatter<
    boost::concurrent::sync_priority_queue<Value, Container, Compare>, char> {
  // No custom parsing options for sync_priority_queue
  constexpr auto parse(std::format_parse_context& ctx) {
    auto it = ctx.begin(), end = ctx.end();
    if (it != end && *it != '}') {
      while (it != end && *it != '}') {
        ++it;
      }
    }
    return it;
  }

  template <typename FormatContext>
  auto format(const boost::concurrent::sync_priority_queue<Value, Container,
                                                           Compare>& q,
              FormatContext& ctx) const {
    // Similar to sync_queue, "Value,..." is symbolic.
    return std::format_to(
        ctx.out(), "vajra::PriorityQueue<Value,...>(status: {}, size: {})",
        q.closed() ? "closed" : "open",
        q.size());  // .size() and .closed() are const
  }
};
//==============================================================================
// formatter specialization for Printable types
//==============================================================================
template <vajra::Printable T>
struct formatter<T> : formatter<string> {
  auto format(const T& obj, format_context& ctx) const {
    return formatter<string>::format(obj.ToString(), ctx);
  }
};
//==============================================================================
// formatter specialization for shared_ptr of Printable types
//==============================================================================
template <vajra::Printable T>
struct formatter<shared_ptr<T>> : formatter<string> {
  auto format(const shared_ptr<T>& ptr, format_context& ctx) const {
    if (ptr) {
      return formatter<string>::format(ptr->ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
// formatter specialization for shared_ptr<const T> of Printable types
//==============================================================================
template <vajra::Printable T>
struct formatter<shared_ptr<const T>> : formatter<string> {
  auto format(const shared_ptr<const T>& ptr, format_context& ctx) const {
    if (ptr) {
      return formatter<string>::format(ptr->ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
// formatter specialization for unique_ptr of Printable types
//==============================================================================
template <vajra::Printable T>
struct formatter<unique_ptr<T>> : formatter<string> {
  auto format(const unique_ptr<T>& ptr, format_context& ctx) const {
    if (ptr) {
      return formatter<string>::format(ptr->ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
// formatter specialization for unique_ptr<const T> of Printable types
//==============================================================================
template <vajra::Printable T>
struct formatter<unique_ptr<const T>> : formatter<string> {
  auto format(const unique_ptr<const T>& ptr, format_context& ctx) const {
    if (ptr) {
      return formatter<string>::format(ptr->ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
// formatter specialization for raw pointers of Printable types
// (use smart pointers when possible)
//==============================================================================
template <vajra::Printable T>
struct formatter<T*> : formatter<string> {
  auto format(T* ptr, format_context& ctx) const {
    if (ptr) {
      return formatter<string>::format(ptr->ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
template <vajra::Printable T>
struct formatter<const T*> : formatter<string> {
  auto format(const T* ptr, format_context& ctx) const {
    if (ptr) {
      return formatter<string>::format(ptr->ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
// formatter specialization for optional of Printable types
//==============================================================================
template <vajra::Printable T>
struct formatter<optional<T>> : formatter<string> {
  auto format(const optional<T>& opt, format_context& ctx) const {
    if (opt.has_value()) {
      return formatter<string>::format(opt.value().ToString(), ctx);
    } else {
      return formatter<string>::format(vajra::kNullString, ctx);
    }
  }
};
//==============================================================================
}  // namespace std
//==============================================================================
