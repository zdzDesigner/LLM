import torch
from net import Model  # 导入训练时的模型类（必须与训练时定义一致）
from transformers import BertTokenizer

# 1. 设备配置（优先GPU）
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. 加载预训练Tokenizer（必须与训练时一致）
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

# 3. 实例化模型并加载权重
model = Model().to(DEVICE)  # 初始化模型（结构必须和训练时一样）
model.load_state_dict(
    torch.load("train_res/0_bert.pt", map_location=DEVICE)  # 加载训练好的权重
)
model.eval()  # 切换到「评估模式」（关闭Dropout/BatchNorm的随机性）


def single_predict(text, model, tokenizer, device):
    """
    单条文本预测
    :param text: 输入文本（如评论）
    :param model: 加载权重的模型
    :param tokenizer: BERT Tokenizer
    :param device: 设备（CPU/GPU）
    :return: 预测的类别（整数，对应训练时的标签）
    """
    # 1. 文本编码（必须与训练时的collate_fn一致）
    encoded = tokenizer.batch_encode_plus(
        [text],  # 单条文本用列表包裹
        truncation=True,  # 截断过长文本
        padding="max_length",  # 填充到最大长度
        max_length=300,  # 与训练时的max_length一致
        return_tensors="pt",  # 返回PyTorch Tensor
    )

    # 2. 将编码后的数据移动到设备
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)
    token_type_ids = encoded["token_type_ids"].to(device)

    # 3. 推理（不计算梯度，节省内存）
    with torch.no_grad():
        outputs = model(input_ids, attention_mask, token_type_ids)

    # 4. 解析结果：取概率最大的类别
    pred_label = outputs.argmax(dim=1).cpu().item()  # 转回CPU并转成整数

    return pred_label


def batch_predict(texts, model, tokenizer, device):
    """
    批量文本预测
    :param texts: 输入文本列表（如["评论1", "评论2", ...]）
    :return: 预测类别列表（与输入顺序一致）
    """
    # 1. 批量编码文本
    encoded = tokenizer.batch_encode_plus(
        texts,
        truncation=True,
        padding="longest",  # 批量填充到最长文本长度（更高效）
        return_tensors="pt",
    )

    # 2. 移动到设备
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)
    token_type_ids = encoded["token_type_ids"].to(device)

    # 3. 推理
    with torch.no_grad():
        outputs = model(input_ids, attention_mask, token_type_ids)

    # 4. 解析结果
    pred_labels = outputs.argmax(dim=1).cpu().tolist()  # 转成Python列表

    return pred_labels


if __name__ == "__main__":
    # 单条预测
    text = "这个手机充电很快，拍照清晰，非常满意！"
    pred = single_predict(text, model, tokenizer, DEVICE)
    print(f"文本：{text} 预测类别：{pred}（0=负面，1=正面）")

    # 批量预测
    texts = [
        "物流很快，包装完好，商品符合预期。",
        "质量太差了，用了一天就坏了，差评！",
        "客服态度恶劣，再也不买了。",
        "质量不错。",
    ]
    preds = batch_predict(texts, model, tokenizer, DEVICE)
    for text, pred in zip(texts, preds):
        print(f"文本：{text} 预测类别：{pred} ")
