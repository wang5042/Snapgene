import xlwt
import os
import re
from snapgene_reader import snapgene_file_to_seqrecord, snapgene_file_to_gbk
from Bio.SeqUtils import MeltingTemp

def main():
    filepath = "D:/PycharmProjects/SnapgeneProcessing/Primer Design/"
    primer_forward_list={}
    primer_backward_list = {}
    savepath = 'D:/PycharmProjects/SnapgeneProcessing/Primer_design.xls'
    A_1 = 'GTGC'
    A_2 = 'ATCA'
    B = 'AATG'
    C = 'TAAA'
    D = 'CCTC'
    BsaI = 'GGTCTC' + 'G'
    BpiI = 'GAAGAC' + 'CT'
    primer_forward_prefix = 'CTGCTC'+BsaI + A_1
    primer_backward_prefix = 'CTGCTC' + BsaI + DNA_complement2(DNA_reverse(A_2))
    for root, dirs, files in os.walk(filepath):
        print(files)
    for file in files:
        print(file)
        sequence = str(get_sequence(filepath+file))
    #print(sequence)
        reverse_sequence = DNA_reverse(sequence)
    #print(reverse_sequence)
        complement_sequence = DNA_complement2(reverse_sequence)
        a, b, primer_forward, primer_backward = primer_design(sequence, complement_sequence)
        i = 0
        primer_forward_list[file[:-4] + '_' + str(i)] = primer_forward_prefix + primer_forward
        primer_backward_list[file[:-4] + '_' + str(i)] = primer_backward_prefix + primer_backward
        while len(sequence)+len(primer_forward)+len(primer_backward) > a + b - 40:
                i = 1
                sequence = sequence[a - 25:len(sequence) + 25 - b]
                complement_sequence = DNA_complement2(DNA_reverse(sequence))
                a, b, primer_forward, primer_backward = primer_design(sequence, complement_sequence)
                primer_forward_list[file[:-4] + '_' + str(i)] = primer_forward
                primer_backward_list[file[:-4] + '_' + str(i)] = primer_backward
                print(len(sequence))
                print(a)
                print(b)
                i = i + 1
    #print(complement_sequence)
    #print(calculate_melting_temp(seqence[30:57]))
    #print(calculate_melting_temp(seqence[0:10]))


    print(primer_forward_list)
    print(primer_backward_list)

    excel_output(primer_forward_list,primer_backward_list,savepath)
def primer_design(sequence,complement_sequence):
    i = 20
    a = 20
    primer_forward = ''
    #print(sequence)
    #print(calculate_melting_temp(sequence[0:69]))
    while i < 69:
        if calculate_melting_temp(sequence[0:i])>75.0:
            print(calculate_melting_temp(sequence[0:i]))
            print('i = ' + str(i))
            break
        i = i + 1
        #print('i = '+ str(i))
    primer_forward= sequence[0:i]
    #print(primer_forward)
    primer_backward=''
    while a < 69:
        #print(calculate_melting_temp(complement_sequence[0:a]))
        if calculate_melting_temp(complement_sequence[0:a])>78.0:
            print(calculate_melting_temp(complement_sequence[0:a]))
            print('a = ' + str(a))
            break
        a = a + 1
        #print('a = '+ str(a))
    primer_backward=complement_sequence[0:a]
    #print(primer_backward)
    return i, a, primer_forward, primer_backward
"""
The get_sequence function is to get the sequence in the file and return its sequence character value
"""
def get_sequence(file):
    sequence = snapgene_file_to_seqrecord(file)
    seq = sequence.seq
    return seq
"""
The following two functions is to get the sequence reverse and complementary sequence
"""
def DNA_reverse(sequence):
    return sequence[::-1]  # 求反向序列
	# 互补序列方法2：python3 translate()方法
def DNA_complement2(sequence):
    trantab = str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh')     # trantab = str.maketrans(intab, outtab)   # 制作翻译表
    string = sequence.translate(trantab)     # str.translate(trantab)  # 转换字符
    return string
"""
The following function is to calculate the primer's melting temperature   
"""
def calculate_melting_temp(dna_seq):
    # calculate melting temp of a given sequence using a simple formula
    #print(dna_seq)
    #print(type(dna_seq))
    Tm = MeltingTemp.Tm_NN(seq=dna_seq, Na=50, Mg=1.5, dNTPs=0.25, dnac1=0.25, dnac2=0.25, nn_table=MeltingTemp.DNA_NN1, saltcorr=1)
    '''
    A = dna_seq.count('A')
    T = dna_seq.count('T')
    G = dna_seq.count('G')
    C = dna_seq.count('C')

    if len(dna_seq) < 14:
        Tm = (A + T) * 2 + (G + C) * 4

    else:
        Tm = 64.9 +41*(G + C - 16.4)/(A + T + G + C)
    '''
    return(round(Tm, 2))
def excel_output(dic_1,dic_2,savepath):
    book = xlwt.Workbook()
    sheet = book.add_sheet('Primer')
    col = ["Forward_Primer","Sequence","Backward_Primer","Sequence"]
    for i in range(0,4):
        sheet.write(0,i,col[i])
    i = 1
    for key in dic_1:
        sheet.write(i,0,key)
        sheet.write(i,1,dic_1[key])
        i = i +1
    i = 1
    for key in dic_2:
        sheet.write(i,2,key)
        sheet.write(i,3,dic_2[key])
        i = i +1
    book.save(savepath)

'''
def Scar_Sequence():
    A_1 = 'GTGC'
    A_2 = 'ATCA'
    B = 'AATG'
    C = 'TAAA'
    D = 'CCTC'
def Endonuclease():
    BsaI = 'GGTCTC'+'G'
    BpiI = 'GAAGAC'+'CT'
'''
if __name__ == "__main__":
    main()
    print("Finish!")