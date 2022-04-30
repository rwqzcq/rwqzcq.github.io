---
title: Keras做文本分类
date: 2021-11-18 22:53:30
tags:
 - 其他
categories:
 - 其他
---

使用原生的`IMDB`情感分析数据集来做。

# 1. 数据预处理

## 1.1 加载原始数据

```python

import re

def rm_tags(test):
    """
    去除HTML代码
    """
    re_tag = re.compile(r'<[^>]+>')
    return re_tag.sub('', test)

import os
def read_files(filetype):  # filetype取值为 'train' / 'test'
    path = "./dataset/aclImdb/"  # 数据集的路径
    file_list=[]  # 用于存放所有评价文件的文件名

    positive_path=path + filetype+"/pos/"  # 好评文件路径
    for f in os.listdir(positive_path):  
        file_list+=[positive_path+f]
    
    negative_path=path + filetype+"/neg/"
    for f in os.listdir(negative_path):
        file_list+=[negative_path+f]
        
    print('read',filetype, 'files:',len(file_list))
    
    # 创建标签，好评标签为1，差评为0
    # 由于先加载好评文件，因此先存放12500个1，再存放12500个0
    all_labels = ([1] * 12500 + [0] * 12500)  
    
    # 保存所有影评
    all_texts  = []
    for fi in file_list:
        # 中文编码utf8
        with open(fi,encoding='utf8') as file_input:
            # 将文本去html代码再保存
            all_texts += [rm_tags(" ".join(file_input.readlines()))] 
    # 返回标签和内容
    return all_labels,all_texts

y_train, train_text = read_files('train')  # 训练标签、训练数据
y_test, test_text = read_files('test')  # # 测试标签、测试数据

```

`train_text`的一个元素为:

`'For a movie that gets no respect there sure are a lot of memorable quotes listed for this gem. Imagine a movie where Joe Piscopo is actually funny! Maureen Stapleton is a scene stealer. The Moroni character is an absolute scream. Watch for Alan "The Skipper" Hale jr. as a police Sgt.'` 可以看到的是就是一个原生的句子，只不过是去除了HTML标签。

## 1.2 分词并给词做编号

```python
from tensorflow.keras.preprocessing.text import Tokenizer
# 创建分词器
# #num_words:None或整数,处理的最大单词数量。少于此数的单词丢掉
token = Tokenizer(num_words=10000)  
# 先分词、再计算数量排序，取num_words个单词作为字典的内容
token.fit_on_texts(train_text) 
```

## 1.3 将原始的句子转化为编号后的句子

```python
from keras.preprocessing import sequence # 用于转换

x_train_seq = token.texts_to_sequences(train_text)
x_test_seq  = token.texts_to_sequences(test_text)

```

## 1.4 句子补全

```python
x_train = sequence.pad_sequences(x_train_seq, maxlen=100) # 一个序列的最大长度
x_test = sequence.pad_sequences(x_test_seq, maxlen=100)
```

# 2. 模型训练


# 参考链接

- IMDB数据集预处理. https://blog.csdn.net/qq_42797457/article/details/102484991
- 



