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
#include "native/metrics_store/Types.h"

#include "commons/Logging.h"
#include "commons/StdCommon.h"
//==============================================================================
using vajra::ComparisonGroupType;
using vajra::EntityAssociationType;
using vajra::LabelType;
using vajra::Metric;
using vajra::PlotType;
using vajra::UnitType;
//==============================================================================
std::string vajra::PlotTypeToString(PlotType type) {
  switch (type) {
    case PlotType::CDF:
      return "cdf";
    case PlotType::HISTOGRAM:
      return "histogram";
    case PlotType::TIME_SERIES:
      return "time_series";
    default:
      RAISE_INVALID_ARGUMENTS_ERROR("Unknown PlotType");
  }
}
//==============================================================================
std::string vajra::UnitTypeToString(UnitType type) {
  switch (type) {
    case UnitType::MS:
      return "Time(ms)";
    case UnitType::SECONDS:
      return "Time(s)";
    case UnitType::PERCENT:
      return "(%)";
    case UnitType::COUNT:
      return "count";
    default:
      RAISE_INVALID_ARGUMENTS_ERROR("Unknown UnitType");
  }
}
//==============================================================================
std::string vajra::LabelTypeToString(LabelType type) {
  switch (type) {
    case LabelType::BATCH:
      return "Batch";
    case LabelType::REQUEST:
      return "Request";
    default:
      RAISE_INVALID_ARGUMENTS_ERROR("Unknown LabelType");
  }
}
//==============================================================================
std::string vajra::EntityAssociationTypeToString(EntityAssociationType type) {
  switch (type) {
    case EntityAssociationType::REQUEST:
      return "Request";
    case EntityAssociationType::BATCH:
      return "Batch";
    default:
      RAISE_INVALID_ARGUMENTS_ERROR("Unknown EntityAssociationType");
  }
}
//==============================================================================
std::string vajra::ComparisonGroupTypeToString(ComparisonGroupType type) {
  switch (type) {
    case ComparisonGroupType::GPU_OPERATION_RUNTIME:
      return "Gpu Operation Runtime";
    case ComparisonGroupType::BATCH_RUNTIME:
      return "Batch Runtime";
    case ComparisonGroupType::BATCH_COMPOSITION:
      return "Batch Composition";
    case ComparisonGroupType::REQUEST_RUNTIME:
      return "Request Runtime";
    default:
      RAISE_INVALID_ARGUMENTS_ERROR("Unknown ComparisonGroupType");
  }
}
//==============================================================================
PlotType vajra::StringToPlotType(const std::string& str) {
  if (str == "cdf") return PlotType::CDF;
  if (str == "histogram") return PlotType::HISTOGRAM;
  if (str == "time_series") return PlotType::TIME_SERIES;
  RAISE_INVALID_ARGUMENTS_ERROR("Unknown PlotType string: {}", str);
}
//==============================================================================
UnitType vajra::StringToUnitType(const std::string& str) {
  if (str == "Time(ms)") return UnitType::MS;
  if (str == "Time(s)") return UnitType::SECONDS;
  if (str == "(%)") return UnitType::PERCENT;
  if (str == "count") return UnitType::COUNT;
  RAISE_INVALID_ARGUMENTS_ERROR("Unknown UnitType string: {}", str);
}
//==============================================================================
LabelType vajra::StringToLabelType(const std::string& str) {
  if (str == "Batch") return LabelType::BATCH;
  if (str == "Request") return LabelType::REQUEST;
  RAISE_INVALID_ARGUMENTS_ERROR("Unknown LabelType string: {}", str);
}
//==============================================================================
EntityAssociationType vajra::StringToEntityAssociationType(
    const std::string& str) {
  if (str == "Request") return EntityAssociationType::REQUEST;
  if (str == "Batch") return EntityAssociationType::BATCH;
  RAISE_INVALID_ARGUMENTS_ERROR("Unknown EntityAssociationType string: {}",
                                str);
}
//==============================================================================
ComparisonGroupType vajra::StringToComparisonGroupType(const std::string& str) {
  if (str == "Gpu Operation Runtime")
    return ComparisonGroupType::GPU_OPERATION_RUNTIME;
  if (str == "Batch Runtime") return ComparisonGroupType::BATCH_RUNTIME;
  if (str == "Batch Composition") return ComparisonGroupType::BATCH_COMPOSITION;
  if (str == "Request Runtime") return ComparisonGroupType::REQUEST_RUNTIME;
  RAISE_INVALID_ARGUMENTS_ERROR("Unknown ComparisonGroupType string: {}", str);
}
//==============================================================================
std::string Metric::ToString() const {
  auto comparison_group_str =
      comparison_group.has_value()
          ? ComparisonGroupTypeToString(comparison_group.value())
          : "n/a";
  auto entity_association_group_str =
      entity_association_group.has_value()
          ? EntityAssociationTypeToString(entity_association_group.value())
          : "n/a";
  auto label_type_str =
      label_type.has_value() ? LabelTypeToString(label_type.value()) : "n/a";
  return std::format(
      "Metric("
      "name={}, "
      "unit={}, "
      "requires_label={}, "
      "plot_type={}, "
      "comparison_group={}, "
      "entity_association_group={}, "
      "label_type={}, "
      "aggregate_time_series={})",
      name, UnitTypeToString(unit), requires_label, PlotTypeToString(plot_type),
      comparison_group_str, entity_association_group_str, label_type_str,
      aggregate_time_series);
}
//==============================================================================
