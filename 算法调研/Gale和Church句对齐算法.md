# Gale & Church句对齐算法原理

Gale & Church算法的核心思想为源语言文本的长度与译文长度有很强的相关性

将句子对齐看成是句长的函数，根据句长的统计信息计算不同模式句子对齐的概率

算法基于动态规划算法，可以将其动态规划原理和LevenShtein算法的原理进行对比

## 概念

* **句子** ：一个短的字符串。
* **段落** ：自然段，由一个连续的句子序列组成
* **片段** ：一个连续的句子序列，是段落的子集
* **片段对** ：双语文本片段组成的对
* **对齐模式** ：或称匹配模式，描述一个片段对由几个原文句子和几个译文句子组成
* **match**：对齐模式的概率分布
* **距离**：度量片段对中两个片段之间对齐的概率
* **片段对序列**：对于双语文本段落的划分
* **距离和**：片段对序列中所有片段对的距离的和
* **对齐序列**：距离和最小的片段对序列

## 句子编辑操作

与LevenShtein中的字符串编辑距离相似，对于句子的编辑操作可以是

将双语对齐中某个语言的文本定义为源文本，其中的句子定义为源句；另一个语言的文本为目标文本，句子定义为目标句

+ 删除 ：一个源句，没有对应的目标句
+ 插入 ： 一个目标句，没有对应的源句
+ 替换 ：一对相互对应的源句和目标句 1-1（理想情况下，最常见的情况）

此外，Gale & Church定义了其他句子编辑操作

+ 缩减 ：两个源句对应于一个目标句
+ 扩展 ：一个源句对应于两个目标句
+ 合并 ：两个源句对应于两个目标句（但没有1-1的对应关系，可以理解为两个目标句中每个都有两个源句的部分内容）

## 距离计算

### 距离估计

Gale & Church通过观察认为，双语匹配的句子长度（字符数）的比值呈现正态分布

$c$为双语句子长度的平均比值（对于0值，让c=1），$s^2$为方差

$l_{1}$，$l_{2}$分别为源句和目标句的长度

定义$\delta =(l_{2}-l_{1}c)/{\sqrt {l_{1}s^{2}}}$，$\delta$是一个零均值、单位方差、正态分布的随机变量

根据贝叶斯法则,基于$\delta$来定义距离和度量match

可知 $P(match| \delta ) \propto P(\delta |match) \cdot P(match)$

Gale & Church 根据数据估计先验概率 $P(match)$，可以参考论文中的Table 5

而 $P(\delta | match) = 2(1 - P(|\delta|))$

$P(|\delta|)$是0-均值、单位方差正态分布，基于$\delta$的累积分布函数

$P(\delta) = \frac{1}{\sqrt{2 \pi}} \int_{-\infty}^{\delta} e^{-z^2/2} {\rm d}z$

### 距离函数定义

Gale & Church对于距离函数d的定义如下

+ $d(x_1, y_1; 0, 0)$ 替换$x_1$和$y_1$的代价
+ $d(x_1, 0; 0, 0)$ 删除$x_1$的代价
+ $d(0, y_1; 0, 0)$ 删除$y_1$的代价
+ $d(x_1, y_1; x_2, 0)$ 将$x_1$、$x_2$缩减到$y_1$的代价
+ $d(x_1, y_1; 0, y_2)$ 将$x_1$扩展到$y_1$和$y_2$的代价
+ $d(x_1, y_1; x_2, y_2)$ 将$x_1$、$x_2$和$y_1$、$y_2$合并的代价

## 动态规划算法

定义$D(i, j)$定义为句子序列$s_1,...,s_i$和$t_1,...,t_j$的最小距离和

$D(i,j)$初始化为0

动态规划算法的递推方式如下，按照这种方法找到最小的距离和与对应的片段对序列

每次更新D(i,j)，记录对应操作的片段对长度：0-1，1-0，1-1，1-2，2-1，2-2

$$
D(i,j) = min
\begin{cases}
D(i,j-1) + d(0,y_j,0,0) \\
D(i-1,j) + d(x_i,0,0,0) \\
D(i-1,j-1) + d(x_i,y_j,0,0) \\
D(i-1,j-2) + d(x_i,y_j,0,y_{j-1}) \\
D(i-2,j-1) + d(x_i,y_j,x_{i-1},0) \\
D(i-2,j-2) + d(x_i,y_j,x_{i-1},y_{j-1}) \\
\end{cases}
$$

## 代码实现

见[实现](./Gale_Church.py)的代码（python）
