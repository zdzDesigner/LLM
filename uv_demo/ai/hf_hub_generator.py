import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


model_dir = (
    "/home/zdz/Documents/Try/LLM/course/demo1/model/uer/gpt2-chinese-cluecorpussmall/models--uer--gpt2-chinese-cluecorpussmall/snapshots/c2c0249d8a2731f269414cc3b22dff021f8e07a3"
)

model = AutoModelForCausalLM.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)


# # generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device="cuda")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device="cuda" if torch.cuda.is_available() else "cpu")
#
# # 1 =============
# output = generator("你好，今天天气不错，", max_length=150, num_return_sequences=1, temperature=0.7, top_k=10, top_p=0.99, clean_up_tokenization_spaces=True)
# print(output)


# # 2 =============


long_prompt = "你好，今天天气不错，"
output = generator(
    long_prompt,
    max_length=150,  # 生成的最大长度
    num_return_sequences=2,  # 返回数量
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    clean_up_tokenization_spaces=False,
)

print("生成输出（提示已截断）:", output[0]["generated_text"])
print(f"output:{output}")

# 示例2: 手动使用tokenizer设置truncation，然后传入pipeline（pipeline内部会使用）
inputs = tokenizer(
    long_prompt,
    truncation=True,  # 显式启用截断
    max_length=30,  # 截断到30个token
    padding=True,
    return_tensors="pt",
)
print("手动截断后的输入长度:", len(inputs["input_ids"][0]))

# 由于pipeline接受文本，我们可以直接用截断后的文本（但实际中pipeline会自动处理）
truncated_prompt = tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)
output_manual = generator(truncated_prompt, max_length=100, num_return_sequences=1, temperature=0.7, top_k=50, top_p=0.9)
print("基于手动截断提示的生成输出:", output_manual[0]["generated_text"])
