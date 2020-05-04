---
layout: post
title:  "句法分析技术应用研究"
categories: NLP
tags: NLP
excerpt: summary of recent works 
author: wjiang
mathjax: true
---

* content
{:toc}


# 用短语结构句法分析来做UCCA

TODO

# 依存句法增强的UCCA

TODO

# 依存句法增强的NMT

## 相关工作

SMT相关：TODO

最早的NMT模型往往是end-to-end的，这也是其优点之一。鉴于SMT中句法的良好表现，研究人员尝试在NMT中加入句法来提高翻译质量。尝试将相关工作分成三类:显试地加入句法、隐式地加入句法以及MTL。

显式地加入句法意味着已经拥有了源端句子的句法树，如何将该句法树信息融入到NMT模型中是关键。较早时期，Sennrich et al.(2016) 尝试用语言学特征来改进NMT，这些特征就包括了句法树中的词性标签、关系标签等。将它们映射到一个稠密向量后和词向量一起输入到encoder端。显然这样做丢失了句法树的全局结构信息，那么如何完整地编码整棵树又成为了研究热点。较为简单的方法是按照规则线性化一棵句法树再用RNN进行编码(Li et al. 2017; Currey and Heafield 2018; Wu et al. 2018)。而更常用的方法是使用Tree-RNN(Eriguchi et al. 2016; Chen et al. 2017)，这是一种专门为编码树状结构而设计的神经网络，往往比直接使用标签特征更有效。随着图神经网络的发展，也有工作尝试了用GNN作为句法树的编码器(Bastings et al. 2017; Beck et al. 2018)，均取得了不错的效果。Hao et al. (2019)则是在transformer的MHA模型中融入了短语结构树的granularity信息。

由于源端的句法树通常是自动生成的，树的准确率就难以保证。这就带来了不可避免的错误传播问题。Zhang et al. (2019)提出了隐式的方法来融入句法信息。即将源端句子输入到句法分析器后，将句法分析器的编码器输出作为NMT源端的额外输入，而非最终生成的句法树。这些基于上下文的向量含有隐式的句法信息，而且可以减轻错误传播的影响。

MTL也是句法增强的一种有效办法，让NMT模型同时去学习句法，在翻译时也就能更注重句法的信息。Luong et al. (2016)、
Aharoni and Goldberg (2017)都是将短语结构树转换为string后与翻译任务同时学习。Wu et al. (2017)、Kiperwasser and Ballesteros (2018)、Pham et al. (2019)则是将依存句法分析转化为额外的序列生成任务。此外，Pham et al. (2019)还提出了一种用MHA来MTL依存关系的方法。

## 工作



## 实验

TODO

## 分析

TODO

# 参考

* [Rico Sennrich and Barry Haddow. 2016. Linguistic input features improve neural machine translation. In Proceedings of the First Conference on Machine Translation](https://arxiv.org/pdf/1905.02878.pdf)

* [Akiko Eriguchi, Kazuma Hashimoto, and Yoshimasa Tsuruoka. 2016. Tree-to-Sequence Attentional Neural Machine Translation. In Proceedings of ACL 2016.](http://aclweb.org/anthology/P16-1078)

* [Junhui Li, Deyi Xiong, Zhaopeng Tu, Muhua Zhu, Min Zhang, and Guodong Zhou. 2017. Modeling Source Syntax for Neural Machine Translation. In Proceedings of ACL 2017. ](http://aclweb.org/anthology/P17-1064)

* [Huadong Chen, Shujian Huang, David Chiang, and Jiajun Chen. 2017. Improved Neural Machine Translation with a Syntax-Aware Encoder and Decoder. In Proceedings of ACL 2017. ](http://aclweb.org/anthology/P17-1177)

* [Joost Bastings, Ivan Titov, Wilker Aziz, Diego Marcheggiani, and Khalil Simaan. 2017. Graph Convolutional Encoders for Syntax-aware Neural Machine Translation. In Proceedings of EMNLP 2017. ](http://aclweb.org/anthology/D17-1209)

* [Daniel Beck, Gholamreza Haffari, and Trevor Cohn. 2018. Graph-to-Sequence Learning using Gated Graph Neural Networks. In Proceedings of ACL 2018. ](http://aclweb.org/anthology/P18-1026)

* [Anna Currey and Kenneth Heafield. 2018. Multi-Source Syntactic Neural Machine Translation. In Proceedings of EMNLP 2018.](http://aclweb.org/anthology/D18-1327)

* [Meishan Zhang, Zhenghua Li, Guohong Fu, and Min Zhang. 2019. Syntax-Enhanced Neural Machine Translation with Syntax-Aware Word Representations. In Proceedings of NAACL 2019.](https://arxiv.org/pdf/1905.02878)

* [Jie Hao, Xing Wang, Shuming Shi, Jinfeng Zhang, and Zhaopeng Tu. 2019. Multi-Granularity Self-Attention for Neural Machine Translation. In Proceedings of EMNLP 2019.](https://arxiv.org/pdf/1909.02222)

* [Shuangzhi Wu, Dongdong Zhang, Nan Yang, Mu Li, and Ming Zhou. 2017. Sequence-to-Dependency Neural Machine Translation. In Proceedings of ACL 2017.](http://aclweb.org/anthology/P17-1065)

* [Roee Aharoni and Yoav Goldberg. 2017. Towards String-To-Tree Neural Machine Translation. In Proceedings of ACL 2017.](http://aclweb.org/anthology/P17-2021)

* [Xinyi Wang, Hieu Pham, Pengcheng Yin, and Graham Neubig. 2018. A Tree-based Decoder for Neural Machine Translation. In Proceedings of EMNLP 2018.](http://aclweb.org/anthology/D18-1509)

* [Shuangzhi Wu, Dongdong Zhang, Zhirui Zhang, Nan Yang, Mu Li and Ming Zhou. 2018. Dependency-to-Dependency Neural Machine Translation. In Proceedings of  IEEE/ACM Transactions on Audio, Speech, and Language Processing.](https://www.researchgate.net/publication/326385741_Dependency-to-Dependency_Neural_Machine_Translation)

* [Minh-Thang Luong, Quoc V. Le, Ilya Sutskever, Oriol Vinyals, and Lukasz Kaiser. 2016. Multi-task Sequence to Sequence Learning. In Proceedings of ICLR 2016.](https://arxiv.org/pdf/1511.06114)

* [Eliyahu Kiperwasser and Miguel Ballesteros. 2018. Scheduled Multi-Task Learning: From Syntax to Translation. Transactions of the Association for Computational Linguistics.](http://aclweb.org/anthology/Q18-1017)

* [Thuong-Hai Pham, Dominik Mach´ aˇcek and Ondˇrej Bojar. Promoting the Knowledge of Source Syntax in Transformer NMT Is Not Needed. CICLING 2019.](https://arxiv.org/abs/1910.11218)






