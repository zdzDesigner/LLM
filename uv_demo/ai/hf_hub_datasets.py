import huggingface_hub
from huggingface_hub import HfApi

print(huggingface_hub.__version__)

# 初始化 API
api = HfApi()

# 创建过滤字典：语言为中文，且数据集样本数小于 10K
filt = {
    "languages": "zh",  # 中文
    # "size_categories": "0<n<100K"  # 小数据集（可调整为 "10K<n<100K" 等）
}

# 列出符合条件的中文小数据集
small_chinese_datasets = api.list_datasets(filter=filt)

print(len(list(small_chinese_datasets)))
# 打印结果（例如数据集 ID）
print("小中文数据集列表：")
for dataset in list(small_chinese_datasets)[:10]:  # 只显示前 10 个，避免输出过多
    print(dataset)
    # print(f"- {dataset.id}")
