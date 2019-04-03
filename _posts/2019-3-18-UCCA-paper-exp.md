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

主要修改了两个部分。一个是在算出batch中所有的lstm_out后直接把所有句子中所有的span向量算出来，这样做显存占用变大，但速度提升很多。第二个就是增加了local_loss+cky解码的方法，其中cky的代码先用矩阵存储分值，再回溯。结果会比原作者的代码快一倍多，虽然看上去原作者的代码不用回溯，省了很多循环。

## 二、实验记录

#### 2019.3.18
只用了charlstm。

|                                         |                     |              |    Primary    |  |  |   Remote    |
|description                              |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|topdown loss & topdown decode            | English-Wiki-Close   |    0.789     |0.795|0.793|0.794|0.627|0.436|0.514|
|local loss平均到每个句子 & cky decode      | English-Wiki-Close   |    0.785     |0.803|0.777|0.790|0.615|0.436|0.510|
|local loss平均到每个span & cky decode      | English-Wiki-Close   |    0.783     |0.796|0.780|0.788|0.612|0.417|0.496|
|global loss & cky decode                 | English-Wiki-Close   |    0.786     |0.819|0.766|0.792|0.639|0.395|0.488|

#### 2019.3.19
测试batch影响。chart默认是local loss + cky解码。

|                                         |                     |              |    Primary    |  |  |   Remote    |
|description                              |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|topdown-batch=32                           | English-Wiki-Close   |    0.788     |0.798|0.788|0.793|0.663|0.327|0.438|
|topdown-batch=64                            | English-Wiki-Close   |    0.787     |0.793|0.792|0.792|0.609|0.373|0.463|
|chart-batch=32                            | English-Wiki-Close   |    0.785     |0.808|0.773|0.790|0.695|0.398|0.506|
|chart-batch=64                            | English-Wiki-Close   |    0.785     |0.803|0.776|0.790|0.668|0.384|0.488|

#### 2019.3.20
charlstm的影响, 加入dropout。chart默认是local loss + cky解码。

|                                         |                     |              |    Primary    |  |  |   Remote    |
|description                              |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|topdown-char_dim=64,char_lstm=32*2,drop=0.2  | English-Wiki-Close   |    0.785     |0.794|0.786|0.790|0.654|0.381|0.482|
|topdown-char_dim=100,char_lstm=50*2,drop=0.5 | English-Wiki-Close   |    0.786     |0.794|0.787|0.791|0.626|0.406|0.493|
|chart-char_dim=64,char_lstm=32*2,drop=0.2  | English-Wiki-Close   |    0.779     |0.801|0.768|0.784|0.620|0.365|0.460|
|chart-char_dim=100,char_lstm=50*2,drop=0.5| English-Wiki-Close   |    0.783     |0.799|0.777|0.788|0.644|0.395|0.490|

#### 2019.3.25
尝试self attention。目前结果77%左右，默认将word representation和position encoding分离。

|                                             |                     |              |    Primary    |  |  |   Remote    |
|description                                  |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|topdown,d=600,l=6,optimizer沿用论文           | English-Wiki-Close   |    0.773     |0.783|0.774|0.779|0.606|0.351|0.445|
|chart,d=600,l=6,optimizer沿用论文             | English-Wiki-Close   |    0.775     |0.794|0.766|0.780|0.591|0.417|0.489|
|topdown,d=600,l=8,optimizer沿用论文           | English-Wiki-Close   |    0.776     |0.785|0.778|0.782|0.581|0.373|0.454|
|topdown,d=600,l=6,optimizer=adam             | English-Wiki-Close   |    0.778     |0.784|0.782|0.783|0.637|0.354|0.455|

普通的adam效果还好一些，继续增大层数已经没有用了。后续有时间继续添加一些实验。

#### 2019.4.1
self attention模型中加入了charlstm部分的dropout，有点提升。
|                                                       |                     |              |    Primary    |  |  |   Remote    |
|description                                            |  Track              |   Aver F1    |  P  |  R |  F   |  P  |  R  |  F  |
|topdown,d=600,l=6,adam,embdrop=0.4,chardrop=0.2        | English-Wiki-Close  |    0.785     |0.795|0.786|0.791|0.586|0.409|0.482|
|topdown,d=600,l=6,adam,embdrop=0.4,chardrop=0.4        | English-Wiki-Close  |    0.783     |0.791|0.786|0.788|0.648|0.376|0.476|
|topdown,d=600,l=6,adam,embdrop=0.5,chardrop=0.5        | English-Wiki-Close  |    0.786     |0.794|0.788|0.791|0.637|0.392|0.486|


#### 2019.4.3
尝试用self attention模型同时训练ucca和srl。目前效果还不好。
