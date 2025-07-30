.. vajra documentation master file, created by
   sphinx-quickstart on Friday Feb 14 14:40:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Vajra
=====

   The second-wave lean distributed low-latency LLM inference serving engine.

Check out the following resources to get started:

.. toctree::
   :maxdepth: 2

   installation
   contributing/contributing


Citation
--------
If you use `vajra` in your research, please cite the following papers:

.. code-block:: bibtex

   @article{agrawal2024mnemosyne,
      title={Mnemosyne: Parallelization strategies for efficiently serving multi-million context length llm inference requests without approximations},
      author={Agrawal, Amey and Chen, Junda and Goiri, {\'I}{\~n}igo and Ramjee, Ramachandran and Zhang, Chaojie and Tumanov, Alexey and Choukse, Esha},
      journal={arXiv preprint arXiv:2409.17264},
      year={2024}
   }

   @article{agrawal2024taming,
      title={Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve},
      author={Agrawal, Amey and Kedia, Nitin and Panwar, Ashish and Mohan, Jayashree and Kwatra, Nipun and Gulavani, Bhargav S and Tumanov, Alexey and Ramjee, Ramachandran},
      journal={Proceedings of 18th USENIX Symposium on Operating Systems Design and Implementation, 2024, Santa Clara},
      year={2024}
   }

Acknowledgement
---------------
`Vajra <https://github.com/project-vajra/vajra>`_ code is being actively developed by the `Systems for AI Lab <https://gatech-sysml.github.io/>`_ at Georgia Tech, and a lot of code has been adopted from `vLLM <https://blog.vllm.ai/>`_ and `SGLang <https://github.com/sgl-project/sglang>`_.
