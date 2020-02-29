import sys
import os
import json

from tqdm import tqdm
import cv2
import numpy as np
import torch
import torchvision
from torchvision import transforms, models

if __name__ == '__main__':

    backbone_name = sys.argv[1]
    data_path = sys.argv[2]
    dest_path = sys.argv[3]

    with open("imagenet_class_index.json") as f:
        class_idx = json.load(f)
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

    backbone = getattr(models, backbone_name)
    net = backbone(pretrained=True).cuda()

    batch_size = 128
    normalize = transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
    transform =  transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            normalize,
        ])

    image_data = torchvision.datasets.ImageFolder(data_path, transform=transform)
    data_loader = torch.utils.data.DataLoader(image_data, batch_size=128)

    for batch in tqdm(data_loader):
        batch_images, batch_labels = batch
        batch_images = batch_images.cuda()
        with torch.no_grad():
            batch_predictions = net(batch_images)
            _, max_predictions = torch.max(batch_predictions, dim=1)
            break

