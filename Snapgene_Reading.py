import SnapgeneProcessing
import xlwt
import os
import re
def main():
    Primer_name = []
    Primer_sequence = []
    for root, dirs, files in os.walk('D:/PycharmProjects/SnapgeneProcessing'):
        print(files)
    file_number = []
    for file in files:
        file =  re.findall("D-Pbs(.*?).dna",file)
        if file != []:
            file_number.append(file[0])
    file_names = []
    for file_No in file_number:
        Primer_name.append('D-Pbs'+file_No + '_Forward')
        Primer_name.append('D-Pbs'+file_No + '_Reverse')
        file_names.append('D-Pbs' + file_No + '.dna')
    #print(file_names)
    for file_name in file_names:
        print(file_name)
        file_docname = open(file_name,'r',encoding='ISO-8859-1')
        #print(file_docname)
        file_data = file_docname.read()
        # print(file_data)
        file_features = file_Segment(file_data)
        #print(file_features)
        sequences = Sequence_Get(file_data)
        #print(sequences)
        Primer_Site = Primer_point(file_features)
        Forward_Primer, Reverse_Primer = Primer_Sequence(Primer_Site, sequences)
        Reverse_Primer = DNA_complement2(DNA_reverse(Reverse_Primer))
        print(Forward_Primer,Reverse_Primer)
        Primer_sequence.append(Forward_Primer)
        Primer_sequence.append(Reverse_Primer)
    #print(Primer_name)
    #print(Primer_sequence)
    list0 = []
    list0.append(Primer_name)
    list0.append(Primer_sequence)
    Save_Path(list0)
'''
This part is to use reg to find the primer site and the whole sequence information
'''
def file_Segment(file_data):

    standard_name = 'XRH-Pbs.*?Segment range="(.*?)"' # The reg calculation to get the starting and ending site of primers
    file_features = re.findall(standard_name,file_data)[-2:]
    return file_features
#print(file_features)
#print(type(file_features))
#print(file_data)
def Sequence_Get(file_data):
    sequence_get = 'SnapGene\W{10}[a-zA-Z]?.(.*)' #The reg calculation to get the sequence
    sequeces = re.findall(sequence_get,file_data)
    #print(sequeces)
    return sequeces
'''
    This part is to get the starting and ending point of Forward and Reverse primer
    '''
def Primer_point(file_features):
    Forward_Primer_Starting = ""
    Forward_Primer_Ending = ""
    Reverse_Primer_Starting = ""
    Reverse_Primer_Ending = ""
    Primer_Starting = []
    Primer_Ending = []
    Primer_Site = []
    for file_feature in file_features:
        Primer_Starting.append(re.findall('(.*)-',file_feature))
        Primer_Ending.append(re.findall('.*-(.*)',file_feature))
        #print(Primer_Starting)
        #print(Primer_Ending)

    if int(Primer_Starting[0][0]) > int(Primer_Starting[1][0]):
        Forward_Primer_Starting = Primer_Starting[1][0]
        Reverse_Primer_Starting = Primer_Starting[0][0]
    else:
        Forward_Primer_Starting = Primer_Starting[0][0]
        Reverse_Primer_Starting = Primer_Starting[1][0]

    if int(Primer_Ending[0][0]) > int(Primer_Ending[1][0]):
        Forward_Primer_Ending = Primer_Ending[1][0]
        Reverse_Primer_Ending = Primer_Ending[0][0]
    else:
        Forward_Primer_Ending = Primer_Ending[0][0]
        Reverse_Primer_Ending = Primer_Ending[1][0]
        #print(Forward_Primer_Starting)
        #print(Forward_Primer_Ending)
        #print(Reverse_Primer_Starting)
        #print(Reverse_Primer_Ending)

    Primer_Site.append(Forward_Primer_Starting)
    Primer_Site.append(Forward_Primer_Ending)
    Primer_Site.append(Reverse_Primer_Starting)
    Primer_Site.append(Reverse_Primer_Ending)
    return Primer_Site
'''
This part is to get the Forward and Reverse primer sequence
'''
def Primer_Sequence(Primer_Site,sequences):
    Forward_Primer = ""
    Reverse_Primer = ""
    for sequence in sequences:
        Forward_Primer = sequence[int(Primer_Site[0])-1:int(Primer_Site[1])]
        Reverse_Primer = sequence[int(Primer_Site[2])-1:int(Primer_Site[3])]
    #print(Forward_Primer)
    #print(Reverse_Primer) #Caution: We need to design the reverse primer according to the bottom strand
    return Forward_Primer, Reverse_Primer
def DNA_reverse(sequence):
    return sequence[::-1]  # 求反向序列
	# 互补序列方法2：python3 translate()方法
def DNA_complement2(sequence):
    trantab = str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh')     # trantab = str.maketrans(intab, outtab)   # 制作翻译表
    string = sequence.translate(trantab)     # str.translate(trantab)  # 转换字符
    return string
def Save_Path(list0):
    book = xlwt.Workbook()
    savepath = 'Primer.xls'
    sheet = book.add_sheet('Primer')
    col = ("Name","Sequence")
    for i in range(0, 2):
        sheet.write(0, i, col[i])
    for i in range(0, 2):
        # print("The %d line" %(i+1))
        list_i = list0[i]  # Save each list information
        for j in range(len(list_i)):
            sheet.write(j + 1, i, list_i[j])
        book.save(savepath)  # Save

if __name__ == "__main__":
    main()
    print("Finish!")

