import datetime
from tqdm import tqdm
from typing import List

from vajra.config import (
    ModelConfig,
    ParallelConfig,
    MetricsConfig,
    LlmReplicaControllerConfig,
    LlmReplicasetControllerConfig,
    InferenceEngineConfig,
    WorkerConfig,
    FixedChunkReplicaSchedulerConfig,
)
from vajra.datatypes import RequestOutput, SamplingParams
from vajra.engine.inference_engine import InferenceEngine


BASE_OUTPUT_DIR = "./offline_inference_output"

# Sample prompts.
prompts = [
    "The breakthrough technique developed by University of Oxford researchers could one day provide tailored repairs for those who suffer brain injuries. The researchers demonstrated for the first time that neural cells can be 3D printed to mimic the architecture of the cerebral cortex. The results have been published today in the journal Nature Communications. Brain injuries, including those caused by trauma, stroke and surgery for brain tumours, typically result in significant damage to the cerebral cortex (the outer layer of the human brain), leading to difficulties in cognition, movement and communication. For example, each year, around 70 million people globally suffer from traumatic brain injury (TBI), with 5 million of these cases being severe or fatal. Currently, there are no effective treatments for severe brain injuries, leading to serious impacts on quality of life. Tissue regenerative therapies, especially those in which patients are given implants derived from their own stem cells, could be a promising route to treat brain injuries in the future. Up to now, however, there has been no method to ensure that implanted stem cells mimic the architecture of the brain.",
    "The immediate reaction in some circles of the archeological community was that the accuracy of our dating was insufficient to make the extraordinary claim that humans were present in North America during the Last Glacial Maximum. But our targeted methodology in this current research really paid off, said Jeff Pigati, USGS research geologist and co-lead author of a newly published study that confirms the age of the White Sands footprints. The controversy centered on the accuracy of the original ages, which were obtained by radiocarbon dating. The age of the White Sands footprints was initially determined by dating seeds of the common aquatic plant Ruppia cirrhosa that were found in the fossilized impressions. But aquatic plants can acquire carbon from dissolved carbon atoms in the water rather than ambient air, which can potentially cause the measured ages to be too old. Even as the original work was being published, we were forging ahead to test our results with multiple lines of evidence, said Kathleen Springer, USGS research geologist and co-lead author on the current Science paper. We were confident in our original ages, as well as the strong geologic, hydrologic, and stratigraphic evidence, but we knew that independent chronologic control was critical.",
    "The president of the United States is",
    "The capital of France is",
    "The breakthrough technique developed by University of Oxford researchers could one day provide tailored repairs for those who suffer brain injuries. The researchers demonstrated for the first time that neural cells can be 3D printed to mimic the architecture of the cerebral cortex. The results have been published today in the journal Nature Communications. Brain injuries, including those caused by trauma, stroke and surgery for brain tumours, typically result in significant damage to the cerebral cortex (the outer layer of the human brain), leading to difficulties in cognition, movement and communication. For example, each year, around 70 million people globally suffer from traumatic brain injury (TBI), with 5 million of these cases being severe or fatal. Currently, there are no effective treatments for severe brain injuries, leading to serious impacts on quality of life. Tissue regenerative therapies, especially those in which patients are given implants derived from their own stem cells, could be a promising route to treat brain injuries in the future. Up to now, however, there has been no method to ensure that implanted stem cells mimic the architecture of the brain.",
    "Hydrogen ions are the key component of acids, and as foodies everywhere know, the tongue senses acid as sour. That's why lemonade (rich in citric and ascorbic acids), vinegar (acetic acid) and other acidic foods impart a zing of tartness when they hit the tongue. Hydrogen ions from these acidic substances move into taste receptor cells through the OTOP1 channel. Because ammonium chloride can affect the concentration of acid -- that is, hydrogen ions -- within a cell, the team wondered if it could somehow trigger OTOP1. To answer this question, they introduced the Otop1 gene into lab-grown human cells so the cells produce the OTOP1 receptor protein. They then exposed the cells to acid or to ammonium chloride and measured the responses. We saw that ammonium chloride is a really strong activator of the OTOP1 channel, Liman said. It activates as well or better than acids. Ammonium chloride gives off small amounts of ammonia, which moves inside the cell and raises the pH, making it more alkaline, which means fewer hydrogen ions.",
]
# Create a sampling params object.
sampling_params = SamplingParams(temperature=1, top_p=0.5, max_tokens=100)

output_dir = f"{BASE_OUTPUT_DIR}/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

model_config = ModelConfig(
    model="Groq/Llama-3-Groq-8B-Tool-Use",
)

parallel_config = ParallelConfig(
    tensor_parallel_size=1,
    pipeline_parallel_size=1,
    kv_parallel_size=1,
    max_num_tokens_per_kvp_group=160,
    enable_sequence_pipeline_parallel=False,
)

scheduler_config = FixedChunkReplicaSchedulerConfig(
    chunk_size=80,
)

metrics_config = MetricsConfig(
    write_metrics=True,
    enable_chrome_trace=True,
    enable_cpu_op_level_metrics=True,
    output_dir=output_dir,
)

worker_config = WorkerConfig(
    use_native_execution_backend=True,
)

replica_controller_config = LlmReplicaControllerConfig(
    model_config=model_config,
    parallel_config=parallel_config,
    scheduler_config=scheduler_config,
    worker_config=worker_config,
)

replicaset_controller_config = LlmReplicasetControllerConfig(
    num_replicas=1,
    replica_controller_config=replica_controller_config,
)

# Create an InferenceEngineConfig with the LlmReplicaControllerConfig
engine_config = InferenceEngineConfig(
    controller_config=replicaset_controller_config,
    metrics_config=metrics_config,
)

# Pass the engine_config to the InferenceEngine
engine = InferenceEngine(engine_config)

def generate(
    engine: InferenceEngine,
    prompts: List[str],
    sampling_params: SamplingParams,
) -> List[RequestOutput]:
    for prompt in prompts:
        engine.add_request(prompt, sampling_params)

    pbar = tqdm(total=len(prompts), desc="Processed prompts")

    # Run the engine
    outputs: List[RequestOutput] = []
    while len(outputs) < len(prompts):
        step_outputs = engine.get_outputs()
        for output in step_outputs:
            if output.finished:
                outputs.append(output)
                pbar.update(1)

    pbar.close()
    # Sort the outputs by request ID.
    outputs = sorted(outputs, key=lambda x: int(x.request_id))
    return outputs

engine.reset_metrics()

# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.
outputs = generate(engine, prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.text
    print("===========================================================")
    print(f"Prompt: {prompt!r}")
    print("-----------------------------------------------------------")
    print(f"Generated text: {generated_text!r}")
    print("===========================================================")

engine.plot_metrics()
