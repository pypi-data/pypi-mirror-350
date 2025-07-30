ARG CUDA_VERSION=12.4.1
ARG PYTORCH_VERSION=2.6

# Start with the same base image as your workflow
FROM nvidia/cuda:${CUDA_VERSION}-cudnn-devel-ubuntu22.04

# Set environment variables
ENV VAJRA_CI_CUDA_VERSION=${CUDA_VERSION%.*}
ENV VAJRA_CI_TORCH_VERSION=${PYTORCH_VERSION}

# Copy the entire repository into the image
COPY . /repo
WORKDIR /repo

# Run the setup script (ideally, inline these commands for better practice)
# Assumption: setup_env.sh installs dependencies like Python, pip, git
RUN bash /repo/scripts/ci/setup_env.sh

# Build Vajra
RUN bash /repo/scripts/ci/build_vajra.sh

# Build vLLM
RUN bash /repo/scripts/ci/build_vllm.sh

# Build SGLang
RUN bash /repo/scripts/ci/build_sgl.sh

# Build MLC-LLM
RUN bash /repo/scripts/ci/build_mlc.sh

# Include the generated ENV commands
RUN rm -rf /tmp/repo

LABEL org.opencontainers.image.title="Vajra Nightly Performance Test Container"
LABEL org.opencontainers.image.description="Vajra container for performance testing. CUDA ${CUDA_VERSION} with PyTorch ${PYTORCH_VERSION}"
LABEL org.opencontainers.image.vendor="Vajra Team"
LABEL org.opencontainers.image.cuda.version="${CUDA_VERSION}"
LABEL org.opencontainers.image.pytorch.version="${PYTORCH_VERSION}"