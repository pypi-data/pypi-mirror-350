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
#include "commons/Constants.h"
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct MetricsConfig final {
  MetricsConfig(bool write_metrics_param,
                std::optional<std::string> wandb_project_param,
                std::optional<std::string> wandb_group_param,
                std::optional<std::string> wandb_run_name_param,
                std::optional<std::string> wandb_sweep_id_param,
                std::optional<std::string> wandb_run_id_param,
                bool enable_gpu_op_level_metrics_param,
                bool enable_cpu_op_level_metrics_param,
                bool enable_chrome_trace_param,
                bool keep_individual_batch_metrics_param, bool store_png_param,
                std::string output_dir_param)
      : write_metrics(write_metrics_param),
        wandb_project(wandb_project_param),
        wandb_group(wandb_group_param),
        wandb_run_name(wandb_run_name_param),
        wandb_sweep_id(wandb_sweep_id_param),
        wandb_run_id(wandb_run_id_param),
        enable_gpu_op_level_metrics(enable_gpu_op_level_metrics_param),
        enable_cpu_op_level_metrics(enable_cpu_op_level_metrics_param),
        enable_chrome_trace(enable_chrome_trace_param),
        keep_individual_batch_metrics(keep_individual_batch_metrics_param),
        store_png(store_png_param),
        output_dir(output_dir_param) {}

  /// @brief Convert to string representation
  /// @return String representation of the MetricsConfig
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "MetricsConfig(write_metrics={}, wandb_project={}, wandb_group={}, "
        "wandb_run_name={}, wandb_sweep_id={}, wandb_run_id={}, "
        "enable_gpu_op_level_metrics={}, enable_cpu_op_level_metrics={}, "
        "enable_chrome_trace={}, keep_individual_batch_metrics={}, "
        "store_png={}, output_dir={})",
        write_metrics,
        wandb_project.has_value() ? wandb_project.value() : kNullString,
        wandb_group.has_value() ? wandb_group.value() : kNullString,
        wandb_run_name.has_value() ? wandb_run_name.value() : kNullString,
        wandb_sweep_id.has_value() ? wandb_sweep_id.value() : kNullString,
        wandb_run_id.has_value() ? wandb_run_id.value() : kNullString,
        enable_gpu_op_level_metrics, enable_cpu_op_level_metrics,
        enable_chrome_trace, keep_individual_batch_metrics, store_png,
        output_dir);
  }

  const bool write_metrics;
  const std::optional<std::string> wandb_project;
  const std::optional<std::string> wandb_group;
  const std::optional<std::string> wandb_run_name;
  const std::optional<std::string> wandb_sweep_id;
  const std::optional<std::string> wandb_run_id;
  const bool enable_gpu_op_level_metrics;
  const bool enable_cpu_op_level_metrics;
  const bool enable_chrome_trace;
  const bool keep_individual_batch_metrics;
  const bool store_png;
  const std::string output_dir;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
