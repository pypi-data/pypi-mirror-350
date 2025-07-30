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
#include "commons/ClassTraits.h"
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
#include "native/metrics_store/MetricType.h"
#include "native/metrics_store/WorkerMetricsStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
class CudaTimer : public NonCopyableNonMovable {
 public:
  // Constructor that initializes the timer but doesn't start it
  CudaTimer(std::optional<MetricType> metric_type,
            std::shared_ptr<WorkerMetricsStore> metrics_store,
            std::optional<int> layer_id = std::nullopt);

  // Non-copyable
  CudaTimer(const CudaTimer&) = delete;
  CudaTimer& operator=(const CudaTimer&) = delete;

  // Movable
  CudaTimer(CudaTimer&&) = default;
  CudaTimer& operator=(CudaTimer&&) = default;

  // Destructor
  ~CudaTimer() = default;

  // Manually start the timer
  void Start();

  // Manually stop the timer
  void Stop();

  // Factory method to create a RAII-style timer guard
  class Guard;
  [[nodiscard]] Guard TimeOperation();

  // Check if the timer is disabled
  bool IsDisabled() const { return disabled_; }

 private:
  std::optional<MetricType> metric_type_;
  std::shared_ptr<WorkerMetricsStore> metrics_store_;
  std::optional<int> layer_id_;
  bool disabled_;

  std::shared_ptr<at::cuda::CUDAEvent> start_event_;
  std::shared_ptr<at::cuda::CUDAEvent> end_event_;
};

//==============================================================================
// RAII guard class for CudaTimer
class CudaTimer::Guard : public NonCopyableNonMovable {
 public:
  // Constructor starts the timer
  explicit Guard(CudaTimer& timer) : timer_(timer) { timer_.Start(); }

  // Non-copyable
  Guard(const Guard&) = delete;
  Guard& operator=(const Guard&) = delete;

  // Movable
  Guard(Guard&&) = default;
  Guard& operator=(Guard&&) = default;

  // Destructor stops the timer
  ~Guard() { timer_.Stop(); }

 private:
  CudaTimer& timer_;
};
//==============================================================================
// Factory method implementation
inline CudaTimer::Guard CudaTimer::TimeOperation() { return Guard(*this); }
//==============================================================================
}  // namespace vajra
//==============================================================================
