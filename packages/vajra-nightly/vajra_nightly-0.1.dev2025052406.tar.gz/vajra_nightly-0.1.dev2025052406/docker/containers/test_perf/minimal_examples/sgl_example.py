from sglang.test.test_utils import is_in_ci
from sglang.utils import wait_for_server, print_highlight, terminate_process

if is_in_ci():
    from patch import launch_server_cmd
else:
    from sglang.utils import launch_server_cmd

# This is equivalent to running the following command in your terminal

# python -m sglang.launch_server --model-path meta-llama/Meta-Llama-3.1-8B-Instruct --host 0.0.0.0

server_process, port = launch_server_cmd(
    """
python -m sglang.launch_server --model-path meta-llama/Meta-Llama-3.1-8B-Instruct \
 --host 0.0.0.0
"""
)

wait_for_server(f"http://localhost:{port}")

import requests

url = f"http://localhost:{port}/v1/chat/completions"

data = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
}

response = requests.post(url, json=data)
print_highlight(response.json())