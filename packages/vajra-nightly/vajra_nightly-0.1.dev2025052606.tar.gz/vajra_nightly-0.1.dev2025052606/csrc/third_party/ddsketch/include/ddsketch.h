/*
 * Unless explicitly stated otherwise all files in this repository are licensed
 * under the Apache License 2.0.
 */

#ifndef INCLUDES_DDSKETCH_DDSKETCH_H_
#define INCLUDES_DDSKETCH_DDSKETCH_H_

#include <algorithm>
#include <cmath>
#include <deque>
#include <limits>
#include <numeric>
#include <sstream>
#include <string>

/*
 * A quantile sketch with relative-error guarantees. This sketch computes
 * quantile values with an approximation error that is relative to the actual
 * quantile value. It works on both negative and non-negative input values.
 *
 * For instance, using DDSketch with a relative accuracy guarantee set to 1%, if
 * the expected quantile value is 100, the computed quantile value is guaranteed to
 * be between 99 and 101. If the expected quantile value is 1000, the computed
 * quantile value is guaranteed to be between 990 and 1010.
 * DDSketch works by mapping floating-point input values to bins and counting the
 * number of values for each bin. The underlying structure that keeps track of bin
 * counts is store.
 */

namespace ddsketch {

namespace {
    static const std::string base64_chars = 
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/";

    static inline bool is_base64(unsigned char c) {
        return (isalnum(c) || (c == '+') || (c == '/'));
    }

    std::string base64_encode(unsigned char const* bytes_to_encode, size_t in_len) {
        std::string ret;
        int i = 0;
        int j = 0;
        unsigned char char_array_3[3];
        unsigned char char_array_4[4];

        while (in_len--) {
            char_array_3[i++] = *(bytes_to_encode++);
            if (i == 3) {
                char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
                char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
                char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
                char_array_4[3] = char_array_3[2] & 0x3f;

                for(i = 0; (i <4) ; i++)
                    ret += base64_chars[char_array_4[i]];
                i = 0;
            }
        }

        if (i) {
            for(j = i; j < 3; j++)
                char_array_3[j] = '\0';

            char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
            char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
            char_array_4[3] = char_array_3[2] & 0x3f;

            for (j = 0; (j < i + 1); j++)
                ret += base64_chars[char_array_4[j]];

            while((i++ < 3))
                ret += '=';
        }

        return ret;
    }

    std::string base64_decode(std::string const& encoded_string) {
        size_t in_len = encoded_string.size();
        size_t i = 0;
        size_t j = 0;
        int in_ = 0;
        unsigned char char_array_4[4], char_array_3[3];
        std::string ret;

        while (in_len-- && (encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
            char_array_4[i++] = encoded_string[in_]; in_++;
            if (i == 4) {
                for (i = 0; i < 4; i++)
                    char_array_4[i] = base64_chars.find(char_array_4[i]);

                char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
                char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
                char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

                for (i = 0; (i < 3); i++)
                    ret += char_array_3[i];
                i = 0;
            }
        }

        if (i) {
            for (j = i; j < 4; j++)
                char_array_4[j] = 0;

            for (j = 0; j < 4; j++)
                char_array_4[j] = base64_chars.find(char_array_4[j]);

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for (j = 0; (j < i - 1); j++) ret += char_array_3[j];
        }

        return ret;
    }
}

using RealValue = double;
using Index = int64_t;

static constexpr Index kChunkSize = 128;

// Simplified BinList without templating - just use RealValue directly
class BinList {
 public:
    using Container = std::deque<RealValue>;
    using iterator = Container::iterator;
    using const_iterator = Container::const_iterator;
    using reference = RealValue&;
    using const_reference = const RealValue&;

    iterator begin() {
         return data_.begin();
    }

    iterator end() {
        return data_.end();
    }

    const_iterator begin() const {
        return data_.begin();
    }

    const_iterator end() const {
        return data_.end();
    }

    BinList() = default;

    ~BinList() = default;

    explicit BinList(size_t size) {
        initialize_with_zeros(size);
    }

    BinList(const BinList& bins)
        : data_(bins.data_) {
    }

    BinList(BinList&& bins) noexcept
        : data_(std::move(bins.data_)) {
    }

    BinList& operator=(const BinList& bins) {
        data_ = bins.data_;
        return *this;
    }

    BinList& operator=(BinList&& bins) noexcept {
        data_ = std::move(bins.data_);
        return *this;
    }

    friend std::ostream& operator<<(std::ostream& os, const BinList& bins) {
        for (const auto& elem : bins) {
            os << elem << " ";
        }

        return os;
    }

    size_t size() const {
        return data_.size();
    }

    reference operator[] (int idx) {
        return data_[idx];
    }

    const_reference operator[] (int idx) const {
        return data_[idx];
    }

    reference first() {
        return data_[0];
    }

    reference last() {
        return data_[size() - 1];
    }

    void insert(RealValue elem) {
        data_.push_back(elem);
    }

    RealValue collapsed_count(int start_idx, int end_idx) const {
        if (index_outside_bounds(start_idx) || index_outside_bounds(end_idx)) {
            throw std::invalid_argument("Indexes out of bounds");
        }

        return std::accumulate(
                   data_.begin() + start_idx,
                   data_.begin() + end_idx,
                   RealValue(0));
    }

    bool has_only_zeros() const {
        auto non_zero_item =
            std::find_if(
                    data_.begin(),
                    data_.end(),
                    [](const auto& item) {
                        return item != 0;
                    });

        return non_zero_item == data_.end();
    }

    RealValue sum() const {
        return collapsed_count(0, data_.size());
    }

    void initialize_with_zeros(size_t num_zeros) {
        auto trailing_zeros = Container(num_zeros, 0);
        data_ = trailing_zeros;
    }

    void extend_front_with_zeros(size_t count) {
       auto trailing_zeros = Container(count, 0);

       data_.insert(
           data_.begin(),
           trailing_zeros.begin(),
           trailing_zeros.end());
    }

    void extend_back_with_zeros(size_t count) {
       auto trailing_zeros = Container(count, 0);

       data_.insert(
           data_.end(),
           trailing_zeros.begin(),
           trailing_zeros.end());
    }

    void remove_trailing_elements(size_t count) {
        data_.erase(data_.end() - count, data_.end());
    }

    void remove_leading_elements(size_t count) {
        data_.erase(data_.begin(), data_.begin() + count);
    }

    void replace_range_with_zeros(int start_idx,
                                  int end_idx,
                                  size_t num_zeros) {
        auto zeros = Container(num_zeros, 0);

        data_.erase(data_.begin() + start_idx, data_.begin() + end_idx);
        data_.insert(data_.begin() + start_idx, zeros.begin(), zeros.end());
    }

 private:
    bool index_outside_bounds(size_t idx) const {
        return idx > size();
    }

    Container data_;
};

// Removed the CRTP pattern and BaseStore template

// Simplified DenseStore without templates
class DenseStore {
 public:
    explicit DenseStore(Index chunk_size = kChunkSize)
    : count_(0),
      min_key_(std::numeric_limits<Index>::max()),
      max_key_(std::numeric_limits<Index>::min()),
      chunk_size_(chunk_size),
      offset_(0) {
    }

    std::string to_string() const {
        std::ostringstream repr;

        repr <<  "{";

        Index i = 0;

        for (const auto& sbin : bins_) {
            repr << i++ + offset_ << ": " << sbin << ", ";
        }

        repr << "}, ";

        repr << "min_key:" << min_key_
             << ", max_key:" << max_key_
             << ", offset:" << offset_;

        return repr.str();
    }

    void copy(const DenseStore& store) {
        count_ = store.count_;
        min_key_ = store.min_key_;
        max_key_ = store.max_key_;
        offset_ = store.offset_;
        bins_ = store.bins_;
    }

    const BinList& bins() const {
        return bins_;
    }

    Index offset() const {
        return offset_;
    }

    RealValue count() const {
        return count_;
    }

    Index length() const {
        return bins_.size();
    }

    bool is_empty() const {
        return length() == kEmptyStoreLength;
    }

    void add(Index key, RealValue weight = 1.0) {
        Index idx = get_index(key);

        bins_[idx] += weight;
        count_ += weight;
    }

    Index key_at_rank(RealValue rank, bool lower = true) const {
        auto running_ct = 0.0;

        auto idx = 0;
        for (const auto bin_ct : bins_) {
            running_ct += bin_ct;
            if ((lower && running_ct > rank) ||
                (!lower && running_ct >= rank + 1)) {
                return idx + offset_;
            }
            ++idx;
        }

        return max_key_;
    }

    void merge(const DenseStore& store) {
        if (store.count_ == 0) {
            return;
        }

        if (count_ == 0) {
            copy(store);
            return;
        }

        if (store.min_key_ < min_key_ || store.max_key_ > max_key_) {
            extend_range(store.min_key_, store.max_key_);
        }

        for (auto key = store.min_key_; key <= store.max_key_ ; ++key) {
            bins_[key - offset_] += store.bins_[key - store.offset_];
        }

        count_ += store.count_;
    }

    // Add these methods to the DenseStore class
    std::string serialize_to_binary() const {
        std::stringstream ss;
        
        // Write store metadata
        ss.write(reinterpret_cast<const char*>(&count_), sizeof(RealValue));
        ss.write(reinterpret_cast<const char*>(&min_key_), sizeof(Index));
        ss.write(reinterpret_cast<const char*>(&max_key_), sizeof(Index));
        ss.write(reinterpret_cast<const char*>(&chunk_size_), sizeof(Index));
        ss.write(reinterpret_cast<const char*>(&offset_), sizeof(Index));
        
        // Write bins size
        auto bins_size = static_cast<size_t>(bins_.size());
        ss.write(reinterpret_cast<const char*>(&bins_size), sizeof(size_t));
        
        // Write bin contents
        for (size_t i = 0; i < bins_size; i++) {
            ss.write(reinterpret_cast<const char*>(&bins_[i]), sizeof(RealValue));
        }
        
        return ss.str();
    }

    // Serialize to base64 encoding (safe for JSON/text protocols)
    std::string serialize() const {
        std::string binary_data = serialize_to_binary();
        return base64_encode(reinterpret_cast<const unsigned char*>(binary_data.data()), binary_data.size());
    }

    static DenseStore deserialize_from_binary(const std::string& data) {
        std::stringstream ss(data);
        DenseStore store;
        
        // Read store metadata
        ss.read(reinterpret_cast<char*>(&store.count_), sizeof(RealValue));
        ss.read(reinterpret_cast<char*>(&store.min_key_), sizeof(Index));
        ss.read(reinterpret_cast<char*>(&store.max_key_), sizeof(Index));
        ss.read(reinterpret_cast<char*>(&store.chunk_size_), sizeof(Index));
        ss.read(reinterpret_cast<char*>(&store.offset_), sizeof(Index));
        
        // Read bins size
        size_t bins_size;
        ss.read(reinterpret_cast<char*>(&bins_size), sizeof(size_t));
        
        // Initialize bins with the right size
        store.bins_ = BinList(bins_size);
        
        // Read bin contents
        for (size_t i = 0; i < bins_size; i++) {
            ss.read(reinterpret_cast<char*>(&store.bins_[i]), sizeof(RealValue));
        }
        
        return store;
    }

    // Deserialize from base64 encoding
    static DenseStore deserialize(const std::string& base64_data) {
        std::string binary_data = base64_decode(base64_data);
        return deserialize_from_binary(binary_data);
    }


 protected:
    virtual Index get_new_length(Index new_min_key, Index new_max_key) {
        auto desired_length = new_max_key - new_min_key + 1;
        auto num_chunks = std::ceil((1.0 * desired_length) / chunk_size_);

        return chunk_size_ * num_chunks;
    }

    // Adjust the bins, the offset, the min_key, and max_key
    virtual void adjust(Index new_min_key, Index new_max_key) {
        center_bins(new_min_key, new_max_key);

        min_key_ = new_min_key;
        max_key_ = new_max_key;
    }

    // Shift the bins; this changes the offset
    void shift_bins(Index shift) {
        if (shift > 0) {
            bins_.remove_trailing_elements(shift);
            bins_.extend_front_with_zeros(shift);
        } else {
            auto abs_shift = std::abs(shift);

            bins_.remove_leading_elements(abs_shift);
            bins_.extend_back_with_zeros(abs_shift);
        }

        offset_ -= shift;
    }

    // Center the bins; this changes the offset
    void center_bins(Index new_min_key, Index new_max_key) {
        auto middle_key = new_min_key + (new_max_key - new_min_key + 1) / 2;

        shift_bins(offset_ + length() / 2 - middle_key);
    }

    // Grow the bins as necessary and call adjust
    void extend_range(Index key, Index second_key) {
        auto new_min_key = std::min({key, second_key, min_key_});
        auto new_max_key = std::max({key, second_key, max_key_});

        if (is_empty()) {
            // Initialize bins
            auto new_length = get_new_length(new_min_key, new_max_key);
            bins_.initialize_with_zeros(new_length);
            offset_ = new_min_key;
            adjust(new_min_key, new_max_key);
        } else if (new_min_key >= min_key_ &&
                   new_max_key < offset_ + length()) {
            // No need to change the range; just update min/max keys
            min_key_ = new_min_key;
            max_key_ = new_max_key;
        } else {
            // Grow the bins
            Index new_length = get_new_length(new_min_key, new_max_key);

            if (new_length > length()) {
                bins_.extend_back_with_zeros(new_length - length());
            }

            adjust(new_min_key, new_max_key);
        }
    }

    void extend_range(Index key) {
        extend_range(key, key);
    }

    // Calculate the bin index for the key, extending the range if necessary
    virtual Index get_index(Index key) {
        if (key < min_key_ || key > max_key_) {
            extend_range(key);
        }

        return key - offset_;
    }

 public:
    RealValue count_; // The sum of the counts for the bins
    Index min_key_;   // The minimum key bin
    Index max_key_;   // The maximum key bin

    // The number of bins to grow by
    Index chunk_size_;

    // The difference btw the keys and the index in which they are stored
    Index offset_;
    BinList bins_;

 private:
    static constexpr size_t kEmptyStoreLength = 0;
};

// Exception classes remain unchanged
class IllegalArgumentException : public std::exception {
 public:
    const char* what() const noexcept override {
        return message_.c_str();
    }

    explicit IllegalArgumentException(const std::string& message)
        : message_(message) {
    }

 private:
    std::string message_;
};

class UnequalSketchParametersException : public std::exception {
 public:
    const char* what() const noexcept override {
        return "Cannot merge two DDSketches with different parameters";
    }
};

// Simplified KeyMapping without inheritance
class KeyMapping {
 public:
    explicit KeyMapping(RealValue relative_accuracy,
                        RealValue offset = 0.0) {
        if (relative_accuracy <= 0.0 || relative_accuracy >= 1.0) {
            throw IllegalArgumentException(
                "Relative accuracy must be between 0 and 1");
        }

        relative_accuracy_ = relative_accuracy;
        offset_ = offset;

        auto gamma_mantissa = 2 * relative_accuracy / (1 - relative_accuracy);

        gamma_ = 1.0 + gamma_mantissa;
        multiplier_ = 1.0 / std::log1p(gamma_mantissa);

        min_possible_ = std::numeric_limits<RealValue>::min() * gamma_;
        max_possible_ = std::numeric_limits<RealValue>::max() / gamma_;
        
        // Initialize for logarithmic mapping
        multiplier_ *= std::log(2.0);
    }

    Index key(RealValue value) const {
        return static_cast<Index>(std::ceil(log_gamma(value)) + offset_);
    }

    RealValue value(Index key) const {
        return pow_gamma(key - offset_) * (2.0 / (1 + gamma_));
    }

    RealValue relative_accuracy() const {
        return relative_accuracy_;
    }

    RealValue gamma() const {
        return gamma_;
    }

    RealValue min_possible() const {
        return min_possible_;
    }

    RealValue max_possible() const {
        return max_possible_;
    }

    // Logarithmic mapping implementation
    RealValue log_gamma(RealValue value) const {
        return std::log2(value) * multiplier_;
    }

    RealValue pow_gamma(RealValue value) const {
        return std::exp2(value / multiplier_);
    }

 private:
    static RealValue adjust_accuracy(RealValue relative_accuracy) {
        if (relative_accuracy <= 0.0 || relative_accuracy >= 1.0) {
            return kDefaultRelativeAccuracy;
        }

        return relative_accuracy;
    }

    static constexpr auto kDefaultRelativeAccuracy = 0.01;
    RealValue relative_accuracy_;
    RealValue offset_;
    RealValue gamma_;
    RealValue min_possible_;
    RealValue max_possible_;
    RealValue multiplier_;
};

// Removed the LogarithmicMapping class and merged it into KeyMapping

// Simplified DDSketch without templating
class DDSketch {
public:
    explicit DDSketch(RealValue relative_accuracy)
        : 
          relative_accuracy_(relative_accuracy),
          mapping_(relative_accuracy),
          store_(),
          negative_store_(),
          zero_count_(0.0),
          count_(0.0),
          min_(std::numeric_limits<RealValue>::max()),
          max_(std::numeric_limits<RealValue>::min()),
          sum_(0.0) {
    }

    static std::string name() {
        return "DDSketch";
    }

    RealValue num_values() const {
        return count_;
    }

    RealValue sum() const {
        return sum_;
    }

    RealValue avg() const {
        return sum_ / count_;
    }

    RealValue min() const {
        return min_;
    }

    RealValue max() const {
        return max_;
    }

    RealValue zero_count() const {
        return zero_count_;
    }

    RealValue count() const {
        return count_;
    }

    RealValue relative_accuracy() const {
        return relative_accuracy_;
    }

    // Add a value to the sketch
    void add(RealValue val, RealValue weight = 1.0) {
        if (weight <= 0.0) {
            throw IllegalArgumentException("Weight must be positive");
        }

        if (val > mapping_.min_possible()) {
            store_.add(mapping_.key(val), weight);
        } else if (val < -mapping_.min_possible()) {
            negative_store_.add(mapping_.key(-val), weight);
        } else {
            zero_count_ += weight;
        }

        // Keep track of summary stats
        count_ += weight;
        sum_ += val * weight;

        if (val < min_) {
            min_ = val;
        }

        if (val > max_) {
            max_ = val;
        }
    }

    // The approximate value at the specified quantile
    RealValue get_quantile_value(RealValue quantile) const {
        auto quantile_value = 0.0;

        if (quantile < 0 || quantile > 1 || count_ == 0) {
            return std::nan("");
        }

        auto rank = quantile * (count_ - 1);

        if (rank < negative_store_.count()) {
            auto reversed_rank = negative_store_.count() - rank - 1;
            auto key = negative_store_.key_at_rank(reversed_rank, false);
            quantile_value = -mapping_.value(key);
        } else if (rank < zero_count_ + negative_store_.count()) {
            return 0.0;
        } else {
            auto key = store_.key_at_rank(
                            rank - zero_count_ - negative_store_.count());
            quantile_value = mapping_.value(key);
        }

        return quantile_value;
    }

    // Merges the other sketch into this one
    void merge(const DDSketch& sketch) {
        if (!mergeable(sketch)) {
            throw UnequalSketchParametersException();
        }

        if (sketch.count_ == 0) {
            return;
        }

        if (count_ == 0) {
            copy(sketch);
            return;
        }

        // Merge the stores
        store_.merge(sketch.store_);
        negative_store_.merge(sketch.negative_store_);
        zero_count_ += sketch.zero_count_;

        // Merge summary stats
        count_ += sketch.count_;
        sum_ += sketch.sum_;

        if (sketch.min_ < min_) {
            min_ = sketch.min_;
        }

        if (sketch.max_ > max_) {
            max_ = sketch.max_;
        }
    }

    // Two sketches can be merged only if their gammas are equal
    bool mergeable(const DDSketch& other) const {
        return mapping_.gamma() == other.mapping_.gamma();
    }

    // Copy the input sketch into this one
    void copy(const DDSketch& sketch) {
        store_.copy(sketch.store_);
        negative_store_.copy(sketch.negative_store_);
        zero_count_ = sketch.zero_count_;
        min_ = sketch.min_;
        max_ = sketch.max_;
        count_ = sketch.count_;
        sum_ = sketch.sum_;
    }

    // Add these methods to the DDSketch class
    std::string serialize_to_binary() const {
        std::stringstream ss;
        
        // Write sketch parameters - relative_accuracy
        RealValue relative_accuracy = mapping_.relative_accuracy();
        ss.write(reinterpret_cast<const char*>(&relative_accuracy), sizeof(RealValue));
        
        // Write summary statistics
        ss.write(reinterpret_cast<const char*>(&zero_count_), sizeof(RealValue));
        ss.write(reinterpret_cast<const char*>(&count_), sizeof(RealValue));
        ss.write(reinterpret_cast<const char*>(&min_), sizeof(RealValue));
        ss.write(reinterpret_cast<const char*>(&max_), sizeof(RealValue));
        ss.write(reinterpret_cast<const char*>(&sum_), sizeof(RealValue));
        
        // Serialize positive and negative stores
        std::string store_data = store_.serialize_to_binary();
        std::string negative_store_data = negative_store_.serialize_to_binary();
        
        // Write store data sizes and content
        size_t store_size = store_data.size();
        size_t negative_store_size = negative_store_data.size();
        
        ss.write(reinterpret_cast<const char*>(&store_size), sizeof(size_t));
        ss.write(store_data.data(), store_size);
        
        ss.write(reinterpret_cast<const char*>(&negative_store_size), sizeof(size_t));
        ss.write(negative_store_data.data(), negative_store_size);
        
        return ss.str();
    }

    // Serialize to base64 encoding (safe for JSON/text protocols)
    std::string serialize() const {
        std::string binary_data = serialize_to_binary();
        return base64_encode(reinterpret_cast<const unsigned char*>(binary_data.data()), binary_data.size());
    }

    static DDSketch deserialize_from_binary(const std::string& data) {
        std::stringstream ss(data);
        
        // Read sketch parameters
        RealValue relative_accuracy;
        ss.read(reinterpret_cast<char*>(&relative_accuracy), sizeof(RealValue));
        
        // Create a new sketch with the correct parameters
        DDSketch sketch(relative_accuracy);
        
        // Read summary statistics
        ss.read(reinterpret_cast<char*>(&sketch.zero_count_), sizeof(RealValue));
        ss.read(reinterpret_cast<char*>(&sketch.count_), sizeof(RealValue));
        ss.read(reinterpret_cast<char*>(&sketch.min_), sizeof(RealValue));
        ss.read(reinterpret_cast<char*>(&sketch.max_), sizeof(RealValue));
        ss.read(reinterpret_cast<char*>(&sketch.sum_), sizeof(RealValue));
        
        // Read store data sizes
        size_t store_size, negative_store_size;
        ss.read(reinterpret_cast<char*>(&store_size), sizeof(size_t));
        
        // Read positive store data
        std::string store_data(store_size, '\0');
        ss.read(&store_data[0], store_size);
        sketch.store_ = DenseStore::deserialize_from_binary(store_data);
        
        // Read negative store data
        ss.read(reinterpret_cast<char*>(&negative_store_size), sizeof(size_t));
        std::string negative_store_data(negative_store_size, '\0');
        ss.read(&negative_store_data[0], negative_store_size);
        sketch.negative_store_ = DenseStore::deserialize_from_binary(negative_store_data);
        
        return sketch;
    }

    // Deserialize from base64 encoding
    static DDSketch deserialize(const std::string& base64_data) {
        std::string binary_data = base64_decode(base64_data);
        return deserialize_from_binary(binary_data);
    }

 private:
    static Index adjust_bin_limit(Index bin_limit) {
        if (bin_limit <= 0) {
            return kDefaultBinLimit;
        }

        return bin_limit;
    }

    RealValue relative_accuracy_;
    KeyMapping mapping_;      // Map between values and store bins
    DenseStore store_;        // Storage for positive values
    DenseStore negative_store_; // Storage for negative values
    RealValue zero_count_;    // The count of zero values
    RealValue count_;         // The number of values seen by the sketch
    RealValue min_;           // The minimum value seen by the sketch
    RealValue max_;           // The maximum value seen by the sketch
    RealValue sum_;           // The sum of the values seen by the sketch

    static constexpr Index kDefaultBinLimit = 2048;
};

}  // namespace ddsketch

#endif  // INCLUDES_DDSKETCH_DDSKETCH_H_