import math
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix
from Bio import SeqIO
import pairwiseAlignment as pa
import suffixtree as sf
from Bio import Phylo
def jukes_cantor_distance(seq1, seq2):
    differences = sum(1 for a, b in zip(seq1, seq2) if a != b)
    p = differences / len(seq1)
    if p < 0.75:
        return -3/4 * math.log(1 - 4/3 * p)
    else:
        return float('inf')

def alignGt(guide_tree, sequences):
    """
    가이드 트리의 병합 순서대로 시퀀스들을 페어와이즈 정렬
    일단 말단에서는 그대로 
    그리고 중간에서는 프로필을 만들고 그걸로 모티프를 만들어서 모티프끼리 정렬
    이후 모티프에 맞춰서 나머지도 페어와이즈 정렬합니다.     
    
    반환하는 건? 프로필(서열의 모음)
    거기서 모티프 추출하고 이러쿵저러쿵
    """

   
    # 재귀적으로 병합 순서 따라가기
    def alignClades(clade):
        profile = []
        
        if clade.is_terminal():
            # 말단 노드는 해당 시퀀스 리스트 형식으로 반환
            for char in sequences[int(clade.name)]:
                profile.append([char])
            
            return profile



        left = alignClades(clade.clades[0])
        right = alignClades(clade.clades[1])
       
        
        aligned_left, aligned_right = pa.pairwise_alignment(left, right)
        
        #align 하고 profile에 넣기 
        for i in range(len(aligned_left)):
            profile.append(aligned_left[i] + aligned_right[i])
        #그대로 profile 반환
        

        return profile

    # 루트에서부터 정렬 시작
    msa_result = alignClades(guide_tree.root)
    return msa_result


def profilize(seq):
    profile = []
    for char in seq:
        profile.append([char])
           
    return profile

    
def print_profile(profile):
    result = ''
    
    parsed = str(profile)
    for i in range(len(parsed)):
        if (parsed[i] != '[' and parsed[i] != ']' and parsed[i] != "'" and parsed[i] != ',' and parsed[i] != ' '):
            result += parsed[i]
    return result

if __name__ == '__main__':
    sequence_file = "assets/sequences.fasta"
    sequencesIO = SeqIO.parse(sequence_file , "fasta")
    sequences = []

    for s in sequencesIO:
        sequences.append(str(s.seq))

  
    distance_matrix = []

    n = len(sequences)
    
    
    

    for i in range(n):
        row = []
        for j in range(i+1):
            print(profilize(sequences[i]))
            alignment1, alignment2 = pa.pairwise_alignment(profilize(sequences[i]), profilize(sequences[j]))
            distance = jukes_cantor_distance(alignment1, alignment2)
            row.append(distance)
        
        distance_matrix.append(row)



    names = [f'{i}' for i in range(len(sequences))]
    dm = DistanceMatrix(names, distance_matrix)

   

    constructor = DistanceTreeConstructor()
    guide_tree = constructor.upgma(dm)

    print(guide_tree)

    Phylo.draw(guide_tree, branch_labels=lambda c: f"{c.branch_length:.2f}" if c.branch_length else "")

    derepeated_sequences = []
    
    for seq in sequences:
        #derepeated_sequences.append(seq)
        l_seq = pa.split_string_with_repeats(seq, sf.findRepeatedStrings(seq))
    
        for i in range(len(l_seq)):
            if (len(l_seq[i]) >  1):
                l_seq[i] = '^'
        derepeated_sequences.append(l_seq)

        
    msa_result = alignGt(guide_tree, derepeated_sequences)
    
    print("Final MSA result:")
    
    
    result = ["" for i in range(n)]
    #~~profile 형태의 MSa결과를 재귀적으로 출력함
    p = print_profile(msa_result)
    for i in range(len(p)):
        result[i%n] += p[i]

    for k in result:
        print(k)
    print("적합 점수 :" )
        
            
        
    
    
    
#     >Sequence1
# dkjvqunskdjfgkksjdnfekunhellothisisinversiontktktsnebsijksdjfnkwejnfnnoisrevnisisihtrhrnakakTdlTekfkawnlfkawnlTJsejEHdrnajd

# >Sequence2
# dkjvqunskdjfgkksjdnfekunheversiontktktsnebsijksdjfnkwejnfnnoisrevnisisihtrhrnakakTdlTekfkawnlfkawnlTJsejEHdrnajd

# >Sequence3
# dkjvqunskdjfgkksjdnfekunhellothisisinversiontktktsnebnoisrevnisisihtrhrnakakTdlTekfkalTJsejEHdrnajd
