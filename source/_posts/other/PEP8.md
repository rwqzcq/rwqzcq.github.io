---
title: 'PEP-8: Python代码规范'
date: 2022-06-15 14:40:06
tags:
 - 其他
categories:
 - 其他
---

# 目前写代码出现的问题

1. 函数命名问题：语义不清晰
    - 别人看不懂自己的命名
    - 过了一段时间自己看不懂自己的命名

# 代码缩进

> Continuation lines should align wrapped elements either vertically using Python’s implicit line joining inside parentheses, brackets and braces, or using a hanging indent [1]. When using a hanging indent the following should be considered; there should be no arguments on the first line and further indentation should be used to clearly distinguish itself as a continuation line

> 续行应该垂直对齐包裹的元素，可以使用Python的隐式行连接内括号、括号和大括号，也可以使用悬挂缩进。使用悬挂缩进时，应考虑以下事项：；第一行上不应有任何参数，应使用进一步的缩进，以清楚地将其本身区分为连续行

> Python会将 圆括号, 中括号和花括号中的行隐式的连接起来

## 函数

```python
# 正确写法1: 每行两个参数，参数与参数之间对齐
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# 正确写法2: 添加4个空格（额外的缩进级别）以区分参数和其他参数
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# 正确写法3: 悬挂缩进应添加一个级别
def long_function_name(
    var_one, var_two,
    var_three, var_four):

# 错误写法1: 第二行函数参数没有跟第一行对齐; 函数括号另起了一行
foo = long_function_name(var_one, var_two,
                        var_three, var_four
)

# 错误写法2: 不使用垂直对齐时，第一行上的参数被禁止
foo = long_function_name(var_one, var_two, 
    var_three, var_four)

# 错误写法3: 由于压痕无法区分，需要进一步缩进
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

> 函数命名以`正确写法3为主`。不要让括号独占一行。

## if语句

When the conditional part of an if-statement is long enough to require that it be written across multiple lines, it’s worth noting that the combination of a two character keyword (i.e. if), plus a single space, plus an opening parenthesis creates a natural 4-space indent for the subsequent lines of the multiline conditional. This can produce a visual conflict with the indented suite of code nested inside the if-statement, which would also naturally be indented to 4 spaces. This PEP takes no explicit position on how (or whether) to further visually distinguish such conditional lines from the nested suite inside the if-statement. Acceptable options in this situation include, but are not limited to:

> 当if语句的条件部分足够长，需要跨多行写入时，值得注意的是，两个字符的关键字（即if）加上一个空格，再加上一个左括号的组合会为多行条件语句的后续行创建一个自然的4空格缩进。这可能会与嵌套在if语句中的缩进代码集产生视觉冲突，这自然也会缩进到4个空格。对于如何（或是否）进一步直观地将这些条件行与if语句中的嵌套套件区分开来，该PEP没有明确的立场。

```python
# 正确写法1: 没有多余缩进, 前后对齐
if (this_is_one_thing and 
    that_is_another_thing):
    pass

# 正确写法2: and在第二行, 同时再次缩进
if (this_is_one_thing
        and that_is_another_thing):
    pass

```

## 每一行最大字符数

- Limit all lines to a maximum of `79` characters.
- For flowing long blocks of text with fewer structural restrictions (`docstrings or comments`), the line length should be limited to `72` characters.

- The preferred way of wrapping long lines is by using Python’s implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses. These should be used in preference to using a backslash for line continuation.

> 包装长行的首选方法是在括号、括号和大括号内使用Python的隐含行继续。通过将表达式括在括号中，可以在多行上打断长行。应优先使用这些选项，而不是使用反斜杠作为行延续。

## 二元运算符

```python
# 正确写法: 加括号, 换行后运算符写在前面, 与第一个参数对齐
income = (gross_wages 
          + taxable_interst
          + (dividents - qualified_dividents)
          - ira_deducation
          - student_loan_interst)
```

# 表达式中空格的使用

```python
# 正确写法:
foo = (0,)

# 错误写法
foo = (0, )
```

> 在元祖中，只有一个元素的时候禁止在逗号后面写空格！

```python
# 正确写法:
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
ham[lower:upper], ham[lower:upper:], ham[lower::step]
ham[lower+offset : upper+offset]
ham[lower + offset : upper + offset]

# 错误写法:
ham[1: 9], ham[1: 9: 3], ham[: 9: 3], ham[1 :: 3]
```
> 在进行列表切片操作的时, 常数不要出现空格, 有表达式的时候表达式中不要有空格，切片运算符`:`要有空格

# 编程建议

## 判断一个集合(list, tuble, str)是否为空

```python
# 正确写法
if not s:
    pass
if s:
    pass

# 错误写法
if len(s):
    pass
```

## 与true, false比较

> Don’t compare boolean values to True or False using ==:

```python
# 正确写法: 什么都不写
if greeing:
    pass

# 错误写法
if greeting == True:
    pass

# 错误写法
if greeting is False:
    pass
```

> `is True`这样的不要用, is运算符是用来`比较判断的是对象间的唯一身份标识`

# 参考链接
- https://peps.python.org/pep-0008/#introduction
- https://www.jianshu.com/p/8b6c425b65a6
- https://www.runoob.com/w3cnote/google-python-styleguide.htmly


