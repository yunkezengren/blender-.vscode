



# isect 是 (相交, 交集) 这个单词的常见缩写
isect = "intersection"

# rctf: 一个矩形 (Rectangle).
rct = "rectangle"


RAII = "Resource Acquisition Is Initialization"

RAII = "RESOURCE_ACQUISITION_IS_INITIALIZATION"
RAII = "resource_acquisition_is_initialization"
RAII = "Resource Acquisition Is Initialization"

# 写一个斐波那契数列函数递归,
# 加上type hint
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# 写一个斐波那契数列函数迭代
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
