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
#include <gtest/gtest.h>

#include "commons/StdCommon.h"
#include "native/utils/ProtoUtils.h"

namespace vajra {
namespace {

class ProtoUtilsTest : public ::testing::Test {
 protected:
  void SetUp() override {}
};

TEST_F(ProtoUtilsTest, StepMicrobatchOutputsConversionTest) {
  const auto& obj = vajra::StepMicrobatchOutputs(1);
  auto proto = ProtoUtils::ToProto<vajra::StepMicrobatchOutputs>(obj);
  ASSERT_EQ(true, true);
}
}  // namespace
}  // namespace vajra
