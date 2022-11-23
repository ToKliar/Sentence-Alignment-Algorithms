from collections import defaultdict
import re
import os

file_dir = 'c:/Users/12247/Desktop/软微课程/翻译技术/第二次作业/Sentence_Alignment_Algorithms/data/太平广记/OEBPS'
files = os.listdir(file_dir)

kind = 1
data = []
src_data=[]
tgt_data=[]

# 中文分句
def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

src = []
tgt = []
src_data = ""
tgt_data = ""

p = re.compile(r'[\u3002\uff1b\uff0c\uff01\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]') # 提取中文句子

begin = False
src_kind = -1
tgt_kind = -1
for file in files:
    file_path = file_dir + "/" + file
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        length = len(lines)
        i = 0
        while i < length:
            line = lines[i].strip()
            line = line.strip("\n")      
            if line == '':
                i += 1
                continue
            if line.startswith("<h4"):
                begin = True
            

            if begin == False:
                i += 1
                continue

            if re.match('<h4 id="par.* class="txtheading-2-c">.*</h4>', line):
                if src_kind != -1:
                    src.append(cut_sent(src_data))
                    src_data = ""
                src_kind = 0
            elif re.match('<h4 class="txtheading-2-c" id="par.*">.*</h4>', line):
                if tgt_kind != -1:
                    tgt.append(cut_sent(tgt_data))
                    tgt_data = ""
                tgt_kind = 1
            elif i > 0 and re.match('<b>.*</b>', line):
                if re.match('<p class="bodyContent-1-c">', lines[i-1]) or re.match('<p class="noindent-bodyContent-1-c-top">', lines[i-1]):
                    if tgt_kind != -1:
                        tgt.append(cut_sent(tgt_data))
                        tgt_data = ""
                    tgt_kind = 1
            elif re.match('<p class=".*bodyContent-1-kaiti">.*', line):
                lines[i] = lines[i].strip()
                lines[i] = lines[i].strip("\n")   
                while i < length and lines[i].endswith("</p>") == False:
                    lines[i] = re.sub('<span class=.*</span>', "", lines[i])
                    tgt_data += "".join(p.findall(lines[i]))
                    i += 1
                    lines[i] = lines[i].strip()
                lines[i] = lines[i].strip("\n")   
                tgt_data += "".join(p.findall(lines[i]))
            elif re.match('<p class=".*bodyContent-1">.*', line):
                lines[i] = lines[i].strip()
                lines[i] = lines[i].strip("\n")   
                while i < length and lines[i].endswith("</p>") == False:
                    lines[i] = re.sub('<span class=.*</span>', "", lines[i])
                    src_data += "".join(p.findall(lines[i]))
                    i += 1
                    lines[i] = lines[i].strip()
                    lines[i] = lines[i].strip("\n")   
                src_data += "".join(p.findall(lines[i]))
            i += 1
        src.append(cut_sent(src_data))
        tgt.append(cut_sent(tgt_data))

for i in range(len(src)):
    with open("paragraph/{}_src.txt".format(i+1), "w", encoding="utf-8") as f:
        for line in src[i]:
            f.write(line + "\n")
    with open("paragraph/{}_tgt.txt".format(i+1), "w", encoding="utf-8") as f:
        for line in tgt[i]:
            f.write(line + "\n")
           