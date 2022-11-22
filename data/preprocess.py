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

        sentence=re.split('[。|？|！]',line.strip())
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


# for title in (data):
#     with open(dir+title+'.txt','w',encoding='utf-8') as f:
#         for line in data[title]:
#             f.write(line+'\n')

# with open(dir + "src.txt", 'w', encoding='utf-8') as f:
#     f.writelines(data_src)

# with open(dir + "tgt.txt", 'w', encoding='utf-8') as f:
#     f.writelines(data_tgt)

print(src_line, tgt_line)
for i in range(len(src_para_len)):
    if src_para_len[i] != tgt_para_len[i]:
        print("para {} src {} tgt {}".format(i + 1, src_para_len[i], tgt_para_len[i]))