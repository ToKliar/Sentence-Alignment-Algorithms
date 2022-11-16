# 双语对齐算法调研

**对齐算法**：给定双语语料，在所有可能的对齐中找到概率最大的对齐

句子对齐的方法可以分为以下四类：

+ 基于长度的句子对齐算法
+ 基于词典的句子对齐算法
+ 基于长度和词典结合的句子对齐算法
+ 基于机器学习和深度学习的句子对齐算法

## 基于长度的句子对齐算法

核心思想：源语言文本的长度与译文长度有很强的相关性

可以分为以下几种：

+ 基于词数长度的对齐（Brown）
+ 基于字符数长度的对齐（Gale & Church）
+ 其他基于长度的对齐方法

### 基于长度对齐方法

将句子对齐看成是句长的函数，根据句长的统计信息计算不同模式句子对齐的概率

使用动态规划算法计算最大概率的句子对齐模式

优点：不需要额外的词典信息

缺点：鲁棒性差，容易造成错误的蔓延

### 基于词数长度的对齐

Brown提出的句子对齐算法中引入**锚点**（anchor）的概念将语料划分为小的片段

采用语料中特定的注释作为锚点，使用动态规划算法对锚点进行匹配

匹配之后锚点之间的文本能够一一对应，形成对齐文本

这种锚点方法不适用于一般情况

### 其他基于长度的方法

Fung通过统计文本中词频和词的位置，将高频的互译词汇作为候选锚点

利用动态规划算法对候选锚点进行匹配，找出真正的锚点

缺点：需要对所有词汇进行统计，计算量很大；由于数据稀疏的问题，可能导致锚点匹配错误

## 基于词典的句子对齐算法

核心思想：最佳的句子对齐是使系统词汇对齐数量最大的句子对齐。优点：相对可靠精确

缺点：计算复杂，费时，且未证明该方法对于大型语料库的适用性

### Kay和Roscheisen的句子对齐算法

使用词语级别的部分对齐推导出句子级别的对齐的最大似然估计，反过来优化词语对齐

假设：如果两个词语的分布是相同的，那么它们是对齐的

将双语文本的首句和尾句作为初始锚点，构建句对集合

选取句对同现的词对，词对中两个词分布模型相似

寻找包含很多同现词对的双语句对，作为锚点，重复直到所有句子对齐

### 扩展

运用词汇信息构建了一对一词汇统计翻译模型进行句子对齐（Chen 1993)

基于词典方法的另一种做法是利用同源词(cognate)（Church,1993）

## 基于长度和词典结合的句子对齐算法

基于长度的句子对齐算法和基于词汇的句子对齐算法各有优缺点

将各种方法混合构建新的句子对齐算法，在大部分场景下优于其中的任何一种方法

如：Melamed，2000；Collier，1998等

## 基于机器学习和深度学习的方法

### 基于机器学习的方法

将机器学习的基于特征的分类思想引入句子对齐任务

以文本长度、特殊标点、同源词、词典匹配、词共现等作为特征使用机器学习模型进行分类实现句子对齐

代表工作：Fattah 2007；Fattah 2012；刘颖 2013；刘颖 2015

### 基于深度学习的方法

方法一：通过机器翻译的结果进行对齐（Bleualign）

方法二：通过embedding方法将句子转换为词向量，进行句子相似度计算，将语义相似的句子对齐（Vecalign）

## 参考文献

[1] Peter F. Brown, Jennifer C. Lai, and Robert L. Mercer.1991. Aligning sentences in parallel corpora. 

[2] William A. Gale and Kenneth W. Church. 1993. A program for aligning sentences in bilingual corpora. 

[3] Martin Kay and Martin Roscheisen. 1993. Text-Translation Alignment.

[4] Fung P. and Church. 1994.  A new approach foraligning parallel texts.

[5] Chen S. 1993. Aligning sentences in bilingual corpora using lexical information.

[6] Church L.W. 1993. Char_align: program for aligning paralleltexts at the character level.

[7] Melamed, I.D. 2000. Models of Transnational Equivalenve among Words.

[8] Collier N. , Ono K. and Hirakawa H. 1998. An Experimentin Hybrid Dictionary and Statistical sentence alignment.

[9] Robert C. Moore. 2002. Fast and accurate sentence alignment of bilingual corpora.

[10] Fattah M A, Bracewell D B, Ren F J, et al. 2007. Sentence Alignment Using P-NNT and GMM

[11] Fattah M A. 2012. The Use of MSVM and HMM for Sentence Alignment.
Alignment[

[11] 刘颖, 王楠 . 2012. 古汉语与现代汉语句子对齐研究.

[12] 刘颖, 王楠. 2015. 最大熵模型和BP神经网络的短句对齐比较.

[13] Rico Sennrich and Martin Volk. 2011. Iterative, MT-based Sentence Alignment of Parallel Texts.

[14] Brian Thompson and Philipp Koehn. Vecalign: Improved Sentence Alignment in Linear Time and Space
