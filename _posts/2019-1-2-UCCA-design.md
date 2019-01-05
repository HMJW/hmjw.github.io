---
layout: post
title:  "UCCA parsing 系统设计"
categories: NLP
tags: NLP semantic-parsing UCCA
excerpt: UCCA parsing system design
author: wjiang
mathjax: true
---

* content
{:toc}


## 一、基本思路

> * 预处理数据，将UCCA图转化为短语结构树的形式。
>    * 处理implicit节点
>    * 处理linkage node
>    * 处理remote边
>    * 处理discontinuity
>    * 调整label位置到non-terminal node上
> * 用span parser训练(预测)
> * 把短语结构树还原成UCCA图

## 二、预处理数据

下图统计了所有数据集的大小。但以下测试都是在英文的训练集和开发集上统计的。

|              |   train   |    dev    |    test   |   total   |
|--------------|-----------|-----------|-----------|-----------|
| corpus       | #sentence | #sentence | #sentence | #sentence |
| English-Wiki |   4113    |    514    |    515    |    5142   |
| English-20K  |   0       |    0      |    492    |    492    |
| French-20K   |   15      |    238    |    239    |    492    |
| German-20k   |   5211    |    651    |    652    |    6514   |


#### 1.处理implicit节点

implicit节点是UCCA中的特殊节点，它没有对应的叶子,如下图所示。baseline模型中也没有提出有效的办法处理它，所以直接将其删除，不考虑。implicit数量待统计。
![implicit-example](/src/2019-1-2-UCCA-design/implicit-example.jpg)

#### 2.处理linkage node

linkage node也是baseline中一个尚未解决的问题。它类似root节点没有父亲，但它对应的span是句子的一部分。也就是说，一个句子可能会构成类似森林的结构，如下图。统计了训练集和开发集，发现共有3818个linkage node出现在了2544个句子中，对应的边应该更多，或许这就是论文中结果并不高的原因。暂时将所有linkage node以及它出去的边全部删去。
![linkage-example](/src/2019-1-2-UCCA-design/linkage-example.jpg)

#### 3.处理remote边

短语结构树要求每个节点只能有一个父亲，而UCCA允许一个节点有多个父亲，其中一个父亲经过primary edge(实边)指向它，其他父亲经过remote edge(虚边)指向它。为了消除remote edge，同时又能还原信息，采取扩展标签的方式。如下图所示，只要删除remote edge，同时在primary edge的标签上添加额外的信息，告知该边指向的节点还有其他remote edge指向它即可。简单起见，就在标签后面添加“-R”。
![remote-example](/src/2019-1-2-UCCA-design/remote-example.jpg)




但是一个节点可以有多条remote edge指向它，仅仅添加“-R”似乎还不够。于是我统计了训练集和开发集(英文)的remote edge分布，如下图，其中第一行表示共有3626个节点只有1条remote edge指向它。根据分布，或许不必要考虑多条remote edge的情况。

| #remote edge  | #node | proportion |
|---------------|-------|------------|
| 1             | 3626  |    83.0%   |
| 2             | 596   |    13.6%   |
| 3             | 104   |    2.4%    |
| 4             | 31    |    0.7%    |
| 5             | 5     |    0.1%    |
| 6             | 6     |    0.1%    |

#### 4.处理discontinuity

短语结构树要求每个non-terminal节点对应的叶子必须连续，而UCCA允许叶子不连续。判断一个节点的叶子是否不连续比较容易，共有939个node出现了discontinuity，分布在735个句子中，占比不是很大。我主要把这些node分成两类。




第一类是node之间没有交叉的discontinuity，如下图所示。不管如何，这种情况可以用两种方法调整。第一种策略是向下移动，这种策略定死了span的左右范围，把范围里的不连续节点移到该范围内。如图中黄色标记所示。第二种策略是向上移动，如图中蓝色标记所示，显然在该例子中向上移动的代价要小一些。
![discontinue-example1](/src/2019-1-2-UCCA-design/discontinue-example1.jpg)




再来看下面一个例子，如果采用向下移动的策略，只要修改一条边，但有一个子树移动了位置。如果采用向上移动的策略则要移动右边所有的边，似乎这样代价比较大。事实上，我目测数据中这种情况最多，span中不连续的叶子只占一小片，向下移动只要动这一小片叶子即可，而向上移动要把右边所有的叶子都调整位置，也可能会移动右边的子树，所以大部分情况不是很好。
![discontinue-example2](/src/2019-1-2-UCCA-design/discontinue-example2.jpg)




同样下面的例子也可以用向上和向下两个策略来解决。总之，只要一个句子中只有一个span出现不连续，或者多个不连续的span彼此不交叉，都可以用这两种方法解决。到时候只要选择代价较小的方法即可。目前向下移动已经实现完。
![discontinue-example3](/src/2019-1-2-UCCA-design/discontinue-example3.jpg)




第二类是node之间出现了交叉的discontinuity，统计了共有125对交叉的node。如下图，有两块不连续的span(图中标红的node的span)有交叉。这种情况比较简单，似乎也可以用向上和向下移动的方法解决，如图中黄色和蓝色标记。目测这种情况占大多数。
![discontinue-example4](/src/2019-1-2-UCCA-design/discontinue-example4.jpg)





但下面这个例子比较复杂，从图中来看可以找到一个比较好的移动方法，但是光向上或者向下移动无法解决两个node的不连续。
![discontinue-example5](/src/2019-1-2-UCCA-design/discontinue-example5.jpg)


## 三、训练span parser

待添加

## 四、还原为UCCA gragh

待添加

## 参考

* [A Transition-Based Directed Acyclic Graph Parser for UCCA(V2)](https://arxiv.org/pdf/1704.00552v2.pdf)

* [Universal Conceptual Cognitive Annotation (UCCA)](http://www.cs.huji.ac.il/~oabend/papers/ucca_acl.pdf)

