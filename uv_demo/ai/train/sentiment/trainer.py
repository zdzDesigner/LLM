import os
import torch
from comment_dataset import CommentDataset
from torch.utils.data import DataLoader
from net import Model
from transformers import BertTokenizer
from torch.optim import AdamW
# from transformers.optimization import Adafactor
# print(AdamW)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EPOCH = 1

token = BertTokenizer.from_pretrained("bert-base-chinese")


# 处理数据编码
def collate_fn(data):
    sentes = [i[0] for i in data]
    label = [i[1] for i in data]
    # 编码
    data = token.batch_encode_plus(
        batch_text_or_text_pairs=sentes,
        truncation=True,
        padding="max_length",
        max_length=300,
        return_tensors="pt",
        return_length=True,
    )
    input_ids = data["input_ids"]
    attention_mask = data["attention_mask"]
    token_type_ids = data["token_type_ids"]
    labels = torch.LongTensor(label)
    return input_ids, attention_mask, token_type_ids, labels


# 创建数据集
train_dataset = CommentDataset()
# 创建数据加载器
train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=32,  # 每次传递8条数据，到collate_fn中编码
    shuffle=True,
    drop_last=True,
    collate_fn=collate_fn,
)


if __name__ == "__main__":
    os.makedirs("train_res", exist_ok=True)

    # 开始训练
    print(DEVICE)
    model = Model().to(DEVICE)  # 把模型放入设备
    optimizer = AdamW(model.parameters(), lr=5e-4)  # 优化器
    loss_func = torch.nn.CrossEntropyLoss()  # 损失函数

    model.train()  # 训练
    for epoch in range(EPOCH):
        for i, (input_ids, attention_mask, token_type_ids, labels) in enumerate(train_loader):
            # 将数据放到DEVICE上
            input_ids, attention_mask, token_type_ids, labels = input_ids.to(DEVICE), attention_mask.to(DEVICE), token_type_ids.to(DEVICE), labels.to(DEVICE)

            # 执行前向计算得到输出
            out = model(input_ids, attention_mask, token_type_ids)

            # print(f"Batch {i}: out.shape={out.shape}, labels.shape={labels.shape}")
            # print(f"Labels min={labels.min().item()}, max={labels.max().item()}, unique={torch.unique(labels)}")
            # print(f"Expected n_classes={out.shape[1]}")
            loss = loss_func(out, labels)

            optimizer.zero_grad()  # 清空梯度权重
            loss.backward()  # 反向传播
            optimizer.step()  # 更新梯度

            if i % 5 == 0:
                out = out.argmax(dim=1)  # 取结果: 解码
                acc = (out == labels).sum().item() / len(labels)  # 精度
                print(epoch, i, loss.item(), acc)

        # 保存模型
        torch.save(model.state_dict(), f"train_res/{epoch}_bert.pt")
        print(epoch, "OK")
