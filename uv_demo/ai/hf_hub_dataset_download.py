from huggingface_hub import snapshot_download
from datasets import load_dataset, load_from_disk, Dataset, DatasetDict


# 从 huggingface 下载并存储在指定磁盘
# dataset = load_dataset(path="NousResearch/hermes-function-calling-v1", split="train")
# dataset.save_to_disk("/home/zdz/Documents/Try/LLM/course/uv_demo/ai/datasets/hermes-function-calling-v1")


dataset = None
try:
    # dataset = load_from_disk(dataset_path="/home/zdz/.cache/huggingface/hub/datasets--NousResearch--hermes-function-calling-v1/snapshots/8f025148382537ba84cd325e1834b706e1461692")
    dataset = load_from_disk(dataset_path="/home/zdz/Documents/Try/LLM/course/uv_demo/ai/datasets/hermes-function-calling-v1")
    if isinstance(dataset, DatasetDict):
        print("DatasetDict")
    elif isinstance(dataset, Dataset):
        print("Dataset")

except FileNotFoundError as e:
    error_msg = str(e)
    print(f"错误信息：{error_msg}")


print(f"{dataset}")

for data in dataset:
    print(data["id"])



# OpenModels/Chinese-Herbal-Medicine-Sentiment
