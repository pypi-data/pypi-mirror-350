# -*- makefile -*-

# Add new non-file targets here
.PHONY: help lint lint/black lint/isort lint/autoflake lint/pyright lint/cpplint lint/clang-format lint/codespell \
        format format/black format/isort format/autoflake format/clang \
        docs docs/build docs/clean \
        setup/dependencies setup/environment \
        build build/native build/native_test build/native_incremental build/native_test_incremental build/wheel \
        test test/performance test/correctness test/functional test/pyunit test/pyintegration test/ctest test/unit test/integration \
        test_reports logs clean \
        _setup_dirs

.DEFAULT_GOAL := help

# --- Configuration & Variables ---

# Directories
BUILD_DIR := build
TEST_REPORTS_DIR := test_reports
LOG_DIR := logs
SHELL := bash
.SHELLFLAGS := -o pipefail -ec

# Find C++ files
CPP_FILES := $(shell find csrc -type f \( -name "*.cpp" -o -name "*.h" \) -not -path "*/third_party/*")

# --- Environment Variable Dependent Variables ---

# Use environment variables if defined, otherwise use defaults
ifdef VAJRA_CI_CUDA_VERSION
  _CUDA_MAJOR := $(shell echo $(VAJRA_CI_CUDA_VERSION) | cut -d. -f1)
  _CUDA_MINOR := $(shell echo $(VAJRA_CI_CUDA_VERSION) | cut -d. -f2)
  CUDA_VERSION := cu$(_CUDA_MAJOR)$(_CUDA_MINOR)
else
  CUDA_VERSION := cu124
endif

# Use VAJRA_CI_TORCH_VERSION if set, otherwise default to 2.6
# $(if ...) is Make's conditional function
TORCH_VERSION ?= $(if $(VAJRA_CI_TORCH_VERSION),$(VAJRA_CI_TORCH_VERSION),2.6)

# Build type configuration: Default to Debug if not set externally
BUILD_TYPE ?= Debug

# --- Logging & Formatting ---

# Check if NO_COLOR is set
_NO_COLOR := $(NO_COLOR)
# Check if stdout is a TTY
_IS_TTY := $(shell test -t 1 && echo true)

# Only use colors if NO_COLOR is not set AND stdout is a TTY
ifeq ($(_IS_TTY),true)
  ifndef _NO_COLOR
    _USE_COLOR = true
  endif
endif

ifdef _USE_COLOR
    BOLD    := \033[1m
    GREEN   := \033[0;32m
    YELLOW  := \033[0;33m
    BLUE    := \033[0;94m
    CYAN    := \033[0;36m
    RESET   := \033[0m
    # Use echo -e for ANSI interpretation
    ECHO = /bin/echo -e
else
    BOLD    :=
    GREEN   :=
    YELLOW  :=
    BLUE    :=
    CYAN    :=
    RESET   :=
    ECHO = /bin/echo
endif

# Emojis
SETUP_ICON="⚙️ "
LINT_ICON="✨"
FORMAT_ICON="💅"
DOCS_ICON="📚"
BUILD_ICON="🧱"
TEST_ICON="🧪"
CLEAN_ICON="🧼"
INFO_ICON="ℹ️ "
SUCCESS_ICON="✅"
PARTY_ICON="🎉"
WARN_ICON="⚠️ "

# Timestamp for log files (evaluated once per 'make' invocation)
TIMESTAMP = $(shell date +%Y%m%d_%H%M%S)

# --- Helper Targets ---

# Internal: Create necessary directories
_setup_dirs:
	@$(ECHO) "$(BLUE)$(SETUP_ICON) Ensuring directories exist: $(BUILD_DIR), $(TEST_REPORTS_DIR), $(LOG_DIR)$(RESET)"
	@mkdir -p $(BUILD_DIR) $(TEST_REPORTS_DIR) $(LOG_DIR)

# Alias for the directory target
logs: _setup_dirs
test_reports: _setup_dirs

# --- Setup & Preparation ---

setup/dependencies: _setup_dirs ## install python dependencies
	@$(ECHO) "$(BOLD)$(SETUP_ICON) Installing Python Dependencies...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Using CUDA=$(YELLOW)$(CUDA_VERSION)$(BLUE), Torch=$(YELLOW)$(TORCH_VERSION)$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Full log: $(LOG_DIR)/pip_install_$(TIMESTAMP).log$(RESET)"
	pip install -r requirements.txt --extra-index-url https://flashinfer.ai/whl/$(CUDA_VERSION)/torch$(TORCH_VERSION)/ 2>&1 | tee "$(LOG_DIR)/pip_install_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Dependencies installed successfully $(PARTY_ICON)$(RESET)"

setup/environment: ## create conda/mamba development environment
	@$(ECHO) "$(BOLD)$(SETUP_ICON) Setting up Conda/Mamba Environment...$(RESET)"
	@$(ECHO) "$(YELLOW)Action:$(RESET) Running 'mamba env create -f environment-dev.yml -p ./env'"
	@mamba env create -f environment-dev.yml -p ./env
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Success!$(RESET) Activate using: $(CYAN)conda activate ./env$(RESET)"

# --- Linting --- (Checks code quality without modifying files)

lint/black: ## check python style with black
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (Black Check)...$(RESET)"
	@black --check vajra test

lint/isort: ## check python style with isort
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (isort Check)...$(RESET)"
	@isort --check-only --profile black vajra test

lint/autoflake: ## check for unused python imports
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (autoflake Check)...$(RESET)"
	@autoflake --recursive --remove-all-unused-imports --check vajra test

lint/pyright: ## run python type checking
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (Pyright Type Check)...$(RESET)"
	@pyright

lint/cpplint: ## run C++ style checks with cpplint
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (cpplint Check)...$(RESET)"
	@cpplint \
	--recursive \
	--exclude=csrc/third_party \
	--exclude=csrc/include/vajra/kernels \
	--exclude=csrc/vajra/kernels \
	--filter="-build/include_what_you_use,-whitespace/parens,-whitespace/braces,-runtime/references" \
	csrc

lint/clang-format: ## check C++ format with clang-format
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (clang-format Check)...$(RESET)"
	@clang-format -n -Werror $(CPP_FILES)

lint/codespell: ## check for common misspellings
	@$(ECHO) "$(BLUE)$(LINT_ICON) Linting (codespell Check)...$(RESET)"
	@codespell \
	--skip './csrc/third_party/**,./csrc/test/testdata/**,./build/**,*.log,./env*/**,./docs/_build/**,./$(TEST_REPORTS_DIR)/**,./$(LOG_DIR)/**' \
	-L inout

lint: lint/isort lint/black lint/autoflake lint/codespell lint/pyright lint/clang-format lint/cpplint ## lint all code
	@$(ECHO) "$(GREEN)$(LINT_ICON) All Linting Checks Passed $(PARTY_ICON)$(RESET)"

# --- Formatting --- (Modifies code files)

format/black: ## format python code with black
	@$(ECHO) "$(BLUE)$(FORMAT_ICON) Formatting (Black)...$(RESET)"
	@black vajra test

format/isort: ## format python imports with isort
	@$(ECHO) "$(BLUE)$(FORMAT_ICON) Formatting (isort)...$(RESET)"
	@isort --profile black vajra test

format/autoflake: ## remove unused python imports
	@$(ECHO) "$(BLUE)$(FORMAT_ICON) Formatting (autoflake - Removing unused imports)...$(RESET)"
	@autoflake --in-place --recursive --remove-all-unused-imports vajra test

format/clang: ## format C++ code with clang-format
	@$(ECHO) "$(BLUE)$(FORMAT_ICON) Formatting (clang-format)...$(RESET)"
	@clang-format -i $(CPP_FILES)

format: format/isort format/autoflake format/black format/clang ## format all code
	@$(ECHO) "$(GREEN)$(FORMAT_ICON) Code Formatting Complete $(SUCCESS_ICON)$(RESET)"

# --- Documentation ---

docs/build: ## build documentation using Sphinx
	@$(ECHO) "$(BOLD)$(DOCS_ICON) Building Documentation...$(RESET)"
	@$(MAKE) -C docs html
	@$(ECHO) "$(GREEN)$(DOCS_ICON) Documentation build complete (see docs/_build/html) $(SUCCESS_ICON)$(RESET)"

docs/clean: ## clean documentation artifacts
	@$(ECHO) "$(BOLD)$(DOCS_ICON) Cleaning Documentation Artifacts...$(RESET)"
	@$(MAKE) -C docs clean

docs: docs/build ## build documentation (alias for docs/build)

# --- Building ---

# Internal: Configure CMake step (can be used as dependency)
_cmake_configure: _setup_dirs
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Configuring CMake...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Build Type=$(YELLOW)$(BUILD_TYPE)$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Full log: $(LOG_DIR)/cmake_configure_$(TIMESTAMP).log$(RESET)"
	@(cd $(BUILD_DIR) && \
	cmake -G Ninja \
		-DCMAKE_BUILD_TYPE=$(BUILD_TYPE) \
		-DVAJRA_PYTHON_EXECUTABLE=`which python3` \
		-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=../vajra \
		.. ) 2>&1 | tee "$(LOG_DIR)/cmake_configure_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) CMake configuration complete$(RESET)"

build/native: setup/dependencies _cmake_configure ## build native extension (full build)
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Building Native Extension...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Build log: $(LOG_DIR)/cmake_build_native_$(TIMESTAMP).log$(RESET)"
	@(cd $(BUILD_DIR) && cmake --build . --target default) 2>&1 | tee "$(LOG_DIR)/cmake_build_native_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Native extension build complete$(RESET)"

build/native_incremental: _setup_dirs ## build native extension (incremental)
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Building Native Extension (Incremental Build)...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Build log: $(LOG_DIR)/cmake_build_native_incr_$(TIMESTAMP).log$(RESET)"
	@(cd $(BUILD_DIR) && cmake --build . --target default) 2>&1 | tee "$(LOG_DIR)/cmake_build_native_incr_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Native extension incremental build complete$(RESET)"

build/native_test: setup/dependencies _cmake_configure ## build native tests (full build)
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Building Native Tests...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Build log: $(LOG_DIR)/cmake_build_tests_$(TIMESTAMP).log$(RESET)"
	@(cd $(BUILD_DIR) && cmake --build . --target all_tests) 2>&1 | tee "$(LOG_DIR)/cmake_build_tests_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Native tests build complete$(RESET)"

build/native_test_incremental: _setup_dirs ## build native tests (incremental)
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Building Native Tests (Incremental Build)...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Build log: $(LOG_DIR)/cmake_build_tests_incr_$(TIMESTAMP).log$(RESET)"
	@(cd $(BUILD_DIR) && cmake --build . --target all_tests) 2>&1 | tee "$(LOG_DIR)/cmake_build_tests_incr_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Native tests incremental build complete$(RESET)"

build/wheel: _setup_dirs ## build python wheel and sdist
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Building Wheel and SDist...$(RESET)"
	python -m build --no-isolation --wheel
	python -m build --no-isolation --sdist
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Wheel and SDist created in dist/$(RESET)"

build: setup/dependencies ## build project (install editable package)
	@$(ECHO) "$(BOLD)$(BUILD_ICON) Installing Editable Package...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Using CUDA=$(YELLOW)$(CUDA_VERSION)$(BLUE), Torch=$(YELLOW)$(TORCH_VERSION)$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Install log: $(LOG_DIR)/pip_install_editable_$(TIMESTAMP).log$(RESET)"
	pip install -e . --extra-index-url https://flashinfer.ai/whl/$(CUDA_VERSION)/torch$(TORCH_VERSION)/ 2>&1 | tee "$(LOG_DIR)/pip_install_editable_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Editable package installed successfully$(RESET)"

# --- Testing ---

test/performance: test_reports ## run performance tests
	@$(ECHO) "$(BOLD)$(TEST_ICON) Running Performance Tests...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Test log: $(LOG_DIR)/pytest_performance_$(TIMESTAMP).log$(RESET)"
	pytest -m performance --junitxml=$(TEST_REPORTS_DIR)/performance-results.xml 2>&1 | tee "$(LOG_DIR)/pytest_performance_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Performance tests complete$(RESET)"

test/correctness: ## run correctness tests (placeholder)
	@$(ECHO) "$(YELLOW)$(WARN_ICON) Correctness tests not yet implemented!$(RESET)"

test/functional: test/performance test/correctness ## run all functional tests

test/pyunit: test_reports ## run python unit tests with reports
	@$(ECHO) "$(BOLD)$(TEST_ICON) Running Python Unit Tests...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Test log: $(LOG_DIR)/pytest_unit_$(TIMESTAMP).log$(RESET)"
	pytest -m "unit" \
		--junitxml=$(TEST_REPORTS_DIR)/pytest-unit-results.xml \
		--cov=vajra \
		--cov-report=xml:$(TEST_REPORTS_DIR)/python_coverage.xml \
		--cov-report=html:$(TEST_REPORTS_DIR)/python_coverage_html \
		2>&1 | tee "$(LOG_DIR)/pytest_unit_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Python unit tests complete$(RESET)"

test/pyintegration: test_reports ## run python integration tests with reports
	@$(ECHO) "$(BOLD)$(TEST_ICON) Running Python Integration Tests...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Test log: $(LOG_DIR)/pytest_integration_$(TIMESTAMP).log$(RESET)"
	pytest -m "integration" \
		--junitxml=$(TEST_REPORTS_DIR)/pytest-integration-results.xml \
		--cov=vajra --cov-append \
		--cov-report=xml:$(TEST_REPORTS_DIR)/python_coverage.xml \
		--cov-report=html:$(TEST_REPORTS_DIR)/python_coverage_html \
		2>&1 | tee "$(LOG_DIR)/pytest_integration_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) Python integration tests complete$(RESET)"

test/ctest: test_reports build/native_test ## run C++ tests (ctest) with reports
	@$(ECHO) "$(BOLD)$(TEST_ICON) Running C++ Tests (CTest)...$(RESET)"
	@$(ECHO) "$(BLUE)$(INFO_ICON) Test log: $(LOG_DIR)/ctest_$(TIMESTAMP).log$(RESET)"
	@(cd $(BUILD_DIR) && \
	ctest -R "kernel_tests|native_tests" \
		--output-on-failure \
		--timeout 180 \
		--test-dir . \
		--output-junit ../$(TEST_REPORTS_DIR)/ctest-results.xml \
	) 2>&1 | tee "$(LOG_DIR)/ctest_$(TIMESTAMP).log"
	@$(ECHO) "$(GREEN)$(SUCCESS_ICON) C++ tests complete$(RESET)"

test/unit: test/pyunit test/ctest ## run all unit tests (py + C++)
	@$(ECHO) "$(GREEN)$(TEST_ICON) All Unit Tests Passed $(PARTY_ICON)$(RESET)"

test/integration: test/pyintegration ## run all integration tests (py)
	@$(ECHO) "$(GREEN)$(TEST_ICON) All Integration Tests Passed $(PARTY_ICON)$(RESET)"

test: test/unit test/integration test/functional ## run all tests
	@$(ECHO) "$(BOLD)$(GREEN)$(TEST_ICON) All Tests Completed Successfully! $(PARTY_ICON)$(RESET)"


# --- Cleaning ---

clean: docs/clean ## clean build artifacts, logs, caches
	@$(ECHO) "$(YELLOW) $(WARN_ICON) This will remove: $(BUILD_DIR)/ dist/ $(TEST_REPORTS_DIR)/ $(LOG_DIR)/ *.so *.egg-info coverage files python cache...$(RESET)"
	@read -p "$(BOLD)Are you sure? [y/N] $(RESET)" confirm && \
		[[ $$confirm == [yY] || $$confirm == [yY][eE][sS] ]] || \
		( $(ECHO) "$(RED)Aborted.$(RESET)"; exit 1 )
	@$(ECHO) "$(BOLD)$(CLEAN_ICON) Cleaning Project Artifacts...$(RESET)"
	@rm -rf $(BUILD_DIR) \
	       dist \
	       vajra/*.so \
	       *.egg-info \
	       $(TEST_REPORTS_DIR) \
	       $(LOG_DIR) \
	       .coverage* \
	       coverage.xml \
	       python_coverage.xml \
	       python_coverage_html \
	       .pytest_cache \
	       .pyright_cache
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -exec rm -rf {} +
	@$(ECHO) "$(GREEN)$(CLEAN_ICON) Clean complete $(SUCCESS_ICON)$(RESET)"

# --- Help ---

help: ## show this help message
	@$(ECHO) "$(BOLD)Vajra Project Makefile$(RESET) $(PARTY_ICON)"
	@$(ECHO) "Usage: $(CYAN)make [TARGET] [VARIABLE=value]...$(RESET)"
	@$(ECHO) "$(BOLD)Common Targets:$(RESET)"
	@grep -E '^[^.#_%][a-zA-Z0-9_/.-]+:.*?## ' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "  $(CYAN)%-28s$(RESET) %s\n", $$1, $$2}'
	@$(ECHO) "$(BOLD)Examples:$(RESET)"
	@$(ECHO) "  $(CYAN)make lint$(RESET)"
	@$(ECHO) "  $(CYAN)make test$(RESET)"
	@$(ECHO) "  $(CYAN)make build BUILD_TYPE=Release$(RESET)"
	@$(ECHO) "  $(CYAN)make clean$(RESET)"
