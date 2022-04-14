---
title: FaceNet人脸检测
date: 2022-03-21 10:58:05
tags:
 - CV
categories:
 -CV
---

# 人脸识别的流程

1. 人脸分割：从一张图中抠出来人脸的部分

2. 特征提取：从第一步得到人脸提取特征

3. 人脸分类：训练一个分类器来判断人脸是哪一张人脸

## 人脸分割

人脸分割是一个目标检测的任务。比较流行的方法有：
- yolov5
- mtcnn

## 特征提取

可以用迁移学习，同预训练模型来提取特征，比如：
- facanet

> facenet是基于resnet的，针对人脸所做的预训练模型

## 人脸分类

分类任务，常见的分类算法都可以：

- SVM
- KNN
- MLP


# 示例代码

TODO

# 参考链接
- yolov5face. https://github.com/deepcam-cn/yolov5-face
- facenet_pytorch简介. https://blog.csdn.net/zhonglongshen/article/details/117995211
- 基于yolov5的人脸识别. https://windfill.gitee.io/article/2391c58c.html
- 

