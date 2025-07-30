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

#include "base_datatypes.pb.h"  // NOLINT
#include "commons/StdCommon.h"
#include "native/configs/ModelConfig.h"
#include "native/datatypes/PendingStepOutput.h"
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceMetadata.h"
#include "native/datatypes/StepInputs.h"
#include "native/datatypes/StepMicrobatchOutputs.h"
#include "native/datatypes/StepOutputs.h"
#include "worker_protocol.pb.h"  // NOLINT
//==============================================================================
namespace vajra {
//==============================================================================
template <typename T>
struct CorrespondingProtoType;  // Map vajra::T -> vajra_proto::U
template <>
struct CorrespondingProtoType<vajra::StepMicrobatchOutputs> {
  using type = vajra_proto::StepMicrobatchOutputs;
};
template <>
struct CorrespondingProtoType<vajra::StepOutputs> {
  using type = vajra_proto::StepOutputs;
};
template <>
struct CorrespondingProtoType<vajra::StepInputs> {
  using type = vajra_proto::StepInputs;
};
//==============================================================================
template <typename P>
struct CorrespondingVajraType;  // Map vajra_proto::P -> vajra::T
template <>
struct CorrespondingVajraType<vajra_proto::StepMicrobatchOutputs> {
  using type = vajra::StepMicrobatchOutputs;
};
template <>
struct CorrespondingVajraType<vajra_proto::StepOutputs> {
  using type = vajra::StepOutputs;
};
template <>
struct CorrespondingVajraType<vajra_proto::StepInputs> {
  using type = vajra::StepInputs;
};
//==============================================================================
class ProtoUtils {
 public:
  ProtoUtils() = delete;
  ~ProtoUtils() = default;

  template <typename T>
  [[nodiscard]] static auto ToProto(const T& obj) ->
      typename CorrespondingProtoType<T>::type {
    if constexpr (std::is_same_v<T, vajra::StepMicrobatchOutputs>) {
      return StepMicrobatchOutputsToProto(obj);
    } else if constexpr (std::is_same_v<T, vajra::StepOutputs>) {
      return StepOutputsToProto(obj);
    } else if constexpr (std::is_same_v<T, vajra::StepInputs>) {
      return StepInputsToProto(obj);
    } else {
      static_assert(!std::is_same_v<T, T>,
                    "Unsupported type T for vajra::ProtoUtils::ToProto");
    }
  }

  template <typename T>
  [[nodiscard]] static T FromProto(
      const typename CorrespondingProtoType<T>::type& proto) {
    if constexpr (std::is_same_v<T, vajra::StepMicrobatchOutputs>) {
      return StepMicrobatchOutputsFromProto(proto);
    } else if constexpr (std::is_same_v<T, vajra::StepOutputs>) {
      return StepOutputsFromProto(proto);
    } else if constexpr (std::is_same_v<T, vajra::StepInputs>) {
      return StepInputsFromProto(proto);
    } else {
      static_assert(!std::is_same_v<T, T>,
                    "Unsupported type T for vajra::ProtoUtils::FromProto");
    }
  }

  template <typename ProtoType>
  [[nodiscard]] static auto FromProto(const ProtoType& proto) ->
      typename CorrespondingVajraType<ProtoType>::type {
    using VajraType = typename CorrespondingVajraType<ProtoType>::type;
    // Ensure the primary template FromProto<VajraType> is visible
    return FromProto<VajraType>(proto);
  }

 private:
  [[nodiscard]] static vajra_proto::StepMicrobatchOutputs
  StepMicrobatchOutputsToProto(const vajra::StepMicrobatchOutputs& obj);
  [[nodiscard]] static vajra::StepMicrobatchOutputs
  StepMicrobatchOutputsFromProto(
      const vajra_proto::StepMicrobatchOutputs& proto);

  [[nodiscard]] static vajra_proto::StepOutputs StepOutputsToProto(
      const vajra::StepOutputs& obj);
  [[nodiscard]] static vajra::StepOutputs StepOutputsFromProto(
      const vajra_proto::StepOutputs& proto);

  [[nodiscard]] static vajra_proto::StepInputs StepInputsToProto(
      const vajra::StepInputs& obj);
  [[nodiscard]] static vajra::StepInputs StepInputsFromProto(
      const vajra_proto::StepInputs& proto);

  // Corrected signatures for shared_ptr parameters
  [[nodiscard]] static vajra_proto::SamplerOutput SamplerOutputToProto(
      const vajra::SamplerOutputPtr& obj);  // Add const&
  [[nodiscard]] static vajra::SamplerOutputPtr SamplerOutputFromProto(
      const vajra_proto::SamplerOutput& proto);

  [[nodiscard]] static vajra_proto::SchedulerOutput SchedulerOutputToProto(
      const vajra::SchedulerOutputPtr& obj);  // Add const&
  [[nodiscard]] static vajra::SchedulerOutput SchedulerOutputFromProto(
      const vajra_proto::SchedulerOutput& proto);

  [[nodiscard]] static vajra_proto::SequenceParams SequenceParamsToProto(
      const vajra::SequenceParams& obj);
  [[nodiscard]] static vajra::SequenceParams SequenceParamsFromProto(
      const vajra_proto::SequenceParams& proto);

  [[nodiscard]] static vajra_proto::PendingStepOutput PendingStepOutputToProto(
      const vajra::PendingStepOutput& obj);
  [[nodiscard]] static vajra::PendingStepOutput PendingStepOutputFromProto(
      const vajra_proto::PendingStepOutput& proto);

  [[nodiscard]] static vajra_proto::SequenceScheduleMetadata
  SequenceScheduleMetadataToProto(
      const vajra::SequenceScheduleMetadataPtr& obj);  // Add const&
  [[nodiscard]] static vajra::SequenceScheduleMetadataPtr
  SequenceScheduleMetadataFromProto(
      const vajra_proto::SequenceScheduleMetadata& proto);

  [[nodiscard]] static vajra_proto::SamplingParams SamplingParamsToProto(
      const vajra::SamplingParams& obj);
  [[nodiscard]] static vajra::SamplingParams SamplingParamsFromProto(
      const vajra_proto::SamplingParams& proto);

  [[nodiscard]] static vajra_proto::ModelConfig ModelConfigToProto(
      const vajra::ModelConfig& obj);
  [[nodiscard]] static vajra::ModelConfig ModelConfigFromProto(
      const vajra_proto::ModelConfig& proto);
  //==============================================================================
  // Utility methods
  //==============================================================================
  template <typename T>
  [[nodiscard]] static std::vector<T> ExtractRepeatedField(
      const google::protobuf::RepeatedPtrField<T>& repeated_field) {
    std::vector<T> result;
    result.reserve(repeated_field.size());
    result.assign(repeated_field.begin(), repeated_field.end());
    return result;
  }

  template <typename T>
  [[nodiscard]] static std::vector<T> ExtractRepeatedField(
      const google::protobuf::RepeatedField<T>& repeated_field) {
    std::vector<T> result;
    result.reserve(repeated_field.size());
    result.assign(repeated_field.begin(), repeated_field.end());
    return result;
  }
};
//==============================================================================
}  // namespace vajra
//==============================================================================
