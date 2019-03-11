---
layout: post
title:  "UCCA系统报告论文"
categories: NLP
tags: NLP semantic-parsing UCCA
excerpt: UCCA system description papers
author: wjiang
mathjax: true
---

* content
{:toc}


## 一、CUNY-PKU Parser at SemEval-2019 Task 1: Cross-lingual Semantic Parsing with UCCA

#### 主要贡献

本文基于TUPA (Hershcovich et al., 2017a, 2018)提出了一个新的模型叫cascaded bilstm模型。很简单，就是在bilstm模型上面再叠一层mlp，如下图所示。

![cascaded model](/src/2019-3-9-UCCA-review/cascaded.jpg)

此外，本文还提出了一种ensemble的方法，即拿到多个模型的输出（UCCA gragh）后，重新用CKY解码得到一个新的UCCA gragh。为此需要把UCCA图转化为（span，label）和其对应的score。span和label的表示方法与我们的system类似。对于每一个parser都赋予一个weight，span就根据它来自哪个parser赋予score，最终把所有的span和score对应相加得到chart。

处理remote：完全没看懂。

处理discontinuity：在ensemble之前需要处理discontinuity。方法也与我们有点类似：
> * 找到一个不连续的节点x，它的span开始位置为[a, b)
> * 找到节点y，它的span连续且从b开始而且高度最高。（类似我们的从下往上找）,设指向y的边为e。
> * 创建MINOR节点z，创建边parent(y)->z,移除边e，创建边x->y,且标记FAKE。

![discontinuity](/src/2019-3-9-UCCA-review/discontinuity.jpg)

另外，作者还尝试了用self-attentive Constituency Parser来做比较，通过tree->conllu->UCCA的方式得到UCCA。

#### 实验

open的训练集中英文和德文多了1000句左右，法语多了500多句，来源未知。其余好像没特别的。实验结果如下：

![discontinuity](/src/2019-3-9-UCCA-review/exp1.jpg)

至于Constituency Parser的方法，作者使用了预训练好的parser，然后通过两次转换得到UCCA进行评价，只给出了unlabeled结果，结果很差。


#### 存疑

1.论文中提到他们是通过预先训练好Bilstm模型,再训练MLP来构建cascaded模型的，意思是 不是用整个模型直接训练的？（原文：Most importantly, we introduce a new model Cascaded BiLSTM by ﬁrst pre-training the BiLSTM and MLP model and then to continue training another MLP model.然而此句只在intro出现了一次，之后再也没提及。)

2.如何还原discontinuity没有讲（看）明白？

3.为什么实验结果中缺失好多?缺失了一些比较。

4.表格中MLP和BiLSTM都是TUPA中的模型，Closed德语为什么比baseline高这么多，不是模型和baseline一样吗？



## 二、UC Davis at SemEval-2019 Task 1: DAG Semantic Parsing with Attention-based Decoder

#### 模型
本文提出了一种attention-based decoder用来实现DAG parsing。

首先需要用向量表示DAG中的每个node，表示方法与结构树中的span表示以及我们的系统几乎一样，不再赘述。

用于解码的注意力机制: 给定一个node表示$v_{i,j}$，与[1 : j]的每个词做attention，取最大的作为它的$left-boundary$。如果$left-boundary \geq i$, 则创建一个父节点只指向它，例如图中的$node_{1.6}$；否则创建一个node，它的span应该囊括[$left-boundary$, j]，例如图中的$node_{1.4}$的$left-boundary$为1，则创建了$node_{1.5}$，连接[1 : 5]中的节点。至于attention计算方法，就是经过同一个MLP，再做点乘：

$$h_i = ReLU(Wv_{i}+b)$$

$$h_o = ReLU(Wv_{o}+b)$$

$$mm = h_i h_o^T$$

$$p_{boundary}=softmax(mm)$$

标签预测: 把某个节点和其父亲的向量拼接后经过MLP作分类：

$$h=ReLU(W_l^1(p\cdot v_{i,j})+b_l^1)$$

$$l=argmax(softmax(W_l^2h+b_l^2))$$

处理discontinuous node: 做一个二元分类：判断该span是否形成一个proper noun，或者该span是一个discontinuous node。
若是第一种情况，则连接所有节点（例如图中的$node_{1.1}$），若是第二种情况，则只连接最左边和最右边的节点（例如图中的$node_{1.4}$）。

处理remote edges: 用一个不同的BiLSTM，然后和primary edge一样做用matrix multiplication decoder。

![attention](/src/2019-3-9-UCCA-review/attention.jpg)

#### 实验
训练时，$node_i$ attend到它父亲$node_p$最左边的孩子，直到$node_p$不是$node_p$的父亲的最左边孩子。cross-entropy loss。
预测时，先为每个terminal创建一个non-termonal node，然后执行attention。
结果只给出了英文close的结果,和baseline差不多。

#### 存疑
1.符号表示不清，我看的时候感觉前后矛盾(比如i,j)。还有自己定义的符号下面没用过($j_r$定义了没用过，下面是写错了？)，不知道定义的干嘛的。比如图中的蓝线表达的意思应该是1.4 attention到1.3和1.1，但是公式的含义明明是attention到terminal node,然后下面又说是父亲的最左边孩子？

2.remote edge不知道怎么做的。

3.还有这个二元分类，算出两个分值是做什么，怎么判断属于哪一种情况？比大小？那loss怎么算。也没说。二元分类不应该是用sigmoid，然后和0.5做比较吗？

4.为什么在预测时要为每个terminal创建non-terminal？




## 参考
* [A Transition-Based Directed Acyclic Graph Parser for UCCA(V2)](https://arxiv.org/pdf/1704.00552v2.pdf)

* [CUNY-PKU Parser at SemEval-2019 Task 1: Cross-lingual Semantic Parsing with UCCA](/src/2019-3-9-UCCA-review/243.pdf)

* [UC Davis at SemEval-2019 Task 1: DAG Semantic Parsing with Attention-based Decoder](/src/2019-3-9-UCCA-review/233.pdf)

