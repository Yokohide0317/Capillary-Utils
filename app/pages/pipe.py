#%%
import streamlit as st
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import pandas as pd
from Bio import SeqIO

import time

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

def plot_fastq_qualities(df, ax=None, cut_left_num=0, cut_right_num=0):
    _max = len(df["index"])
    print(_max)
    #fig = px.scatter(y=df["score"].values, x=df["index"].values)
    fig = px.bar(y=df["score"].values, x=df["index"].values)
    fig.add_hrect(y0=0, y1=20, line_width=0, fillcolor="red", opacity=0.2)
    fig.add_hrect(y0=20, y1=28, line_width=0, fillcolor="yellow", opacity=0.2)
    fig.add_hrect(y0=28, y1=50, line_width=0, fillcolor="green", opacity=0.2)

    if cut_left_num > 0:
        fig.add_vrect(x0=-0.5, x1=(cut_left_num+0.5), fillcolor="black", opacity=0.5)
    if _max-cut_right_num > 1:
        fig.add_vrect(x0=(cut_right_num-0.5), x1=(_max+0.5), fillcolor="black", opacity=0.5)

    fig.update_layout(
        xaxis_title="position(bp)",
        yaxis_title="score",
        title="per base sequence quality",
    )

    return fig


###############################
st.markdown("# 1. Import")

uploaded_file = st.file_uploader("Choose a abi or fastq file")

if uploaded_file is not None:

    filename = uploaded_file.name
    if filename.endswith(".ab1"):
        seq = ab1_to_seq(uploaded_file)
    elif filename.endswith(".fastq"):
        seq = SeqIO.read(uploaded_file, "fastq")
    else:
        st.markdown("Please upload .ab1 or .fastq file.")
        st.stop()

    st.markdown("# 2. QC")

    max_value = len(seq)
    #cut_left = st.slider("左", 0, max_value-1, 0, 1)
    #cut_right = st.slider("右", 1, max_value, max_value+1, 1)

    cut_left, cut_right = st.slider("QCの位置選択", 0, max_value-1, (0, max_value+1), 1)


    df = seq_to_df(seq)
    fig = plot_fastq_qualities(df, cut_left_num=cut_left, cut_right_num=cut_right)
    st.plotly_chart(fig)

    st.dataframe(df.set_index("index").T)

    if st.button("Start Cutting"):
        #cut_df = df.copy().set_index("index")
        cut_seq = seq

        if max_value-cut_right > 1:
            st.markdown(cut_right)
            cut_seq = cut_seq[:cut_right-1]

        if cut_left > 0:
            cut_seq = cut_seq[cut_left:]

        cut_df = seq_to_df(cut_seq)
        st.dataframe(cut_df.set_index("index").T)

        st.markdown(cut_seq.seq)
        fileSaveName = f"{Path(filename).stem}_afterqc.fasta"
        SeqIO.write(cut_seq, 'sequence.fasta', "fasta")
        with open('sequence.fasta', mode = 'rb') as f:
            #filename =
            st.download_button(label='Download' , data=f, file_name=fileSaveName, mime= 'application/octet-stream')
