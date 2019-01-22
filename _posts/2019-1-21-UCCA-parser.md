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
* 加入dep label，entity label(几乎没提升，没调好？)；加入pretrained word embedding[(http://fasttext.cc)](http://fasttext.cc), 提升很大。
* remote classifier(MLP + Biaffine)的dropout全部删去，本身remote数据少，用drop可能导致训练不完全。MLP的激活函数改为Relu, remote略微提升。
* span parser部分的FFN加入dropout, 正交初始化，aver f1略微提升。
* 加入entity-iob, 似乎有点提升，可能是误差的缘故。

存在的问题：
* 还需要区分PUNC node？还原成UCCA的时候简单处理了一下，就改了node的type属性。
* 把结果写到XML文件后重新用脚本评价结果反而变高了一点(0.3-0.4)。为什么？是因为区分PUNC node的原因？
* remote的F不是很稳定，本身dev中较少。
* 没有用batch算loss，速度太慢14min一次迭代，span parser就占了10min左右。GPU更慢。
* 多线程跑, 会有误差(挺大的)，重复跑了多个实验发现结果不是很稳定。



|                                                             labeled                              |
|                           |                    |    Primary    |  |  |  | Remote    |
|description                |  Track             |   Aver F1   |  P  |  R |  F   |  P  |  R  |  F  |
|Relu + FFN drop            | English-Wiki-Close |    0.789    |0.798|0.789|0.794|0.613|0.474|0.535|
|+ entity_iob(最好的一次)     | English-Wiki-Close |    0.795    |0.803|0.796|0.799|0.591|0.520|0.554|

## 参考

* [A Transition-Based Directed Acyclic Graph Parser for UCCA(V2)](https://arxiv.org/pdf/1704.00552v2.pdf)

* [Universal Conceptual Cognitive Annotation (UCCA)](http://www.cs.huji.ac.il/~oabend/papers/ucca_acl.pdf)

* [A Minimal Span-Based Neural Constituency Parser](http://www.aclweb.org/anthology/P/P17/P17-1076.pdf)

* [UCCA resource](http://www.cs.huji.ac.il/~oabend/ucca.html#guidelines)

* [DEEP BIAFFINE ATTENTION FOR NEURAL DEPENDENCY PARSING](https://arxiv.org/pdf/1611.01734.pdf)

