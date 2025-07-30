ARG CUDA_VERSION=12.4.1

FROM nvidia/cuda:${CUDA_VERSION}-cudnn-devel-ubuntu22.04

ARG PYTORCH_VERSION=2.6

# Set environment variables
ENV VAJRA_CI_CUDA_VERSION=${CUDA_VERSION%.*}
ENV VAJRA_CI_TORCH_VERSION=${PYTORCH_VERSION}

# Set up working directory
WORKDIR /repo

# Copy everything from the repo home directory
COPY . /tmp/repo

# Make scripts executable
RUN chmod +x /tmp/repo/scripts/ci/setup/*.sh

# Install base dependencies
RUN /tmp/repo/scripts/ci/setup/install_base.sh

# Install Mamba
RUN /tmp/repo/scripts/ci/setup/install_mamba.sh

# Install ZSH and related components
RUN /tmp/repo/scripts/ci/setup/install_zsh.sh

# Install the pip requirements
RUN /tmp/repo/scripts/ci/setup/install_pip_requirements.sh

# Clean up
RUN rm -rf /tmp/repo

# Set default shell to zsh
SHELL ["/bin/zsh", "-c"]
CMD ["zsh"]

# Add labels
LABEL org.opencontainers.image.title="Vajra Development Container"
LABEL org.opencontainers.image.description="CUDA ${CUDA_VERSION} with PyTorch ${PYTORCH_VERSION} for Vajra development"
LABEL org.opencontainers.image.vendor="Vajra Team"
LABEL org.opencontainers.image.cuda.version="${CUDA_VERSION}"
LABEL org.opencontainers.image.pytorch.version="${PYTORCH_VERSION}"

