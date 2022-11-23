from collections import defaultdict
import re

dir='paragraph/'
filename='文心雕龙.txt'

data=defaultdict(list)
data_src = []
data_tgt = []

src_line = 0
tgt_line = 0
src_para_len = []
tgt_para_len = []

def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

with open(filename,encoding='utf-8') as file:
    src_index=1 
    tgt_index=1 
    for line in file:
        if line.strip()=='':
            continue
        if re.match(r"..第.?",line):
            flag=True #为True时表示原文 为False表示译文
            continue

        if re.match(r"【译文】",line):
            flag=False
            continue

        sentence=cut_sent(line.strip())
        sentence.pop() #去掉split在句子最后产生的空字符串
        if flag:
            title = "{}_src".format(src_index)
            src_index += 1
            data[title]+=sentence
            src_line += len(sentence)
            src_para_len.append(len(sentence))
            data_src += [line + "\n" for line in sentence]
        else:
            title = "{}_tgt".format(tgt_index)
            tgt_index += 1
            data[title]+=sentence
            tgt_line += len(sentence)
            data_tgt += [line + "\n" for line in sentence]
            tgt_para_len.append(len(sentence))


for title in (data):
    with open(dir+title+'.txt','w',encoding='utf-8') as f:
        for line in data[title]:
            f.write(line+'\n')

with open(dir + "src.txt", 'w', encoding='utf-8') as f:
    f.writelines(data_src)

with open(dir + "tgt.txt", 'w', encoding='utf-8') as f:
    f.writelines(data_tgt)
