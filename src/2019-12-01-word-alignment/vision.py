import argparse
import codecs
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

plt.rcParams['font.sans-serif'] = ['STFangsong']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def read_lines(filename):
    result = []
    with codecs.open(filename, 'r',encoding= u'utf-8',errors='ignore') as f:
        for line in f:
            result.append(line.strip().split())
    return result

def write_lines(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        if isinstance(lines, list):
            for line in lines:
                f.write(line)
                f.write("\n")
        elif isinstance(lines, str):
            f.write(lines)
            f.write("\n")

def transform_align(alignment, left_length, right_length):
    matrix = np.zeros((left_length, right_length), dtype=np.long)
    alignment = [x.split("-") for x in alignment]
    alignment = map(lambda x: (int(x[0]), int(x[1])), alignment)
    alignment = tuple(zip(*alignment))
    matrix[alignment] = 1
    return matrix

def vision(source, target, alignment):
    raws = source
    column = target
    alignment = transform_align(alignment, len(source), len(target))

    df = pd.DataFrame(alignment, columns=column, index=raws)

    fig = plt.figure()

    ax = fig.add_subplot(111)

    cax = ax.matshow(df, interpolation='nearest', cmap='hot_r')
    #cax = ax.matshow(df)
    fig.colorbar(cax)

    tick_spacing = 1
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.set_xticks(np.arange(len(column)) + 0.5, minor=True)  # Grid lines
    ax.set_yticks(np.arange(len(raws)) + 0.5, minor=True)
    ax.xaxis.grid(True, which='minor')
    ax.yaxis.grid(True, which='minor')

    # fontdict = {'rotation': 'vertical'}    #设置文字旋转
    fontdict = {'rotation': 90}       #或者这样设置文字旋转
    #ax.set_xticklabels([''] + list(df.columns), rotation=90)  #或者直接设置到这里
    # Axes.set_xticklabels(labels, fontdict=None, minor=False, **kwargs)
    ax.set_xticklabels([''] + list(df.columns), fontdict=fontdict)
    ax.set_yticklabels([''] + list(df.index))

    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="reranking")
    parser.add_argument(
        "--src_file", "-s", default="./toy.ch", help="src file"
    )
    parser.add_argument(
        "--tgt_file", "-t", default="./toy.en", help="tgt file"
    )
    parser.add_argument(
        "--alignment_file", "-a", default="./final_alignment.out", help="alignment_file"
    )

    parser.add_argument(
        "--num", "-n", default=0, help="alignment_file", type=int
    )

    args = parser.parse_args()

    alignments = read_lines(args.alignment_file)
    source = read_lines(args.src_file)
    target = read_lines(args.tgt_file)

    assert len(alignments) == len(source) == len(target)
    vision(source[args.num], target[args.num], alignments[args.num])
