#%%
import streamlit as st
import os
from pathlib import Path
from Bio import SeqIO

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.tools import ab1_to_seq

###############################
st.markdown("# 1. Import")

uploaded_file = st.file_uploader("Choose a abi file", accept_multiple_files=False)


if uploaded_file is not None:

    filename = uploaded_file.name
    seq = ab1_to_seq(uploaded_file)

    fileSaveName = f"{Path(filename).stem}.fastq"
    SeqIO.write(seq, 'sequence.fastq', "fastq")
    with open('sequence.fastq', mode = 'rb') as f:
        st.download_button(label='Download' , data=f, file_name=fileSaveName, mime= 'application/octet-stream')
