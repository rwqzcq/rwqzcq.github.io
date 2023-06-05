---
title: 用fastnlp做文本分类与序列标注
date: 2022-01-04 11:07:25
tags:
 - NLP
categories:
 - NLP
---

# 文档地址
https://fastnlp.readthedocs.io/

# 安装

```shell
pip install torch
pip install fastnlp
```

# 数据预处理

- 首先需要做的就是将自己的数据装填入fastnlp的[`Dataset`](https://fastnlp.readthedocs.io/zh/latest/tutorials/tutorial_1_data_preprocess.html)对象中。一个`Dataset`相当于一个pandas的`DataFrame`。

- 构建`Vocabulary`将字符转化成Id。


## 使用自己的中文数据集做情感分析

## Dataset

情感分析作为一个二分类任务，首先需要构建一个Dataset，推荐构建的方法为:


```python
from fastNLP import DataSet
# 构建一个dict
data = {
    'raw_chars': [ # 一维数组，存放了所有的原始文本
        '这个酒店太辣鸡了吧！', 
        '体验还算可以，环境比较安静',
        '交通还算是比较便利的，总体打9分'
    ],
    'chars': [ # 二维数组，存放的是已经切分为单独的汉字的序列
        ['这', '个', '酒', '店', '太', '辣', '鸡', '了', '吧', '！'],
        ['体', '验', '还', '算', '可', '以', '，', '环', '境', '比', '较', '安', '静'],
        ['交', '通', '还', '算', '是', '比', '较', '便', '利', '的', '，', '总', '体', '打', '9', '分'],
    ], 
    'raw_words': [ # 一维数组，存放了存放了对原始文本分词(预处理：去除停用词、词干还原....)后形成的一个以空格为分隔符的字符串
        '酒店 辣鸡',
        '体验 可以 环境 安静',
        '交通 遍历 总体 9分'
    ],
    'words': [ # 二维数组，存放了对原始文本分词(预处理：去除停用词、词干还原....)后形成的一个token list
        ['酒店', '辣鸡'],
        ['体验', '可以', '环境', '安静'],
        ['交通', '便利', '总体', '9分'],
    ],
    'seq_len': [ # 一维数组,存放了输入序列的长度，注意是输入的序列,比如情感分析输入的是words的话，那么序列就是[2, 4, 4]
        2,
        4,
        4
    ],
    'taget': [ # 每一个样本的标签
        '正向',
        '负向'
    ]
}
# 将dict传入到Dataset中
dataset = Dataset(data)
test_dataset = DataSet(test_data)
dev_dataset = DataSet(dev_dataset)
```

> 对不对原始的数据分词、完全取决于自己，

## Vocab

第二步构建`Vocab`，将字符数字转化成`数字`。

```python
from fastNLP import Vocabulary
vocab = Vocabulary()
vocab.from_dataset(dataset, field_name='words', no_create_entry_dataset=[dev_dataset, valid_dataset]) # 根据dataset的words字段来构建vocab，把test dev数据集放到no_create_entry_dataset

target_vocab = Vocabulary(unknown=None, padding=None) # 标签做映射
target_vocab.from_dataset(dataset, field_name='target')
```
关于`no_create_dataset`，官方文档的表述为：

Vocabulary 中的 no_create_entry ，如果您并不关心具体的原理，您可以**直接采取**以下的建议：在添加来自于`非训练集的词的时候将该参数置为True`, 或将`非训练集数据 传入 no_create_entry_dataset 参数`。它们的意义是在接下来的模型会使用pretrain的embedding(包括glove, word2vec, elmo与bert)且会finetune的情况下，如果仅使用来自于train的数据建立vocabulary，会导致只出现在test与dev中的词语无法充分利用到来自于预训练embedding的信息(因为他们 会被认为是unk)，所以在建立词表的时候将test与dev考虑进来会使得最终的结果更好。

## DataBundle

第三步构建[`data_bundle`](https://fastnlp.readthedocs.io/zh/latest/fastNLP.io.data_bundle.html)，将训练集、测试集、验证集、词表集成到一个对象中。关于设立data_bundle的原因官方文档表述如下：

而由于对于同一个任务，训练集，验证集和测试集会`共用同一个词表以及具有相同的目标值`，所以在fastNLP中我们使用了 DataBundle 来承载同一个任务的多个数据集 DataSet 以及它们的词表 Vocabulary 。

```python
from fastNLP.io.data_bundle import DataBundle
data_bundle = Databundle()
data_bundle.set_dataset(train_dataset, 'train')
data_bundle.set_dataset(test_dataset, 'test')
data_bundle.set_dataset(dev_dataset, 'dev')
data_bundle.set_vocab(vocab, 'words')
data_bundle.set_vocab(target_vocab, 'target')
```

## Pipeline

第四步使用`pipeline`对`data_bundle`做处理：主要是批量将数据集中的文本通过vocab转化成数字。针对文本分类任务，其内置了针对不同公开数据集的pipeline，比如针对情感分析数据集，有`ChnSentiCorpPipe`，`IMDBPipe`，针对新闻分类数据集，有`THUCNewsPipe`，比如针对情感分析任务：

```python
from fastNLP.io.pipe.classification import ChnSentiCorpPipe
pipeline = ChnSentiCorpPipe()
data_bundle = pipeline.process(data_bundle)
```
新的data_bundle里面还有4列，分别是`[chars, raw_chars, target, seq_len]`，其中`chars`里面包含了所有转化后的数字。
`ChnSentiCorpPipe`会对dataset中的`raw_chars`与`target`进行处理。针对raw_chars的话就是进行简单的字符切分，因此如果要用分好词的情感分析数据，需要把分词好的数据放到`raw_chars`。
不过针对自己的数据集，建议使用[`CLSBasePipe`](https://fastnlp.readthedocs.io/zh/latest/_modules/fastNLP/io/pipe/classification.html#AGsNewsPipe)也可以选择自己重新写一个类继承`CLSBasePipe`,`CLSBasePipe`会对dataset中的`raw_chars`与`target`进行处理。
```python
from fastNLP.io.pipe.classification import BasePipe
pipeline = BasePipe()
data_bundle = pipeline.process(data_bundle)
```
新的data_bundle生成了3列，分别是`[words, raw_words, seq_len]`。其中`words`中存放了转化后的数字。

## Word Embedding

第五步位选择词向量模型，可以用中文词向量也可以选择bert

```python
from fastNLP.embeddings import StaticEmbedding
# word2vec
embed = StaticEmbedding(data_bundle.get_vocab('words'), model_dir_or_name='cn-char-fastnlp-100d')
# bert
from fastNLP.embeddings import BertEmbedding
embed = BertEmbedding(data_bundle.get_vocab('words'), model_dir_or_name='bert-base-chinese')

```

## Model

```python

from torch import nn
from fastNLP.modules import LSTM
import torch

# 定义模型
class BiLSTMMaxPoolCls(nn.Module):
    def __init__(self, embed, num_classes, hidden_size=400, num_layers=1, dropout=0.3):
        super().__init__()
        self.embed = embed

        self.lstm = LSTM(self.embed.embedding_dim, hidden_size=hidden_size//2, num_layers=num_layers,
                         batch_first=True, bidirectional=True)
        self.dropout_layer = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, chars, seq_len):  # 这里的名称必须和DataSet中相应的field对应，比如之前我们DataSet中有chars，这里就必须为chars
        # chars:[batch_size, max_len]
        # seq_len: [batch_size, ]
        chars = self.embed(chars)
        outputs, _ = self.lstm(chars, seq_len)
        outputs = self.dropout_layer(outputs)
        outputs, _ = torch.max(outputs, dim=1)
        outputs = self.fc(outputs)

        return {'pred':outputs}  # [batch_size,], 返回值必须是dict类型，且预测值的key建议设为pred

# 初始化模型
model = BiLSTMMaxPoolCls(word2vec_embed, len(data_bundle.get_vocab('target')))
```

## Train

```python
from fastNLP import Trainer
from fastNLP import CrossEntropyLoss
from torch.optim import Adam
from fastNLP import AccuracyMetric

loss = CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.001)
metric = AccuracyMetric()
device = 0 if torch.cuda.is_available() else 'cpu'  # 如果有gpu的话在gpu上运行，训练速度会更快

trainer = Trainer(train_data=data_bundle.get_dataset('train'), model=model, loss=loss,
                  optimizer=optimizer, batch_size=32, dev_data=data_bundle.get_dataset('dev'),
                  metrics=metric, device=device)
trainer.train()  # 开始训练，训练完成之后默认会加载在dev上表现最好的模型

```

## Test

```python
from fastNLP import Tester
print("Performance on test is:")
tester = Tester(data=data_bundle.get_dataset('test'), model=model, metrics=metric, batch_size=64, device=device)
tester.test()
```

> fastnlp也给出了如何以[`词`](https://fastnlp.readthedocs.io/zh/latest/tutorials/%E6%96%87%E6%9C%AC%E5%88%86%E7%B1%BB.html#ps)为基本单位来做数据预处理

>fastnlp是怎么针对不同的任务做数据转换的

## 使用自己的数据集做序列标注

序列标注任务以`chars`作为最基本的单元，因此需要的是最核心的`raw_chars`与`target`两列。


> 调试的时候可以先用小批量的数据，train test dev用同样的数据。！

> data_bundle里面可以没有`vocab`因为`pipeline`会去生成一个vocab

# 序列标注使用bert准确率为0问题排查

使用自带的微博数据集能够正确得运行

## 用微博的数据集再加上自己的代码来弄

- 使用微博的data_bundle+_NERPipe结果为0
- 使用微博的data_bundle+WeiboNERPipe结果为0
- 使用Bert的`www`模型也不行
- 把学习率调小，使用官方文档里面默认的：**有效果**
- 设置优化器为空

> 把学习率调小,调整到跟官方给的demo一样！自己当时用的学习率是按照那个word2vec的来的，官方的用bert的学习率为`2e-5`，也就是`0.0001`

关于学习率的文章，可以看这个论文`How to How to Fine-Tune BERT for Text Classification`，推荐的就是`2e-5`

![学习率](https://img-blog.csdnimg.cn/20200225003007515.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpb24xOTkzMDkyNA==,size_16,color_FFFFFF,t_70)

# 使用自己的数据进行情感分析
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from fastNLP import DataSet
from fastNLP import Vocabulary
from fastNLP.io.data_bundle import DataBundle
from fastNLP.io import CWSPipe, ChnSentiCorpPipe
from torch import nn
from fastNLP.modules import LSTM
from fastNLP.embeddings import BertEmbedding
import torch
from fastNLP import Trainer
from fastNLP import CrossEntropyLoss
from torch.optim import Adam
from fastNLP import AccuracyMetric
from fastNLP import Tester
from fastNLP.io.model_io import ModelSaver
import pickle as pkl

# 读取数据
df = pd.read_csv('dataset/train.labeled.csv', encoding='UTF-8')
# 保留两列
df = df[['微博中文内容', '情感倾向']]
# 去除空值
df = df.dropna()
# 列重新命名
df.columns = ['content', 'label']
# 过滤label
df = df[df['label'].isin(['-1', '0', '1'])]
df['label'] = df['label'].astype(int)
# 重新索引
df = df.reset_index(drop=True)

# 设置最大字符数
max_len = 410
# 处理content字段
def process_content(sentence):
    sentence = str(sentence).strip()
    if len(sentence) >= max_len:
        sentence = sentence[0: max_len]
    return sentence
df['content'] = df['content'].apply(process_content)
# 再次过滤内容为空的数据
df = df[df['content'] != '']

# 切分数据
train_idx, test_idx, _, _  = train_test_split(list(range(df.shape[0])), df['label'], test_size=0.1, random_state=32)
df['type'] = ''
df.loc[train_idx, 'type'] = 'train'
df.loc[test_idx, 'type'] = 'test'

# 构造fastnlp数据格式
df['chars'] = df['content'].apply(lambda x: [str(i) for i in list(x)])
df['seq_len'] = df['chars'].apply(lambda x: len(x))
df['target'] = df['label']

print('数据加载成功')

def gen_dataset(_type):
    """
    生成dataset
    """
    _df = df[df['type'] == _type]
    dataset = DataSet({
        'raw_chars': _df['content'].values,
        'chars': _df['chars'].values,
        'seq_len': _df['seq_len'].values,
        'target': _df['target'].values
    })
    return dataset

train_dataset = gen_dataset('train')
test_dataset = gen_dataset('test')
valid_dataset = gen_dataset('test')

# 构建vocab
vocab = Vocabulary()
#  将验证集或者测试集在建立词表是放入no_create_entry_dataset这个参数中。
vocab.from_dataset(train_dataset, field_name='chars', no_create_entry_dataset=[valid_dataset, test_dataset])

# 创建databundle
data_bundle = DataBundle({'chars': vocab}, {'train': train_dataset, 'test': test_dataset, 'valid': valid_dataset})

# 处理databunble
data_bundle = ChnSentiCorpPipe().process(data_bundle)


# 定义模型
class BiLSTMMaxPoolCls(nn.Module):
    def __init__(self, embed, num_classes, hidden_size=400, num_layers=1, dropout=0.3):
        super().__init__()
        self.embed = embed
        self.lstm = LSTM(self.embed.embedding_dim, hidden_size=hidden_size//2, num_layers=num_layers,
                         batch_first=True, bidirectional=True)
        self.dropout_layer = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, chars, seq_len):  # 这里的名称必须和DataSet中相应的field对应，比如之前我们DataSet中有chars，这里就必须为chars
        # chars:[batch_size, max_len]
        # seq_len: [batch_size, ]
        chars = self.embed(chars)
        outputs, _ = self.lstm(chars, seq_len)
        outputs = self.dropout_layer(outputs)
        outputs, _ = torch.max(outputs, dim=1)
        outputs = self.fc(outputs)

        return {'pred':outputs}  # [batch_size,], 返回值必须是dict类型，且预测值的key建议设为pred


char_vocab = data_bundle.get_vocab('chars')
# 加载Bert
bert_embed = BertEmbedding(char_vocab, model_dir_or_name='cn', auto_truncate=True, requires_grad=True)
# 定义模型
model = BiLSTMMaxPoolCls(bert_embed, len(data_bundle.get_vocab('target')))

# 定义损失函数
loss = CrossEntropyLoss()
# 定义优化器
optimizer = Adam(model.parameters(), lr=2e-5)
# 定义评价指标
metric = AccuracyMetric()
# 定义设备
device = 0 if torch.cuda.is_available() else 'cpu'  # 如果有gpu的话在gpu上运行，训练速度会更快

# 定义trainer
batch_size = 16
n_epochs = 30
trainer = Trainer(train_data=data_bundle.get_dataset('train'), model=model, loss=loss,
                  optimizer=optimizer, batch_size=batch_size, dev_data=data_bundle.get_dataset('test'),
                  metrics=metric, device=device, n_epochs=n_epochs)
# 开始训练，训练完成之后默认会加载在dev上表现最好的模型
trainer.train()

# 测试模型
print("Performance on test is:")
tester = Tester(data=data_bundle.get_dataset('test'), model=model, metrics=metric, batch_size=batch_size, device=device)
tester.test()

# 保存模型
model_path = './save_models/bert_senti.pt'
saver = ModelSaver(model_path)
saver.save_pytorch(model)

with open('./save_models/data_bundle.pkl', 'wb') as wp:
    pkl.dump(data_bundle, wp)
```

# 预测

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from fastNLP import DataSet
from fastNLP import Vocabulary
from fastNLP.io.data_bundle import DataBundle
from fastNLP.io import CWSPipe, ChnSentiCorpPipe
from torch import nn
from fastNLP.modules import LSTM
from fastNLP.embeddings import BertEmbedding
import torch
from fastNLP import Trainer
from fastNLP import CrossEntropyLoss
from torch.optim import Adam
from fastNLP import AccuracyMetric
from fastNLP import Tester
from fastNLP.io.model_io import ModelSaver, ModelLoader
import pickle as pkl

# 定义设备
device = 0 if torch.cuda.is_available() else 'cpu'  # 如果有gpu的话在gpu上运行，训练速度会更快

# 定义模型
class BiLSTMMaxPoolCls(nn.Module):
    def __init__(self, embed, num_classes, hidden_size=400, num_layers=1, dropout=0.3):
        super().__init__()
        self.embed = embed
        self.lstm = LSTM(self.embed.embedding_dim, hidden_size=hidden_size//2, num_layers=num_layers,
                         batch_first=True, bidirectional=True)
        self.dropout_layer = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, chars, seq_len):  # 这里的名称必须和DataSet中相应的field对应，比如之前我们DataSet中有chars，这里就必须为chars
        # chars:[batch_size, max_len]
        # seq_len: [batch_size, ]
        chars = self.embed(chars)
        outputs, _ = self.lstm(chars, seq_len)
        outputs = self.dropout_layer(outputs)
        outputs, _ = torch.max(outputs, dim=1)
        outputs = self.fc(outputs)

        return {'pred':outputs}  # [batch_size,], 返回值必须是dict类型，且预测值的key建议设为pred


# 加载data_bundle
with open('./save_models/data_bundle.pkl', 'rb') as fp:
    data_bundle = pkl.load(fp)

char_vocab = data_bundle.get_vocab('chars')
# 加载Bert
bert_embed = BertEmbedding(char_vocab, model_dir_or_name='cn', auto_truncate=True, requires_grad=True)
# 定义模型
model = BiLSTMMaxPoolCls(bert_embed, len(data_bundle.get_vocab('target')))
# 加载模型
# 有GPU的情况下用这个方式加载
params = ModelLoader.load_pytorch_model('./save_models/bert_senti.pt')
# 没有GPU的情况下用这个方式加载，先放到CPU上面去
params = torch.load('./save_models/bert_senti.pt', map_location=torch.device('cpu'))
model.load_state_dict(params)
model = model.to(device)

max_len = 410

def predict(sentence):
    """
    预测一句话的情感倾向
    """
    sentence = str(sentence).strip()
    sentence = sentence[0 :max_len]
    chars = list(sentence)
    test_dataset = DataSet(data={'chars': [chars, ]})
    data_bundle.get_vocab('chars').index_dataset(test_dataset, field_name='chars', new_field_name='token_ids')
    test_data = torch.tensor(test_dataset['token_ids']).to(device)
    seq_len = torch.tensor([test_data.size()[1], ]).to(device)
    pred_index = model(test_data, seq_len)['pred'].argmax().detach().cpu().numpy().tolist()
    pred_label = data_bundle.get_vocab('target').to_word(pred_index)
    return pred_label


df = pd.read_csv('./dataset/test.csv')
df = df[df['微博中文内容'] != '']
df['预测结果'] = df['微博中文内容'].apply(predict)
df.to_csv('dataset/test.labeled.csv', index=False)
```

# 参考链接

- 利用fastnlp做的第一个中文情感分析Demo. https://blog.csdn.net/yingdajun/article/details/106825834
- Bert微调技巧实验大全-How to Fine-Tune BERT for Text Classification. https://blog.csdn.net/lion19930924/article/details/104469944
- Adam和学习率衰减（learning rate decay）. https://www.cnblogs.com/wuliytTaotao/p/11101652.html
- spacy做命名实体识别. https://blog.harumonia.moe/fastnlp-and-spacy/
- 