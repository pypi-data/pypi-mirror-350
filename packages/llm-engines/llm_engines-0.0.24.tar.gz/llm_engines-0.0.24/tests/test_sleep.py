import time
from llm_engines import LLMEngine
model_name="meta-llama/Meta-Llama-3-8B-Instruct"
llm = LLMEngine()
llm.load_model(
    model_name=model_name,
    num_workers=1, # number of workers
    num_gpu_per_worker=1, # tensor parallelism size for each worker
    engine="vllm", # or "sglang"
    use_cache=False
)
response = llm.call_model(model_name, "What is the capital of France?", temperature=0.0, max_tokens=None)
print(response)
llm.sleep_model(model_name)
time.sleep(20)
# wake up the model when calling it again if the model is in sleep mode
response = llm.call_model(model_name, "What is the capital of France?", temperature=0.0, max_tokens=None)

