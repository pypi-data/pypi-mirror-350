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
#include "commons/Time.h"
#include "native/metrics_store/BaseMetricsStore.h"
#include "native/metrics_store/MetricType.h"
//==============================================================================
namespace vajra {
//==============================================================================
class CpuTimer : public NonCopyableNonMovable {
 public:
  // Constructor that initializes the timer but doesn't start it
  CpuTimer(std::optional<MetricType> metric_type,
           std::shared_ptr<BaseMetricsStore> metrics_store);

  // Non-copyable
  CpuTimer(const CpuTimer&) = delete;
  CpuTimer& operator=(const CpuTimer&) = delete;

  // Movable
  CpuTimer(CpuTimer&&) = default;
  CpuTimer& operator=(CpuTimer&&) = default;

  // Destructor
  ~CpuTimer() = default;

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
  std::shared_ptr<BaseMetricsStore> metrics_store_;
  bool disabled_;

  double start_time_;
  double end_time_;
};
//==============================================================================
// RAII guard class for CpuTimer
class CpuTimer::Guard : public NonCopyableNonMovable {
 public:
  // Constructor starts the timer
  explicit Guard(CpuTimer& timer) : timer_(timer) { timer_.Start(); }

  // Non-copyable
  Guard(const Guard&) = delete;
  Guard& operator=(const Guard&) = delete;

  // Movable
  Guard(Guard&&) = default;
  Guard& operator=(Guard&&) = default;

  // Destructor stops the timer
  ~Guard() { timer_.Stop(); }

 private:
  CpuTimer& timer_;
};

// Factory method implementation
inline CpuTimer::Guard CpuTimer::TimeOperation() { return Guard(*this); }
//==============================================================================
}  // namespace vajra
//==============================================================================
