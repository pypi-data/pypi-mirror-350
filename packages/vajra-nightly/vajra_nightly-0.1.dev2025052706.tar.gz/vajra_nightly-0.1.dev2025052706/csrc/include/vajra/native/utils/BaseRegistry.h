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
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * A generic registry base class template. Subclasses will have their own
 * registry map. Each subclass can store implementations keyed by an enum type.
 *
 * This is a C++ translation of the Python BaseRegistry class.
 */
template <typename EnumType, typename BaseType>
class BaseRegistry : public NonCopyableNonMovable {
 protected:
  // Each subclass gets its own registry map
  using RegistryMap =
      std::unordered_map<EnumType,
                         std::function<std::shared_ptr<BaseType>(void)>>;
  static RegistryMap _registry;

 public:
  /**
   * Register an implementation class with the registry.
   *
   * @param key The enum key to register the implementation under
   * @param factory A factory function that creates instances of the
   * implementation
   */
  template <typename ImplType>
  static void Register(EnumType key) {
    if (_registry.find(key) != _registry.end()) {
      return;  // Already registered
    }

    _registry[key] = []() -> std::shared_ptr<BaseType> {
      return std::make_shared<ImplType>();
    };
  }

  /**
   * Register an implementation class with the registry with custom factory
   * function.
   *
   * @param key The enum key to register the implementation under
   * @param factory A factory function that creates instances of the
   * implementation
   */
  static void RegisterWithFactory(
      EnumType key, std::function<std::shared_ptr<BaseType>(void)> factory) {
    if (_registry.find(key) != _registry.end()) {
      return;  // Already registered
    }

    _registry[key] = factory;
  }

  /**
   * Unregister an implementation from the registry.
   *
   * @param key The enum key to unregister
   * @throws std::invalid_argument if the key is not registered
   */
  static void Unregister(EnumType key) {
    if (_registry.find(key) == _registry.end()) {
      throw std::invalid_argument("Key is not registered");
    }

    _registry.erase(key);
  }

  /**
   * Get an instance of the implementation registered under the given key.
   *
   * @param key The enum key to get the implementation for
   * @return A shared pointer to the implementation instance
   * @throws std::invalid_argument if the key is not registered
   */
  static std::shared_ptr<BaseType> Get(EnumType key) {
    if (_registry.find(key) == _registry.end()) {
      throw std::invalid_argument("Key is not registered");
    }

    return _registry[key]();
  }
};

// Initialize the static registry map for each template instantiation
template <typename EnumType, typename BaseType>
typename BaseRegistry<EnumType, BaseType>::RegistryMap
    BaseRegistry<EnumType, BaseType>::_registry = {};
//==============================================================================
}  // namespace vajra
//==============================================================================
