import scipy.stats
import math
import re
from tqdm import tqdm

match = {(1,1): 0.901577143566071,
        (1,2): 0.04752728081012763,
        (2,1): 0.040147634284650895,
        (2,2): 0.003269044874412642}

c = 1.518482311924114
var = 2.6296565142276704

pre = re.compile(u'[\u4e00-\u9fa5]')

def prob_delta(delta):
    return scipy.stats.norm(0,1).cdf(delta)

# 计算片段的长度特征
def l_distance(partition1, partition2):
    l1 = sum(len(sentence) for sentence in partition1)
    l2 = sum(len(sentence) for sentence in partition2)
    if l1 == 0:
        return float('inf')
    
    delta = (l2 - l1 * c) / math.sqrt(l1 * var)
    
    prob_delta_match = 2 * (1 - prob_delta(abs(delta))) # P(\delta | match) = 2 * (1 - P(|\delta|))
    if prob_delta_match <= 0:
        return 10 ** 24
    return -100 * math.log(prob_delta_match)

# 计算片段的句子对齐特征
def m_distance(match_prob):
    return -100 * math.log(match_prob)

def h_distance1(i, u):
    set_1 = set("".join(re.findall(pre, i)))
    set_2 = set("".join(re.findall(pre, u)))
    return len(set_1 & set_2) / min(len(set_1), len(set_2))

def h_distance2(i, u, j):
    set_1 = set("".join(re.findall(pre, i)))
    set_2 = set("".join(re.findall(pre, u)))
    set_3 = set("".join(re.findall(pre, j)))
    return (len(set_2 & set_3) - len(set_1 & set_2 & set_3)) / len(set_3)

def h_distance3(i, u, v):
    set_1 = set("".join(re.findall(pre, i)))
    set_2 = set("".join(re.findall(pre, u)))
    set_3 = set("".join(re.findall(pre, v)))
    return (len(set_1 & set_3) - len(set_1 & set_2 & set_3)) / len(set_3)

# 计算片段的共现汉字特征
def h_distance(partition1, partition2, d1, d2):
    if len(partition1) != d1 or len(partition2) != d2:
        return 10 ** 8
    if d1 == 1:
        if d2 == 1:
            return h_distance1(partition1[0], partition2[0])
        elif d2 == 2:
            return h_distance1(partition1[0], partition2[0]) + h_distance3(partition1[0], partition2[0], partition2[1])
    elif d1 == 2:
        if d2 == 1:
            return h_distance1(partition1[0], partition2[0]) + h_distance2(partition1[0], partition2[0], partition1[1])
        elif d2 == 2:
            h_dis_1 = h_distance1(partition1[0], partition2[0]) + h_distance2(partition1[0], partition2[0], partition1[1]) + h_distance1(partition1[1], partition2[1])
            h_dis_2 = h_distance1(partition1[0], partition2[0]) + h_distance3(partition1[0], partition2[0], partition2[1]) + h_distance1(partition1[1], partition2[1])
            h_dis_3 = h_distance1(partition1[0], partition2[1]) + h_distance1(partition1[1], partition2[0])
            return min(h_dis_1, min(h_dis_2, h_dis_3))
    return 10 ** 8

def distance(partition1, partition2, match_prob, d1, d2):
    return l_distance(partition1, partition2) + m_distance(match_prob) + h_distance(partition1, partition2, d1, d2)

# 句子对齐
def align(paragraph1, paragraph2):
    align_dp = [[(10 ** 24, 0, 0) for j in range(len(paragraph2) + 1)] for i in range(len(paragraph1) + 1)]
    for i in tqdm(range(len(paragraph1) + 1)):
        for j in range(len(paragraph2) + 1):
            if i == j and i == 0:
                align_dp[0][0] = (0, 0, 0) 
            else:
                align_dp[i][j] = (float('inf'), 0, 0)
                for (di, dj), match_prob in match.items():
                    if i - di >= 0 and j - dj >= 0:
                        align_dp[i][j] = min(align_dp[i][j], (align_dp[i-di][j-dj][0] + distance(paragraph1[i-di:i], paragraph2[j-dj:j], match_prob, di, dj), di, dj))
    
    segment_seq = []
    x, y = len(paragraph1), len(paragraph2)
    while True:
        (c, dx, dy) = align_dp[x][y]
        if dx == dy and dx == 0:
            break
        segment_seq.append(["".join(paragraph1[x-dx:x]), "".join(paragraph2[y-dy:y]), dx, dy])
        x -= dx
        y -= dy
    return segment_seq

src_paragraph = []
tgt_paragraph = []

with open("1_src.txt", "r", encoding="utf-8") as f:
    src_paragraph = f.readlines()
    src_paragraph = [line.strip("\n") for line in src_paragraph] 

with open("1_tgt.txt", "r", encoding="utf-8") as f:
    tgt_paragraph = f.readlines()
    tgt_paragraph = [line.strip("\n") for line in tgt_paragraph] 

print(len(src_paragraph))
print(len(tgt_paragraph))
seq = align(src_paragraph, tgt_paragraph)
seq.reverse()
with open("result", "w", encoding="utf-8") as f:
    for line in seq:
        f.write(str(line) + "\n")

