import math
import numpy
class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.indexes = []

class SuffixTree:
    def __init__(self, text):
        self.root = SuffixTreeNode()
        self.text = text
        self.build_suffix_tree()

    def build_suffix_tree(self):
        for i in range(len(self.text)):
            current_node = self.root
            suffix = self.text[i:]
            
            for char in suffix:
                if char not in current_node.children:
                    current_node.children[char] = SuffixTreeNode()
                current_node = current_node.children[char]
                current_node.indexes.append(i)

    def search_all_repeated_substrings(self, min_length=2):
        #스택으로 일정 길이 이상의 중복되는 문자열 탐색
        stack = [(self.root, "")]
        repeated_substrings = []

        while stack:
            node, prefix = stack.pop()

            if len(node.indexes) > 1 and len(prefix) >= min_length:
                repeated_substrings.append((prefix, node.indexes))

            for char, child_node in node.children.items():
                stack.append((child_node, prefix + char))

        return repeated_substrings


def findRepeatedStrings(text):
    reversed_text = text[::-1]
    text = text + reversed_text
    
    suffix_tree = SuffixTree(text)
    
    all_repeated_substrings = suffix_tree.search_all_repeated_substrings(min_length=10)
    
    all_repeated_substrings.reverse()
    
    longest_repeated_substrings = []
    
    currentPosition = 0
    for (substring, positions) in all_repeated_substrings:
      
        if (currentPosition != positions):
            longest_repeated_substrings.append((substring, positions))
            currentPosition = positions
           # print(substring, positions, "\n\n")
    
    
        
    end_poses = {}
    
    
    for (substring, positions) in longest_repeated_substrings:
        end = positions[0] + len(substring)
        if (end not in end_poses):
            end_poses[end] = [(substring, positions) ]
        else:
            end_poses[end].append((substring, positions))
    
  #  print("~~~~~~", end_poses)
            
    prior_repeated_substrings = []
            
    for end in end_poses:
        longest = end_poses[end][0]
        min = math.inf
        for sub in end_poses[end]:
            if ((sub[1][0]) < min):
                longest = sub
                min = sub[1][0]
        
        prior_repeated_substrings.append(longest)


    
    #print(prior_repeated_substrings)
        
    postInversed_repeated_strings = []
        
    for sub1, pos1 in prior_repeated_substrings:
        newposes = []
        for (sub2, pos2) in prior_repeated_substrings:
            if sub1 == sub2: continue;
            if (sub1 == sub2[::-1]):
                
                poses  = pos1 + pos2
                print(")))))))))" , poses);
                for pos in poses:
                   
                    if (pos < len(text) / 2):
                        newposes.append(pos)
                
        if (newposes):
            postInversed_repeated_strings.append([sub1, newposes])
        else:
            postInversed_repeated_strings.append([sub1, pos1])
    
    for l in postInversed_repeated_strings:
        m = numpy.min(l[1])
        l[1].remove(m)
        
        
    for substring, positions in postInversed_repeated_strings:
        print(f"Repeated substring: {substring}, Positions: {positions}")
        
        
        
        
    
        
    return (postInversed_repeated_strings)
    

if __name__ == "__main__":
    text = "attttactattttatttagtgtctagaaaaaaatgtgtgacccacgaccgtaggaaactctagagggtaagaaaaatcaatcgtttatagagaccatcagaaagaggtttaatatttttgtgagacctatcgaagagagaaaggataaaaactttttacgactccatcagaaagaggtttaatatttttgtgagacccatcgaagagagaaagagatggttagtcaagatatttttcttagtacaaaagtcaatgttttaaaatatatggacgagaattaatttgtctgtataaaaacttgtgtgaaattatgtactagagaaaaaacgtgagcagtgtcccctacatggattttacagatcatttatattccaaaaatattaactatatacgtttattatatgatgttaacgtgtaaattataaacattattttatgatgcaattgtctgacaacctagattggtataaggatgttgataagctctacgagaatatattgttggacgttatcgtttacgaaatagttgagacatcagaaagaggtttaatatttttgtgagaccatcgaagagagaaagagaataaaaatattttttttttttttgtaaaacttttttatgagaccaagagaatacgaatagtgatcatatcgtatcacatattgaaacagaaagaagaagtaacgagaggtaactttttgtgaatgtagttaaatatttttgttttgcaaaccggaatatagtgcccggtcttttttaattcgtggtgcggtgtctgaatcgttcgattaacccaactcatccattttcagatgaatagagttatcgattcagacacatgctttgagttttgttgaatcgatgagtgaagtatcatcggttgcaccttcagatgccgatccgtcgacatacttgaatccatccttgacttcaagttcagatgattcctcacacatgtctccgatacgtacgctaaactctaggttcttgacacattttgtatcaacgatcgttgaaccgatgatatctttgtaactcactttcttatgtgagatgttagacccaagtactggatgggtcttgatgtcactgtctttctcttcttcgctacatctgatgtcgatagacatctcacagtctttgatcatagccagagcttcttcacgcgtgatcgcgggagagtccttaccttgtcccggtgacacgctggacaatctagtattcacagtgtttccatcagaggattcggagatggataaaatctttgggcatttggtgaatccaaagttcatgttaagacccgcaccgacgatagtgtaataagtggtgggatctccttttacaacttcttcggatacctcatcatcttcggtctctgtaacttccgttacggattgacaaatcttatcattggtcggtgtttggtcttgctttgt"
    findRepeatedStrings(text)


#gtaagaaaaatcaatcgtttatagagaccatcagaaagaggtttaatatttttgtgagacccatcgaagagagaaaggataaaaactttttacgactccatcagaaagaggtttaatatttttgtgagacccatcgaagagagaaagagatggttagtcaagatatttttcttagtacaaagtcaatgttttaaaatatatggacgagaattaatttgtctgtataaaaacttgtgtgaaattatgtactagagaaaaaacgtgagcagtgtcccctacatggattttacagatcatttatattccaaaaatattaactatatacgtttattatatgatgttaacgtgtaaattataaacattattttatgatgcaattgtctgacaacctagattggtataaggatgttgataagctctacgagaatatattgttggacgttatcgtttacgaaatagttgagacatcagaaagaggtttaatatttttgtgagaccatcgaagagagaaatagaataaaaatattttttttttttttttttgtaaaacttttttatgagaccaagagaatacgaatagtgatcatatcgtatcacatattgaaacagaaagaagaagtaacgagaggtaactttttgtaaatgtagttaaatatttttgttttgcaaaccggaatatagtgcccggtcttttttaattcgtggtgcggtgtctgaatcgttcgattaacccaactcatccattttcagatgaatagagttatcgattcagacacatgctttgagttttgttgaatcgatgagtgaagtatcatcggttgcaccttcagatgccgatccgtcgacatacttgaatccatccttgacttcaagttcagatgattcctcacacatgtctccgatacgtacgctaaactctaggttcttgacacattttgtatcaacgatcgttgaaccgatgatatctttgtaactcactttcttatgtgagatgttagacccaagtactggatgggtcttgatgtcactgtctttctcttcttcgctacatctgatgtcgatagacatctcacagtctttgatcatagccagagcttcttcacgcgtgatcgcgggagagtccttaccttgtcccggtgacacgctggacaatctagtattcacagtgtttccatcagaggattcggagatggatgaaatctttgggcatttggtgaatccaaagttcatgttaagacccgcaccgacgatagtgtaataagtggtgggatctccttttacaacttcttcggatacctcatcatcttcggtctctgtaacttccgttacggattgacaaatcttatcattggtcggtgtttggtcttgctttgtgactttgataataacatcgattcccatatgatgtttgttttcttcttcagtacacgaggatgaagattgttgaagactagtaggcatagcagctgccactaggcacatgcatgccaggacaatatattgtttcatgattgctattgattgattactgttctagatgattctactttcttaccatataataaattagaatatattttctacttttacgagaaattaattattgtatttattattta
   
   
