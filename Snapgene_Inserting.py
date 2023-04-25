import Bio
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from snapgene_reader import snapgene_file_to_dict, snapgene_file_to_seqrecord
import os
filepath = "D:/PycharmProjects/SnapgeneProcessing/"
for root, dirs, files in os.walk(filepath+'Pre-editing/'):
    print(files)
for file in files:
    seqrecord = snapgene_file_to_seqrecord(filepath+'Pre-editing/'+file)
    #print(seqrecord.annotations)
    print(seqrecord)
# 已编辑好的序列
    seq = "GCTTGCTATGTCGTCGGAGGAGATATTTATTACTTTTATTATTCTAGTTTTTTACAGTTATTTATTAATTAATTATTTTTATATGCATGCGAATAAAAAGTCTATATTTAAGTTCTTTTATTTATTAATACATTTTCCTCTACGAGCTGTCACCGGATGTGCTTTCCGGTCTGATGAGTCCGTGAGGACGAAACAGCCTCTACAAATAATTTTGTTTAAGAGCAGGTTGTTCATGGCCGTGCGTATGATGTGGGGGGCTCGGGCGTTGAAACCGGGGTTCGGAGCGCCAGGGGGTTTTcaacggcCTAGCATGTGATTAATTAATTATTTTGTTTTTTTTTTGCAGTATAAAAAGTTAGTTTGTTTAAACAACAAACTTTTTTCATTTCTTTTGTTTCCCCTTCTCTTCTTTTAGTTAGTTTGTTTAAACAACAAACTAGAATATCAAGCTACAAAAATAAATAAAAaatg"


# 在 backbone 质粒的某个特定位置插入编辑好的序列
    insertion_site = 527
    new_sequence = seqrecord.seq[:insertion_site] + Seq(seq) + seqrecord.seq[insertion_site+415:]
    print(new_sequence)
    new_record = SeqRecord(new_sequence, id=f"plasmid_{file}", description=f"Plasmid with inserted sequence {'Pxyl-UAS'}")
    # 将新质粒序列写入文件
    file_0 = file[0:12]+"-UASpxyl-"+file[18:31]+".gbk"
    file_new = open(filepath+'Already-Editing/'+file_0, "w")
    SeqIO.write(new_record, file_new, "fasta")
