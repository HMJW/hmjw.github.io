---
layout: post
title:  "UCCA简介"
categories: NLP
tags: NLP semantic-parsing UCCA
excerpt: UCCA语义表示简介
author: wjiang
mathjax: true
---

* content
{:toc}


## 一、语义和语法

语义和语法有着密不可分的关系。语法结构主要用来表示语言的标准模式，但是只能间接的反应语义区别。比如，所有的语法标注方案都对(a)“John took a shower”和
(b)“John showerd”这两个句子的结构区别很敏感，但是它们很少区别(a)和(c)“John took my book”这两个句子。下图是三个句子CoNLL-style的依存表示，注意到(a)和(c)有着不同的语义但是有着相同的语法结构。

![dep-example](/src/2018-12-22-UCCA-intro/dep-example.png)




强调(a)和(b)之间的语义相似性有助于机器翻译，比如(a)和(b)都会被翻译成德语句子“John duschte”，忽略它们的语法区别。而区分(a)和(c)之间的语义差别有利于问答(Question Answering)应用。比如当回答“what did John take?”这个问题时，“my book”会是比“a shower”更似是而非的答案。所以很多语义表示方案被提出，本文介绍一种新颖的表示方法用于注释语义区别，旨在从特定的句法结构中抽象出来。

## 二、UCCA简介

UCCA全称为Universal Conceptual Cognitive Annotation。UCCA使用有向无环图(Directed Acyclic Graghs,DAGs)来表示语义结构，它们的叶子就对应了句子中的每个词。一个node(或者叫unit)对应了一个或多个terminal(但是不一定连续，如下图b)，它们被看做是一个单独的实体或者认知考虑。每条边都带有一个类别，表示子节点在父亲关系中的作用。下图是几个例子。

![ucca-example](/src/2018-12-22-UCCA-intro/ucca-example.png)




UCCA是一种多层表示，其中每一层对应于语义区别的“模块”。 UCCA的foundational layer涵盖了由所有语法类别（言语，名义，形容词和其他）的谓词引起的谓词-论证结构，它们之间的相互关系以及其他主要语言现象（如协调和多词表达)。图层的基本概念是场景，描述状态，动作，动作或其他随时间演变的关系。每个场景包含一个主要关系（标记为进程或状态），以及一个或多个参与者。例如，句子“After graduation, John moved to Paris”（图a）包含两个场景，其主要关系是“graduation”和“moved”。 “John”是两个场景中的参与者，而“Paris”仅在后者中。进一步的类别考虑了场景间关系以及复杂论证和关系的内部结构（例如协调，多词表达和修改）。




对于每个非根节点，都有指向它的边，这些边被区分为primary(实边)和remote(虚边)，primary边构成树状结构，remote边允许重入，导致形成了DAGs。所以，UCCA gragh有几个特殊的属性，一个是可重入(reentrancy)，一个是不连续(discontinuity)，最后一个是用了non-terminal nodes，这给parsing带来了巨大的挑战。

## 参考

* [A Transition-Based Directed Acyclic Graph Parser for UCCA](https://arxiv.org/pdf/1704.00552v2.pdf)

* [Universal Conceptual Cognitive Annotation (UCCA)](http://www.cs.huji.ac.il/~oabend/papers/ucca_acl.pdf)

* [UCCA resource](http://www.cs.huji.ac.il/~oabend/ucca.html#guidelines)

