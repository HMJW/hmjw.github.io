---
layout: post
title:  "UCCA parser 实验记录"
categories: NLP
tags: NLP semantic-parsing UCCA
excerpt: UCCA parser
author: wjiang
mathjax: true
---

* content
{:toc}


## 一、基本思路

> * 预处理数据，从UCCA中提取树以及remote信息。
>    * 删除implicit节点
>    * 删除linkage node
>    * 处理remote边，扩展标签
>    * 处理discontinuity，扩展标签
>    * 调整label位置到non-terminal node上
> * 训练模型
>    * 共用底层的LSTM encoder
>    * 用Multi-task learning 同时训练span parser以及remote classifier
> * 预测UCCA图
>    * 先用span parser预测树
>    * 通过扩展的标签还原discontinuity
>    * 通过扩展的标签以及remote classifier还原remote

## 二、模型介绍

模型主要分成三个部分。第一个部分是shared encoder，就是底层公用的LSTM。第二个部分是span parser部分，详情参考<[A Minimal Span-Based Neural Constituency Parser](http://www.aclweb.org/anthology/P/P17/P17-1076.pdf)>,几乎没有做任何变化。第三个部分是remote classifier，详情参考<[DEEP BIAFFINE ATTENTION FOR NEURAL DEPENDENCY PARSING](https://arxiv.org/pdf/1611.01734.pdf)>，每个node同样也像span parser一样用span向量表示，其余没有做太多改动。

* 训练时，需要从UCCA中提取转换后的树(详情见[博客](https://hmjwhmjw.github.io/2019/01/02/UCCA-design/))以及remote的信息，分别传给span parser以及remote classifier来计算loss。得到的两个loss相加后进行backword。若图中没有remote，remote部分的loss就为0。如下图所示。
![training](/src/2019-1-21-UCCA-parser/training.png)

* 测试时，先通过span parser得到一棵树，先通过规则还原discontinuity，再检测树中的扩展标签。如果没有对应的remote标签则无需添加remote edge，若有，通过remote classifier添加remote edge。如下图所示。
![testing](/src/2019-1-21-UCCA-parser/testing.png)


## 三、实验记录

下图统计了所有数据集的大小。

|              |   train   |    dev    |    test   |   total   |
|--------------|-----------|-----------|-----------|-----------|
| corpus       | #sentence | #sentence | #sentence | #sentence |
| English-Wiki |   4113    |    514    |    515    |    5142   |
| English-20K  |   0       |    0      |    492    |    492    |
| French-20K   |   15      |    238    |    239    |    492    |
| German-20k   |   5211    |    651    |    652    |    6514   |


细节及调参:
* 没有考虑left，down只考虑向下移一步
* 一个节点如果有多条remote edge，都作为正确的pair训练，但预测的时候只取最大的一个。
* 排除掉了一些节点不可能作为remote edge的parent，但是没有提高准确率。
* 在恢复discontinuity时，如果移动会产生没有叶子的节点，则不移动。
* 加入dep label，entity label(几乎没提升，没调好？)；加入pretrained word embedding[(http://fasttext.cc)](http://fasttext.cc), 提升很大。需要除以标准差，否则基本没效果。
* remote classifier(MLP + Biaffine)的dropout全部删去，本身remote数据少，用drop可能导致训练不完全。MLP的激活函数改为Relu, remote略微提升。
* span parser部分的FFN加入dropout, 正交初始化，aver f1略微提升。
* 加入entity-iob, 似乎有点提升，可能是误差的缘故。

存在的问题：
* 还需要区分PUNC node？还原成UCCA的时候简单处理了一下，就改了node的type属性。
* 把结果写到XML文件后重新用脚本评价结果反而变高了一点(0.3-0.4)。为什么？是因为区分PUNC node的原因？
* remote的F不是很稳定，本身dev中较少。
* 没有用batch算loss，速度太慢14min一次迭代，span parser就占了10min左右。GPU更慢。
* 多线程跑, 会有误差(挺大的)，重复跑了多个实验发现结果不是很稳定。


|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|single + pre emb            | English-Wiki-Closed |    0.789     |0.798|0.789|0.794|0.613|0.474|0.535|
|single + bert               | English-Wiki-Open   |    0.817     |0.820|0.823|0.821|0.575|0.612|0.593|
|single + pre emb + bert     | English-Wiki-Open   |    0.821     |0.822|0.828|0.825|0.597|0.610|0.603|
|Multilingual                | English-Wiki-Open   |    0.761     |0.768|0.764|0.766|0.538|0.441|0.485|
|Multilingual + pre emb      | English-Wiki-Open   |    0.786     |0.784|0.798|0.791|0.444|0.591|0.507|
|Multilingual + bert         | English-Wiki-Open   |    0.815     |0.825|0.815|0.820|0.602|0.548|0.573|
|Multilingual +pre emb + bert| English-Wiki-Open   |    0.822     |0.823|0.831|0.827|0.599|0.580|0.590|

|                            |                      |              |    Primary    |  |  |   Remote    |
|description                 |  Track               |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|Multilingual                | French-20K-Open      |    0.681     |0.682|0.694|0.688|0.614|0.238|0.343|
|Multilingual + pre emb      | French-20K-Open      |    0.645     |0.658|0.649|0.653|0.079|0.472|0.136|
|Multilingual + bert         | French-20K-Open      |    0.788     |0.790|0.801|0.795|0.638|0.388|0.483|
|Multilingual +pre emb + bert| French-20K-Open      |    0.773     |0.786|0.775|0.780|0.350|0.688|0.464|

|                            |                      |              |    Primary    |  |  |   Remote    |
|description                 |  Track               |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|single + pre emb            | German-20K-Closed    |    0.825     |0.832|0.830|0.831|0.830|0.396|0.536|
|single + bert               | German-20K-Open      |    0.837     |0.839|0.845|0.842|0.501|0.777|0.610|
|single + pre emb + bert     | German-20K-Open      |    0.844     |0.848|0.849|0.849|0.509|0.817|0.628|
|Multilingual                | German-20K-Open      |    0.803     |0.810|0.808|0.809|0.736|0.423|0.537|
|Multilingual + pre emb      | German-20K-Open      |    0.822     |0.826|0.829|0.828|0.422|0.748|0.555|
|Multilingual + bert         | German-20K-Open      |    0.835     |0.840|0.839|0.840|0.844|0.455|0.592|
|Multilingual +pre emb + bert| German-20K-Open      |    0.843     |0.849|0.848|0.849|0.512|0.775|0.617|


## 参考

* [A Transition-Based Directed Acyclic Graph Parser for UCCA(V2)](https://arxiv.org/pdf/1704.00552v2.pdf)

* [Universal Conceptual Cognitive Annotation (UCCA)](http://www.cs.huji.ac.il/~oabend/papers/ucca_acl.pdf)

* [A Minimal Span-Based Neural Constituency Parser](http://www.aclweb.org/anthology/P/P17/P17-1076.pdf)

* [UCCA resource](http://www.cs.huji.ac.il/~oabend/ucca.html#guidelines)

* [DEEP BIAFFINE ATTENTION FOR NEURAL DEPENDENCY PARSING](https://arxiv.org/pdf/1611.01734.pdf)

