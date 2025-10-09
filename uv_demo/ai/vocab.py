from transformers import BertTokenizer


model_dir = "/home/zdz/.cache/huggingface/hub/models--google-bert--bert-base-chinese/snapshots/8f23c25b06e129b6c986331a13d8d025a92cf0ea"
token = BertTokenizer.from_pretrained(model_dir)
# print(token)

vocab = token.get_vocab()
# print(vocab)


print("中" in vocab)
print("𰻝" in vocab)

token.add_tokens(["𰻝"])
vocab = token.get_vocab()
print(len(vocab))
print("𰻝" in vocab)
print(vocab)
