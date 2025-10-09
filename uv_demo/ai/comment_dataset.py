from torch.utils.data import Dataset
from datasets import load_from_disk


print(Dataset)


class CommentDataset:
    dataset_path="/home/zdz/Documents/Try/LLM/course/uv_demo/ai/datasets/herbal"
    dataset=None
    # 初始化数据
    def __init__(self, split=None):
        self.dataset = load_from_disk(self.dataset_path)
        # print(self.dataset)
        # print(dataset['category'])
        # if split == "id":
        #     self.dataset = dataset['id']
        # elif split == "category": 
        #     self.dataset = dataset['category']
        # elif split == "task": 
        #     self.dataset = dataset['task']


    # 获取数据长度
    def __len__(self):
        return len(self.dataset)
    # 处理数据
    def __getitem__(self, index):
        text = self.dataset[index]["review_text"]
        label = self.dataset[index]["sentiment_label"]
        rating = self.dataset[index]["rating"]
        return text, label, rating
        
        




if __name__ == "__main__":
    dataset = CommentDataset()
    print(dataset)
    for data in dataset:
        print(data)

