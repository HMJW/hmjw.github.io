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
* 把结果写到XML文件后重新用脚本评价结果反而变高了一点(0.3-0.4)。仍未解决。
* remote的F不是很稳定，本身dev中较少。
* 没有用batch算loss，速度太慢14min一次迭代，span parser就占了10min左右。GPU更慢。
* 多线程跑, 会有误差(挺大的)，重复跑了多个实验发现结果不是很稳定。


#### 2019.1.28
初步实验。

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|single + pre emb            | English-Wiki-Closed |    0.789     |0.798|0.789|0.794|0.613|0.474|0.535|
|single + bert               | English-Wiki-Open   |    0.817     |0.823|0.820|0.821|0.612|0.575|0.593|
|single + pre emb + bert     | English-Wiki-Open   |    0.821     |0.822|0.828|0.825|0.610|0.597|0.603|
|Multilingual                | English-Wiki-Open   |    0.761     |0.768|0.764|0.766|0.538|0.441|0.485|
|Multilingual + pre emb      | English-Wiki-Open   |    0.786     |0.798|0.784|0.791|0.591|0.444|0.507|
|Multilingual + bert         | English-Wiki-Open   |    0.815     |0.825|0.815|0.820|0.602|0.548|0.573|
|Multilingual +pre emb + bert| English-Wiki-Open   |    0.822     |0.823|0.831|0.827|0.599|0.580|0.590|

|                            |                      |              |    Primary    |  |  |   Remote    |
|description                 |  Track               |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|Multilingual                | French-20K-Open      |    0.681     |0.682|0.694|0.688|0.614|0.238|0.343|
|Multilingual + pre emb      | French-20K-Open      |    0.645     |0.649|0.658|0.653|0.472|0.079|0.136|
|Multilingual + bert         | French-20K-Open      |    0.788     |0.790|0.801|0.795|0.638|0.388|0.483|
|Multilingual +pre emb + bert| French-20K-Open      |    0.773     |0.775|0.786|0.780|0.688|0.350|0.464|

|                            |                      |              |    Primary    |  |  |   Remote    |
|description                 |  Track               |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|single + pre emb            | German-20K-Closed    |    0.825     |0.832|0.830|0.831|0.830|0.396|0.536|
|single + bert               | German-20K-Open      |    0.837     |0.845|0.839|0.842|0.777|0.501|0.610|
|single + pre emb + bert     | German-20K-Open      |    0.844     |0.849|0.848|0.849|0.817|0.507|0.628|
|Multilingual                | German-20K-Open      |    0.803     |0.810|0.808|0.809|0.736|0.423|0.537|
|Multilingual + pre emb      | German-20K-Open      |    0.822     |0.829|0.826|0.828|0.748|0.442|0.555|
|Multilingual + bert         | German-20K-Open      |    0.835     |0.840|0.839|0.840|0.844|0.455|0.592|
|Multilingual +pre emb + bert| German-20K-Open      |    0.843     |0.848|0.849|0.849|0.775|0.512|0.617|


#### 2019.2.7
调整了部分代码，重跑一遍所有实验。发现Multilingual + bert模型在英语和法语上的结果有问题，之前的结果偏低了，会影响最终结果。Multilingual + pre模型在法语上的结果也偏低了，不过还是比不加pre要低挺多，不影响最终结果。其他实验误差只在0.2%左右，说明没有问题。尝试了添加阈值来确定是否选择两条remote，但是好像没有用。发现提交的法语结果有误，不过还是比第一名低很多。

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|Multilingual + pre emb      | English-Wiki-Open   |    0.788     |0.797|0.789|0.793|0.602|0.490|0.541|
|Multilingual + bert         | English-Wiki-Open   |    0.826     |0.831|0.831|0.831|0.619|0.537|0.575|
|Multilingual +pre emb + bert| English-Wiki-Open   |    0.822     |0.833|0.821|0.827|0.626|0.575|0.599|

|                            |                      |              |    Primary    |  |  |   Remote    |
|description                 |  Track               |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|Multilingual + pre emb      | French-20K-Open      |    0.665     |0.670|0.677|0.673|0.564|0.103|0.174|
|Multilingual + bert         | French-20K-Open      |    0.789     |0.790|0.801|0.796|0.706|0.416|0.524|
|Multilingual +pre emb + bert| French-20K-Open      |    0.777     |0.780|0.789|0.785|0.680|0.327|0.442|

|                            |                      |              |    Primary    |  |  |   Remote    |
|description                 |  Track               |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|Multilingual + pre emb      | German-20K-Open      |    0.821     |0.829|0.824|0.826|0.766|0.434|0.554|
|Multilingual + bert         | German-20K-Open      |    0.841     |0.845|0.847|0.846|0.830|0.515|0.635|
|Multilingual +pre emb + bert| German-20K-Open      |    0.841     |0.845|0.846|0.845|0.811|0.547|0.654|


#### 2019.2.24
补跑了几个实验, 暂时各跑了两个。

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|no pre emb                  | English-Wiki-Close   |    0.774     |0.777|0.780|0.778|0.619|0.482|0.542|
|+pre emb&no fine tuning     | English-Wiki-Close   |    0.785     |0.793|0.787|0.790|0.619|0.411|0.494|


|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|no pre emb                  | German-20K-Close   |    0.811     |0.817|0.816|0.817|0.733|0.439|0.549|
|+pre emb&no fine tuning     | German-20K-Close   |    0.823     |0.830|0.827|0.829|0.812|0.409|0.544|


#### 2019.2.27
修改了处理discontinuity的部分。修改了remote部分，只用一个MLP和loss。结果没有太大变化。

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|modify dis&remote           | English-Wiki-Close  |    0.790     |0.799|0.790|0.795|0.644|0.433|0.518|


|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|modify dis&remote           | German-20K-Close    |    0.825     |0.835|0.827|0.831|0.763|0.401|0.526|

#### 2019.3.2
改用了英文的单语言BERT测试结果

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|base BERT + pre emb         | English-Wiki-Open   |    0.826     |0.833|0.828|0.831|0.616|0.507|0.556|
|large BERT + pre emb        | English-Wiki-Open   |    0.821     |0.827|0.825|0.826|0.634|0.534|0.580|

#### 2019.3.6
用单语言BERT在unlabeled数据上fine tuning后重新训练，发现结果没有太大变化。

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|finetuning BERT + pre emb   | English-Wiki-Open   |    0.826     |0.833|0.828|0.831|0.616|0.507|0.556|

#### 2019.3.7
测试charlstm的效果。删除entity和dep label。

|                            |                     |              |    Primary    |  |  |   Remote    |
|description                 |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|finetuning BERT + pre emb   | English-Wiki-Open   |    0.826     |0.833|0.828|0.831|0.616|0.507|0.556|




## 参考

* [A Transition-Based Directed Acyclic Graph Parser for UCCA(V2)](https://arxiv.org/pdf/1704.00552v2.pdf)

* [Universal Conceptual Cognitive Annotation (UCCA)](http://www.cs.huji.ac.il/~oabend/papers/ucca_acl.pdf)

* [A Minimal Span-Based Neural Constituency Parser](http://www.aclweb.org/anthology/P/P17/P17-1076.pdf)

* [UCCA resource](http://www.cs.huji.ac.il/~oabend/ucca.html#guidelines)

* [DEEP BIAFFINE ATTENTION FOR NEURAL DEPENDENCY PARSING](https://arxiv.org/pdf/1611.01734.pdf)

