from datasets import load_dataset, load_from_disk

dataset_remote = "OpenModels/Chinese-Herbal-Medicine-Sentiment"
dataset_local = "/home/zdz/Documents/Try/LLM/course/uv_demo/ai/datasets/herbal"
dataset = None
try:
    dataset = load_from_disk(dataset_local)
except FileNotFoundError as err:
    print(str(err))
    dataset = load_dataset(path=dataset_remote, split="train")
    dataset.save_to_disk(dataset_local)


print(dataset)

for i in range(10):
    data = dataset[i]
    print(data["rating"], data["review_text"])

# for data in dataset:
#     print(data["review_text"])
