# !/usr/bin/python3
# -*- coding:utf-8 -*-
# Author:WeiFeng Liu
# @Time: 2021/11/4 下午2:38

##读入文件，显示正确分类和预测分类
import matplotlib.pyplot as plt
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
from GoogLeNet import my_Googlenet

transform = transforms.Compose([
    transforms.Resize([299,299]),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    # transforms.Normalize(mean=[.5,.5,.5],std=[.5,.5,.5]),
    ])


file_name = input("输入要预测的文件名：")
img = Image.open(file_name).convert("RGB")
show_img = img
img = transform(img)
#
# print(img)
# print(img.shape)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
img = img.to(device)
img = img.unsqueeze(0)
net = my_Googlenet().to(device)
net.load_state_dict(torch.load(r'model/pretrain/epoch200.pth'))

pred = net(img)
print(pred)
print(pred.argmax(dim = 1).cpu().numpy()[0])
res = ''
if pred.argmax(dim = 1) == 0:
    res += 'pred:no_covid'
else:
    res += 'pred:covid'

plt.figure("Predict")
plt.imshow(show_img)
plt.axis("off")
plt.title(res)
plt.show()
