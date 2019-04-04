---
layout: post
title:  "提交arxiv遇到的问题"
categories: tools
tags:  tools
excerpt: 提交arxiv需要注意的问题
author: wjiang
---

* content
{:toc}

## 注意事项

在overleaf上下载的源码可能不包含.bbl文件，而是.bib文件。提交arxiv需要bbl文件，所以请确保在本地编译通过，生成.bbl文件，然后把文件名都命名为main。下图是提交时的所有文件。

运行如下命令：

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

提交时把bib文件移除。
```bash
├── acl2018.sty
├── acl_natbib.bst
├── content
│   ├── abstract.tex
│   ├── approach-bert.tex
│   ├── approach-parser.tex
│   ├── approach-preprocess.tex
│   ├── approach-remote.tex
│   ├── approaches.tex
│   ├── conclusions.tex
│   ├── exp.tex
│   ├── intro.tex
│   ├── language-emb.tex
│   └── not-used
│       ├── approach-pred.tex
│       └── approach-train.tex
├── image
│   ├── fig.tex
│   ├── model.tex
│   ├── sample.tex
│   ├── tree.tex
│   └── ucca-example.tex
├── main.aux
├── main.bbl
├── main.blg
├── main.log
├── main.out
├── main.pdf
├── main.tex
└── tikz-dependency.sty
```
其中有一些为编译生成的文件，提交时会自动忽略。
