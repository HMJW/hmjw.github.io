---
layout: post
title:  "UCCA论文实验记录"
categories: NLP
tags: NLP semantic-parsing UCCA
excerpt:  为写论文准备的实验记录
author: wjiang
mathjax: true
---

* content
{:toc}

## 一、优化修改代码

主要修改了两个部分。一个是在算出batch中所有的lstm_out后直接把所有句子中所有的span向量算出来，这样做显存占用变大，但速度提升很多。第二个就是增加了local_loss+cky解码的方法，其中cky的代码先用矩阵存储分值，再回溯。结果会比原作者的代码快一倍多，虽然看上去原作者的代码不用回溯，省了很多计算。

## 二、实验记录

#### 2019.3.18
只用了charlstm。

|                                         |                     |              |    Primary    |  |  |   Remote    |
|description                              |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|topdown loss & topdown decode            | English-Wiki-Close   |    0.789     |0.795|0.793|0.794|0.627|0.436|0.514|
|local loss平均到每个句子 & cky decode      | English-Wiki-Close   |    0.785     |0.803|0.777|0.790|0.615|0.436|0.510|
|local loss平均到每个span & cky decode      | English-Wiki-Close   |    0.783     |0.796|0.780|0.788|0.612|0.417|0.496|
|global loss & cky decode                 | English-Wiki-Close   |    0.000     |0.000|0.000|0.000|0.000|0.000|0.000|

#### 2019.3.19
测试batch影响。

