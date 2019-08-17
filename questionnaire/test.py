# 1.分数出现以下情况怎么处理没有列出来:
# （一共有R、I、A、S、E、C）
# （假设R=I>A>S>E>C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R=I=A>S>E>C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R=I=A=S>E>C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R=I=A=S=E>C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R=I=A=S=E=C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R>I>A>S>E>C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R>I=A=S=E=C）
# 需要显示的结果是什么，以及如何判断得出该结果的
# （假设R>I>A=S=E=C）
# 需要显示的结果是什么，以及如何判断得出该结果的

import itertools

# 重复的排列组合
# for i in itertools.product([1,2,3,4,5],repeat= 3):
#     print(i)
# 不重复的排列组合
# for i in itertools.permutations((1,2,3),1):
#     print(i)
for i, j in [[1,2,3,4,5], [6,7,8,9,1]]:
    print(i, j)
# def fun1(s=''):
#     if len(s)<=1:
#         return [s]
#     sl=[]
#     for i in range(len(s)):
#         for j in fun1(s[0:i]+s[i+1:]):
#             sl.append(s[i]+j)
#     return sl

# print(fun1('a'))
# print(fun1('cde'))
# print(fun1('yiop'))
# print(fun1('cd'))
