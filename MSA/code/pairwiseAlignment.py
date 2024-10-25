import suffixtree as sf
import numpy as np
from collections import Counter

# 일치 / 불일치/ 갭 ㄷ읃으 점수 할당 
match_score = 1
mismatch_penalty = -1
gap_penalty = -1

def needleman_wunsch(seq1, seq2):
    n = len(seq1)
    m = len(seq2)
    
    
    seq1_ori = seq1[:]
    seq2_ori = seq2[:]
    
    #profile이라면 , motif만들기
    
    if (len(seq1[0]) > 1):
        i = 0
        for pos in seq1:
            counter = Counter(pos)
            most = counter.most_common(1)[0][0]
            seq1[i] = [most]
            i += 1
    
    if (len(seq2[0]) > 1):
        i = 0
        for pos in seq2:
            counter = Counter(pos)
            most = counter.most_common(1)[0][0]
            seq2[i] = [most]
            i += 1
    
    
    
    
    #점수 행렬 생성 
   
    score_matrix = np.zeros((n + 1, m + 1), dtype=int)
    
    
    # 1열 , 1행 - 갭 페널티로 초기화
    for i in range(1, n + 1):
        score_matrix[i][0] = gap_penalty * i
    for j in range(1, m + 1):
        score_matrix[0][j] = gap_penalty * j

    # 행렬 돌면서 조건에 따라 점수 행렬 채우기
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diagonal = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            up = score_matrix[i-1][j] + gap_penalty
            down = score_matrix[i][j-1] + gap_penalty
            score_matrix[i][j] = max(diagonal, up, down)

    # 최대 점수 경로 역추적
    align1, align2 = [], []
    i, j = n, m
    
    #대각선, 위, 아래 방향 중 penalty 점수 에 맞는 방향 선택, 갭 집어넣기
    while (i > 0) or (j > 0):
        current_score = score_matrix[i][j]
        if (i > 0) and (j > 0) and (current_score == score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)):
            align1.append(seq1_ori[i-1])
            align2.append(seq2_ori[j-1])
            i -= 1
            j -= 1

        elif (i > 0) and (current_score == score_matrix[i-1][j] + gap_penalty):
            align1.append(seq1_ori[i-1])
            align2.append(['-' for k in range(len(seq1_ori[i-1]))]) 
            i -= 1
        else:
            align1.append(['-' for k in range(len(seq2_ori[j-1]))]) 
            align2.append(seq2_ori[j-1])
            j -= 1

    # 최종 서열 반환 (뒤집어야됨)
    return align1[::-1], align2[::-1], score_matrix[n][m]



def clustering(text):
    listedtext = []
    recursions  = sf.findRepeatedStrings(text)
    gone = 0
    for string in recursions:
        for position in string[1]:
            leng = len(string[0])
            listedtext = list(text[:position]) + [text[position:(position+ leng)]] + list(text[(position + leng):])
            gone += leng -1
            
    
    return 1
    
    
def split_string_with_repeats(text, repeated_substrings):
    result = []
    last_end = 0
    
   
    repeated_substrings.sort(key=lambda x: x[1][0])  
    for substring, positions in repeated_substrings:
        start = positions[0] 

       
        if last_end < start:
            result.extend(list(text[last_end:start]))

      
        result.append(substring)


        last_end = start + len(substring)

   
    if last_end < len(text):
        result.extend(list(text[last_end:]))

    return result
    
    
def pairwise_alignment(seq1, seq2):
    # list_seq1 =  split_string_with_repeats(seq1, sf.findRepeatedStrings(seq1))
    # list_seq2 =  split_string_with_repeats(seq2, sf.findRepeatedStrings(seq2))
    # for i in range(len(list_seq1)):
    #     if (len(list_seq1[i]) >  1):
    #         list_seq1[i] = '^'
    # for i in range(len(list_seq2)):
    #     if (len(list_seq2[i]) > 1):
    #         list_seq2[i] = '^'
    # print(list_seq1)
    # print(list_seq2)
    alignment1, alignment2, score = needleman_wunsch(seq1, seq2)
    
    return alignment1, alignment2
    


if __name__ == '__main__':
    seq1 = "dkjvqunskdjfgkksjdnfekunhellothisisinversiontktktsnebsijksdjfnkwejnfnnoisrevnisisihtrhrnakakTdlTekfkawnlfkawnlTJsejEHdrnajd"
    seq2 = "dkjvqunskdjfgkksjdnfekunhellothisisinversiontktktsnebsijksdjfnkwejnfnrhrnakakTdlTekfkawnlfkawnlTJsejEHdrnajd"
    
   
    list_seq1 =  split_string_with_repeats(seq1, sf.findRepeatedStrings(seq1))
    list_seq2 =  split_string_with_repeats(seq2, sf.findRepeatedStrings(seq2))
    for i in range(len(list_seq1)):
        if (len(list_seq1[i]) >  1):
            list_seq1[i] = '^'
    for i in range(len(list_seq2)):
        if (len(list_seq2[i]) > 1):
            list_seq2[i] = '^'
             
    print(list_seq1)
    print(list_seq2)
    
    alignment1, alignment2, score = needleman_wunsch(list_seq1, list_seq2)

    print("1:", alignment1)
    print("2:", alignment2)
    print("적합 점수:", score)
    



