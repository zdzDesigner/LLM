from transformers import BertModel
import torch



DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(DEVICE)

# model = BertModel.from_pretrained("/home/zdz/.cache/huggingface/hub/models--google-bert--bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")
pretrained = model.to(DEVICE)

print(pretrained)
