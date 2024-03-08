from Bio import SeqIO
import pandas as pd

def seq_to_df(seq):
    seqStr = [s for s in str(seq.seq)]
    score = seq.letter_annotations["phred_quality"]

    _df = pd.DataFrame(seqStr, columns=["seq"])
    _df["score"] = score

    _df["seq"] = _df["seq"].astype(str)
    _df["score"] = _df["score"].astype(int)
    _df["index"] = _df.index + 1

    _df = _df[["index", "seq", "score"]]
    return _df

def ab1_to_seq(ab1_file):
    seqHandle = SeqIO.parse(ab1_file, "abi")

    for seq in seqHandle:
        break

    return seq