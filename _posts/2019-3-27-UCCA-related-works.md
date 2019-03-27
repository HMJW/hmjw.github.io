---
layout: post
title:  "UCCA相关工作论文"
categories: NLP
tags: NLP semantic-parsing UCCA
excerpt: 最近看的一些相关论文, 主要来自UCCA两篇ACL论文中引用的文献以及constituency parsing相关文献。
author: wjiang
---

* content
{:toc}

## Constituency Parsing
[Constituency Parsing with a Self-Attentive Encoder](https://arxiv.org/pdf/1805.01052v1.pdf) : 来自ACL2018，用self-attention代替LSTM。我重点看了该文章以及对应的代码，并且尝试复现，发现结果没有论文中的那么好，最有可能的原因是论文中的训练集有3万多句，而我只有4100多句，而且还是转化过来的树。值得一提的是论文中提到的将word representation和position encoding分离的方法在UCCA数据上提升非常大（3个多点），也许是因为本身准确率低。

[Grammar as a Foreign Language](https://arxiv.org/pdf/1412.7449.pdf) : 首次提出用seq2seq模型来实现syntactic constituency parsing。

[Straight to the Tree: Constituency Parsing with Neural Syntactic Distance](https://arxiv.org/pdf/1806.04168.pdf) : 提出了一种利用syntactic distance的表示来实现类似top-down解码。

[Constituent Parsing as Sequence Labeling](https://arxiv.org/pdf/1810.08994.pdf) : 来自EMNLP2018，提出用序列标注模型来解决短语结构树解析。

## Semantic Multi-task Learning
[Neural Semantic Parsing over Multiple Knowledge-bases](https://arxiv.org/pdf/1702.01569.pdf) : 来自ACL2017。

[Transfer Learning for Neural Semantic Parsing](https://arxiv.org/pdf/1706.04326.pdf)

[A Joint Many-Task Model: Growing a Neural Network for Multiple NLP Tasks](https://arxiv.org/pdf/1611.01587v5.pdf) : 来自EMNLP2017

[Deep multitask learning for semantic dependency parsing](https://arxiv.org/pdf/1704.06855.pdf) : 来自ACL2017

几个常用的MTL架构：
1. 共享embedding和encoder，分别使用各自的decoder。
2. 共享embedding；保留主任务的encoder，添加一个共享的encoder，两个encoder的输出拼接或相加或者只用主任务的作为特定decoder的输入。

## SRL
TO BE ADDED。
