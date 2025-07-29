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
//==============================================================================
namespace vajra {
//==============================================================================
enum class PlotType { CDF, HISTOGRAM, TIME_SERIES };
//==============================================================================
enum class UnitType {
  MS,       // Time(ms)
  SECONDS,  // Time(s)
  PERCENT,  // (%)
  COUNT     // count
};
//==============================================================================
enum class LabelType { BATCH, REQUEST };
//==============================================================================
enum class EntityAssociationType { REQUEST, BATCH };
//==============================================================================
enum class ComparisonGroupType {
  GPU_OPERATION_RUNTIME,
  BATCH_RUNTIME,
  BATCH_COMPOSITION,
  REQUEST_RUNTIME
};
//==============================================================================
struct Metric {
  Metric(
      MetricType type_param, UnitType unit_param, bool requires_label_param,
      PlotType plot_type_param,
      std::optional<ComparisonGroupType> comparison_group_param = std::nullopt,
      std::optional<EntityAssociationType> entity_association_group_param =
          std::nullopt,
      std::optional<LabelType> label_type_param = std::nullopt,
      bool aggregate_time_series_param = true)
      : type(type_param),
        name(MetricTypeToString(type_param)),
        unit(unit_param),
        requires_label(requires_label_param),
        plot_type(plot_type_param),
        comparison_group(comparison_group_param),
        entity_association_group(entity_association_group_param),
        label_type(label_type_param),
        aggregate_time_series(aggregate_time_series_param) {}

  // Custom copy constructor
  Metric(const Metric& other)
      : type(other.type),
        name(other.name),
        unit(other.unit),
        requires_label(other.requires_label),
        plot_type(other.plot_type),
        comparison_group(other.comparison_group),
        entity_association_group(other.entity_association_group),
        label_type(other.label_type),
        aggregate_time_series(other.aggregate_time_series) {}

  // Custom move constructor
  Metric(Metric&& other) noexcept
      : type(other.type),
        name(std::move(const_cast<std::string&>(other.name))),
        unit(other.unit),
        requires_label(other.requires_label),
        plot_type(other.plot_type),
        comparison_group(other.comparison_group),
        entity_association_group(other.entity_association_group),
        label_type(other.label_type),
        aggregate_time_series(other.aggregate_time_series) {}

  // Custom copy assignment operator
  Metric& operator=(const Metric& other) {
    if (this != &other) {
      this->~Metric();
      new (this) Metric(other);
    }
    return *this;
  }

  // Custom move assignment operator
  Metric& operator=(Metric&& other) noexcept {
    if (this != &other) {
      this->~Metric();
      new (this) Metric(std::move(other));
    }
    return *this;
  }

  // Returns a string representation of the Metric object
  std::string ToString() const;

  // Equality operator for comparing two Metric objects
  bool operator==(const Metric& other) const {
    return type == other.type && name == other.name && unit == other.unit &&
           requires_label == other.requires_label &&
           plot_type == other.plot_type &&
           comparison_group == other.comparison_group &&
           entity_association_group == other.entity_association_group &&
           label_type == other.label_type &&
           aggregate_time_series == other.aggregate_time_series;
  }

  // Inequality operator for comparing two Metric objects
  bool operator!=(const Metric& other) const { return !(*this == other); }

  const MetricType type;
  const std::string name;
  const UnitType unit;
  const bool requires_label;
  const PlotType plot_type;
  const std::optional<ComparisonGroupType> comparison_group;
  const std::optional<EntityAssociationType> entity_association_group;
  const std::optional<LabelType> label_type;
  const bool aggregate_time_series;
};
//==============================================================================
// Helper functions to convert enum values to strings
std::string PlotTypeToString(PlotType type);
std::string UnitTypeToString(UnitType type);
std::string LabelTypeToString(LabelType type);
std::string EntityAssociationTypeToString(EntityAssociationType type);
std::string ComparisonGroupTypeToString(ComparisonGroupType type);
//==============================================================================
// Helper functions to convert strings to enum values
PlotType StringToPlotType(const std::string& str);
UnitType StringToUnitType(const std::string& str);
LabelType StringToLabelType(const std::string& str);
EntityAssociationType StringToEntityAssociationType(const std::string& str);
ComparisonGroupType StringToComparisonGroupType(const std::string& str);
}  // namespace vajra
//==============================================================================
