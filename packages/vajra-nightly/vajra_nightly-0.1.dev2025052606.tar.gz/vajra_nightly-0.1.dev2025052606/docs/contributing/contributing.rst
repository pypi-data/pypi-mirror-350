Contributing
============

This section contains developer guides to enable you to effectively contribute to the project. The guides cover the coding style, the development process, and the tools used in the project.

Setup
-----
Setup CUDA
~~~~~~~~~~
Vajra has been tested with CUDA 12.6 on A100 and H100 GPUs.

Clone repository
~~~~~~~~~~~~~~~~

.. code-block:: shell

    git clone --recursive -j8 https://github.com/project-vajra/vajra

Create mamba Environment
~~~~~~~~~~~~~~~~~~~~~~~~
Setup mamba if you don't already have it,

.. code-block:: shell

    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
    bash Miniforge3-Linux-x86_64.sh # follow the instructions from there

Create a Python 3.12 environment with cmake,

.. code-block:: shell

    mamba env create -f environment-dev.yml -p ./env

Activate the environment,

.. code-block:: shell

    mamba activate ./env

Install Vajra
~~~~~~~~~~~~~

.. code-block:: shell

    make build

Incremental C++ Builds
^^^^^^^^^^^^^^^^^^^^^^

To perform incremental native builds, use the following commands:

.. code-block:: shell

    make build_native_incremental

Linting & formatting
~~~~~~~~~~~~~~~~~~~~

For linting code,

.. code-block:: shell

    make lint

You can simplify life by performing auto-formatting,

.. code-block:: shell

    make format

Check out the following guides to learn more:

.. toctree::
   :maxdepth: 1

   style_guides/cpp_style_guide
   testing/writing_python_tests
