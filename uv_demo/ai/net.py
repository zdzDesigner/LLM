from transformers import BertModel
import torch



DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(DEVICE)

# model = BertModel.from_pretrained("/home/zdz/.cache/huggingface/hub/models--google-bert--bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")
pretrained = model.to(DEVICE)

# print(pretrained)

class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(in_features=768, out_features=2)
    
    def forward(self, input_ids,attention_mask,token_type_ids):
        # 上游模型自身不训练，参与前向训练
        with torch.no_grad():
            out = pretrained(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        
        # 下游任务参与训练
        out = self.fc(out.last_hidden_state[:,0])
        out = out.softmax(dim=1)
        return out


