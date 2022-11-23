from collections import defaultdict
import re
import os

dir = 'paragraph/'
file_dir = './资治通鉴/text'
files = os.listdir(file_dir)

kind = 1
data = []

src_data=[]
tgt_data=[]
num_sum = 0
begin = -1

def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

for file in files:
    file_path = file_dir + "/" + file
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()      
            if line == '':
                continue
            if re.match('<p class="calibre2">.*</p>', line):
                line = line[20:-4]
                sentences=cut_sent(line)

                for i, sentence in enumerate(sentences):
                    if sentence == "":
                        continue
                    if re.match(r'.*年.*[（|(].*\d+.*[）|)]', sentence):
                        num_sum += 1
                        num = re.findall(r'\d+', sentence)[0]
                        if kind == 0:   
                            if begin != -1:
                                src_data.append(data)
                            else:
                                begin = 0
                        else:
                            if begin != -1:
                                tgt_data.append(data)
                            else:
                                begin = 0
                        kind = 1 - kind
                        data = []
                    data.append(sentence)
                # data.append(line)

if kind == 0:
    src_data.append(data)
else:
    tgt_data.append(data)

for i in range(len(src_data)):
    with open("paragraph/{}_src.txt".format(i+1), "w", encoding="utf-8") as f:
        for line in src_data[i]:
            f.write(line + '\n')
    with open("paragraph/{}_tgt.txt".format(i+1), "w", encoding="utf-8") as f:
        for line in tgt_data[i]:
            f.write(line + '\n')