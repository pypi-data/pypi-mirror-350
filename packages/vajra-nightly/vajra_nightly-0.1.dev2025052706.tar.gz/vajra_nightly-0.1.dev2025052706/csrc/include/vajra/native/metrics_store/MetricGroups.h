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
#include "commons/StdCommon.h"
#include "native/metrics_store/MetricType.h"
#include "native/metrics_store/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Get GPU Operation Metrics
std::vector<MetricType> GetGpuOperationMetricsTypes();
std::vector<Metric> GetGpuOperationMetrics(bool requires_label = false);

// Get CPU Operation Metrics
std::vector<MetricType> GetCpuOperationMetricsTypes();
std::vector<Metric> GetCpuOperationMetrics(bool requires_label = false);

// Get Sequence Time Distribution Metrics
std::vector<MetricType> GetSequenceTimeDistributionMetricsTypes();
std::vector<Metric> GetSequenceTimeDistributionMetrics();

// Get Sequence Histogram Metrics
std::vector<MetricType> GetSequenceHistogramMetricsTypes();
std::vector<Metric> GetSequenceHistogramMetrics();

// Get Batch Count Distribution Metrics
std::vector<MetricType> GetBatchCountDistributionMetricsTypes();
std::vector<Metric> GetBatchCountDistributionMetrics(
    bool requires_label = false);

// Get Batch Time Distribution Metrics
std::vector<MetricType> GetBatchTimeDistributionMetricsTypes();
std::vector<Metric> GetBatchTimeDistributionMetrics(
    bool requires_label = false);

// Get Token Time Distribution Metrics
std::vector<MetricType> GetTokenTimeDistributionMetricsTypes();
std::vector<Metric> GetTokenTimeDistributionMetrics();

// Get Completion Time Series Metrics
std::vector<MetricType> GetCompletionTimeSeriesMetricsTypes();
std::vector<Metric> GetCompletionTimeSeriesMetrics();

// Get all metrics based on configuration
std::vector<Metric> GetAllMetrics(bool write_metrics = true,
                                  bool keep_individual_batch_metrics = false,
                                  bool enable_gpu_op_level_metrics = false,
                                  bool enable_cpu_op_level_metrics = false);

}  // namespace vajra
//==============================================================================
