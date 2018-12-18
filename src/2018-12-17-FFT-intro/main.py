import math
import random
import string
pi = math.pi

def euler_formula(x):
    # 欧拉公式
    return complex(math.cos(x), math.sin(x))

def root_w(n, k):
    # 单位根
    return euler_formula(2 * pi * k / n)
    
def FFT(a, reverse=False):
    # 递归版本FFT；若reverse=True则为逆FFT
    n = len(a)
    if n == 1:
        return a
    w_n = root_w(n, 1) if not reverse else root_w(n, -1) # w^1_{n}和w^-1_{n}
    w = 1

    # divide
    a_even = [a[i] for i in range(0, n, 2)] # 取出偶数位系数a
    a_odd = [a[i] for i in range(1, n, 2)]  # 取出奇数位系数a
    y_even = FFT(a_even, reverse) # 递归对A^0(x)做FFT
    y_odd = FFT(a_odd, reverse) # 递归对A^1(x)做FFT

    # conquer
    y = [0] * n
    for i in range(0, n//2):
        y[i] = y_even[i] + w * y_odd[i] # 根据消去引理
        y[i + n//2] = y_even[i] - w * y_odd[i] # 根据折半原理
        w = w * w_n
    return y

def pad(string, pad_len):
    # 将字符串转化为多项式系数，以10作为x，长度为pad_len
    return [int(string[i]) if i >=0 else 0 for i in range(len(string)-1, len(string)-pad_len-1, -1)]

def mutiply(string1, string2):
    # 取保长度为2的次幂
    maxlen = len(string1) if len(string1) > len(string2) else len(string2)
    pad_len = 1
    while pad_len < maxlen:
        pad_len *= 2
    pad_len *= 2
    # 转化为多项式系数[a]
    a1 = pad(string1, pad_len)
    a2 = pad(string2, pad_len)
    # 用FFT求得A(x)和B(x)
    A , B = FFT(a1), FFT(a2)
    # 对应相乘求得C(x)
    C = [x * y for x, y in zip(A, B)]
    # 逆FFT求得系数a
    a = FFT(C, reverse=True)
    # 取整
    a = [int(x.real/pad_len+0.5) for x in a]
    # 进位
    for i in range(0, len(a)-2):
        a[i+1] += a[i] // 10
        a[i] = a[i] % 10
    # 去掉高位多余的0
    pointer = len(a) - 1
    while(a[pointer] == 0):
        pointer -= 1
        if pointer < 0:
            return '0'
    return ''.join(reversed([str(x) for x in a[:pointer+1]]))


if __name__ == '__main__':
    # 随机生成100位的整数,最高位不能为0
    string1 = random.sample('123456789',1)[0] + ''.join(map(lambda x:random.choice('0123456789'), range(99)))
    string2 = random.sample('123456789',1)[0] + ''.join(map(lambda x:random.choice('0123456789'), range(99)))
    print(string1 + ' * '+ string2 + '=' + mutiply(string1, string2))