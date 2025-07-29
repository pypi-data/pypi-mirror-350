# Vajra Development Container

This container provides a consistent development environment with CUDA and PyTorch support, along with useful developer tools. It's designed to match the CI environment for building and testing Vajra.

## Features

- CUDA support with cuDNN
- PyTorch with CUDA support
- Miniforge (faster Conda alternative)
- ZSH with Oh My Zsh and Powerlevel10k theme
- FZF (fuzzy finder) for enhanced command-line navigation
- Development tools (git, vim, nano, etc.)
- Similar environment to CI pipelines for consistent development and testing

## Available Tags

Images are tagged with the CUDA and PyTorch versions:

- `ghcr.io/project-vajra/vajra-dev:cuda12.4.1-torch2.6`
- And more as needed

## Building the Container

### Using Make (Recommended)

```bash
# From this directory
make build

# With specific versions
make build CUDA_VERSION=11.8 PYTORCH_VERSION=2.0
```

## Running the Container

```bash
# Run with default versions
make run

# Run with specific versions
make run CUDA_VERSION=11.8 PYTORCH_VERSION=2.0
```

