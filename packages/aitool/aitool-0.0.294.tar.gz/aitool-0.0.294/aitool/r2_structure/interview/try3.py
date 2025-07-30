# -*- coding: UTF-8 -*-
import torch
from torch.utils.data import DataLoader
from datasets import load_dataset
from transformers import CLIPProcessor, CLIPModel
from transformers import AdamW
import tqdm

# 加载数据集
# 这里以Hugging Face的示例数据集为例，你可以替换为自己的数据集
dataset = load_dataset("hf-internal-testing/fixtures_clip")

# 加载CLIP模型和处理器
model_name = "openai/clip-vit-base-patch16"
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)


# 定义数据处理函数
def preprocess_function(examples):
    images = examples["image"]
    texts = examples["text"]
    inputs = processor(text=texts, images=images, return_tensors="pt", padding=True)
    return inputs


# 处理数据集
processed_dataset = dataset.map(preprocess_function, batched=True)
processed_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'pixel_values'])

# 创建数据加载器
train_dataloader = DataLoader(processed_dataset["train"], batch_size=2, shuffle=True)

# 定义优化器
optimizer = AdamW(model.parameters(), lr=5e-5)

# 训练循环
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in tqdm.tqdm(train_dataloader):
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
    print(f"Epoch {epoch + 1}: Loss = {total_loss / len(train_dataloader)}")

# 保存微调后的模型
model.save_pretrained("fine_tuned_clip")
processor.save_pretrained("fine_tuned_clip")
