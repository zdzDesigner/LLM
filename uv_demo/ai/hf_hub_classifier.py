from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification

# 加载模型和分词器
model_dir = "/home/zdz/.cache/huggingface/hub/models--google-bert--bert-base-chinese/snapshots/8f23c25b06e129b6c986331a13d8d025a92cf0ea"
model = BertForSequenceClassification.from_pretrained(model_dir)
tokenizer = BertTokenizer.from_pretrained(model_dir)


# 创建分类
classier = pipeline('text-classification', model=model, tokenizer=tokenizer)


# 分类
# res = classier("你好, 今天很糟糕")
res = classier("你好, 今天高兴")
print(f"{res}")
