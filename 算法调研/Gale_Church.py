import math
import scipy.stats

# 因为没有切实的数据，下面的数据来源于网络

# 基于统计的方法计算先验概率分布
match = {(1, 0): 0.023114355231143552,  
         (1, 2): 0.0012165450121654502, 
         (2, 2): 0.006082725060827251, 
         (2, 1): 0.0006082725060827251, 
         (1, 1): 0.9422141119221411, 
         (0, 1): 0.0267639902676399}

# 双语文本长度比值的均值
c = 1.467

# 双语文本长度比值的方差
s2 = 6.315

# 计算P(\delta)
def prob_delta(delta):
    return scipy.stats.norm(0,1).cdf(delta)

# 计算片段的距离函数
def distance(partition1, partition2, match_prob):
    l1 = sum(len(sentence) for sentence in partition1)
    l2 = sum(len(sentence) for sentence in partition2)

    if l1 == 0:
        return float('inf')
    
    delta = (l2 - l1 * c) / math.sqrt(l1 * s2)
    prob_delta_match = 2 * (1 - prob_delta(abs(delta))) # P(\delta | match) = 2 * (1 - P(|\delta|))
    return - math.log(prob_delta_match) - math.log(match_prob)

# 句子对齐
def align(paragraph1, paragraph2):
    align_dp = [[(0, 0, 0) for j in range(len(paragraph2) + 1)] for i in range(len(paragraph1) + 1)]
    for i in range(len(paragraph1) + 1):
        for j in range(len(paragraph2) + 1):
            if i == j and i == 0:
                align_dp[0][0] = (0, 0, 0) 
            else:
                align_dp[i][j] = (float('inf'), 0, 0)
                for (di, dj), match_prob in match.items():
                    if i - di >= 0 and j - dj >= 0:
                        align_dp[i][j] = min(align_dp[i][j], (align_dp[i-di][j-dj][0] + distance(paragraph1[i-di:i],paragraph2[j-dj:j],match_prob), di, dj))
    
    segment_seq = []
    x, y = len(paragraph1), len(paragraph2)
    while True:
        (c, dx, dy) = align_dp[x][y]
        if dx == dy and dx == 0:
            break
        segment_seq.append(["".join(paragraph1[x-dx:x]), "".join(paragraph2[y-dy:y])])
        x -= dx
        y -= dy

