---
layout: post
title:  "如何配置vscode的remote服务器以及git"
categories: tools
tags:  tools
excerpt: 记录使用vscode的配置
author: wjiang
---

* content
{:toc}

## 提要

本文记录如何配置vscode remote的方法，以及如何在公用服务器上配置git。之前一直使用sftp作为同步方法，但是最近的一个服务器sftp无法连接,而且remote用的也越来越多，所以在此记录一下配置方法。

## 配置vscode remote
第一步：首先确保本机已经生成SSH Key，用户主目录下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果已经有了，可直接跳到下一步。如果没有，如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：

```shell
$ ssh-keygen -t rsa -C "767257113@qq.com"
```

如果一切顺利的话，可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。

第二步：复制SSH Key。打开Shell（Windows下打开Git Bash），复制SSH Key：

```shell
$ ssh-copy-id LaGroup@192.168.126.143
```

如果你在本机有多个SSH Key，那么可能会出现问题，最简单的方法是把所有key都拷贝到服务器：

```shell
$ ssh-copy-id -i /c/Users/jw/.ssh/id_rsa.pub LaGroup@192.168.126.143
```

做好如上准备工作后，我们需要配置vscode。首先安装remote插件，我们点击左侧remote的菜单栏进入remote界面。

![1](/src/2019-10-25-vscode-remote/1.png)

点击+号按钮，
根据提示输入服务器端地址，最后选择配置文件即可。此时应当连接服务器正常。

![2](/src/2019-10-25-vscode-remote/2.png)


## 配置服务器端git

由于服务器是多人共用，所以配置全局的git会有问题，所以要确保每个人使用自己的账号方法如下：

首先生成SSH Key，同时在github账号上添加:

```shell
ssh-keygen -t rsa -C '767257113@qq.com' -f ~/.ssh/id_rsa.wjiang
```

然后在.ssh下创建一个config
在该config中添加如下：
```shell
Host github.wjiang
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa.wjiang
```

对于一个仓库：

```shell
cd repos
git config user.name hmjw
git config user.email '767257113@qq.com'
git remote remove origin
git remote add origin git@github.wjiang:hmjw/repos.git
git fetch
```