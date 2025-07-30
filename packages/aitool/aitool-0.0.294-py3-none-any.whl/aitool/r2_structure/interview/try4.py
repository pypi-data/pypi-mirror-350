# -*- coding: UTF-8 -*-
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os


# 自定义数据集类
class ImageClassificationDataset(Dataset):
    def __init__(self, image_dir, labels, processor):
        self.image_dir = image_dir
        self.labels = labels
        self.processor = processor
        self.image_files = []
        self.image_labels = []
        for label in labels:
            label_dir = os.path.join(image_dir, label)
            for file in os.listdir(label_dir):
                self.image_files.append(os.path.join(label_dir, file))
                self.image_labels.append(label)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image = Image.open(self.image_files[idx]).convert("RGB")
        label = self.image_labels[idx]
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        text_inputs = self.processor(text=label, return_tensors="pt", padding=True)
        return {
            "image_inputs": {k: v.squeeze(0) for k, v in inputs.items()},
            "text_inputs": {k: v.squeeze(0) for k, v in text_inputs.items()},
            "label": self.labels.index(label)
        }


# 训练函数
def train_clip(model, processor, train_dataloader, optimizer, device, epochs):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch in train_dataloader:
            image_inputs = {k: v.to(device) for k, v in batch["image_inputs"].items()}
            text_inputs = {k: v.to(device) for k, v in batch["text_inputs"].items()}
            labels = batch["label"].to(device)

            optimizer.zero_grad()
            outputs = model(**image_inputs, **text_inputs)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_dataloader)}")


# 主函数
def main():
    # 初始化模型和处理器
    model_name = "openai/clip-vit-base-patch16"
    model = CLIPModel.from_pretrained(model_name)
    processor = CLIPProcessor.from_pretrained(model_name)

    # 定义数据集路径和标签
    image_dir = "path/to/your/dataset"
    labels = ["class1", "class2", "class3"]  # 替换为实际的类别标签

    # 创建数据集和数据加载器
    dataset = ImageClassificationDataset(image_dir, labels, processor)
    train_dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    # 设备设置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 定义优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

    # 训练模型
    epochs = 5
    train_clip(model, processor, train_dataloader, optimizer, device, epochs)


if __name__ == "__main__":
    main()

