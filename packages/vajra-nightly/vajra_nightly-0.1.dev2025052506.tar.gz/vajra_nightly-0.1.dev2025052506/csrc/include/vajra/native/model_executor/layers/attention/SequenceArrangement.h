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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/datatypes/SequenceMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr int64_t LONG_REQUEST_THRESHOLD = 256 * 1024;  // 256K
//==============================================================================
class BaseSequenceArrangement;
//==============================================================================
using BaseSequenceArrangementPtr = std::shared_ptr<BaseSequenceArrangement>;
using ContainerType =
    std::variant<SequenceMetadataVector, BaseSequenceArrangementPtr>;
//==============================================================================
class BaseSequenceArrangement {
 public:
  virtual ~BaseSequenceArrangement() = default;

  void Append(SequenceMetadataPtr seq_metadata /*[in]*/);
  void Extend(const SequenceMetadataVector& seq_metadata_list /*[in]*/);
  void CheckArrangementAndExtend(
      const SequenceMetadataVector& seq_metadata_list /*[in]*/);
  void Clear();
  [[nodiscard]] SequenceMetadataVector GetArranged() const;
  [[nodiscard]] std::vector<SequenceMetadataVector> GetSplits() const;
  [[nodiscard]] int GetNumSplits() const;

 protected:
  BaseSequenceArrangement(ContainerType r1 /*[in]*/, ContainerType r2 /*[in]*/);
  virtual bool CheckPredicate(
      SequenceMetadataPtr seq_metadata /*[in]*/) const = 0;

  ContainerType r1_;
  ContainerType r2_;
};
//==============================================================================
class SequenceGroupArrangement : public BaseSequenceArrangement {
 public:
  SequenceGroupArrangement();

 protected:
  bool CheckPredicate(SequenceMetadataPtr seq_metadata /*[in]*/) const override;
};
//==============================================================================
class SaveKvCacheBasedSequenceArrangement : public BaseSequenceArrangement {
 public:
  SaveKvCacheBasedSequenceArrangement();

 protected:
  bool CheckPredicate(SequenceMetadataPtr seq_metadata /*[in]*/) const override;
};
//==============================================================================
class LengthBasedSequenceArrangement : public BaseSequenceArrangement {
 public:
  LengthBasedSequenceArrangement();

 protected:
  bool CheckPredicate(SequenceMetadataPtr seq_metadata /*[in]*/) const override;
};
//==============================================================================
class SequenceArrangement : public BaseSequenceArrangement {
  /*
    We need to arrange sequences in a way that allows us to perform
    attention computation in an efficient manner. Due to poor handling of mixed
    batches in attention kernels. We need to split the first split the sequences
    into prefill and decode: | prefill seqs | decode seqs |

    Secondly, when we mix sequences of different lengths, the attention kernel
    parallelization heuristics fail, and results in high latency. Thus, we need
    to further split the sequences: | long seqs | short seqs |

    Furthermore, within each group, we can have kvp sequences. Some of these kvp
    sequences might not require kv cache to be saved. So, within each group, we
    need to further organize sequences as follows: | seqs w/ save_kv_cache |
    seqs w/o save_kv_cache |

    Finally, we need to organize the sequences in a way that allows us to
    perform kvp reduction in an efficient manner. We need to organize the
    sequences in the following way: | non kvp seqs | kvp seqs | However, for
    this last bit, we don't need to make a separate kernel call, just sorting
    the sequences in this order is sufficient.
  */
 public:
  SequenceArrangement();

 protected:
  bool CheckPredicate(SequenceMetadataPtr seq_metadata /*[in]*/) const override;
};
//==============================================================================
using SequenceArrangementPtr = std::shared_ptr<SequenceArrangement>;
//==============================================================================
}  // namespace vajra
//==============================================================================
