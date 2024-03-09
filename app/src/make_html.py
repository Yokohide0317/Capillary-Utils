#%%
from Bio import SeqIO
import pandas as pd
from bs4 import BeautifulSoup

import plotly.graph_objects as go

"""
"PBAS2",  # base-called sequence
"PCON2",  # quality values of base-called sequence
"SMPL1",  # sample id inputted before sequencing run
"RUND1",  # run start date
"RUND2",  # run finish date
"RUNT1",  # run start time
"RUNT2",  # run finish time
# NOTE: The following are used for trace data
"PLOC2",  # position of peaks
"DATA1",  # channel1 raw data
"DATA2",  # channel2 raw data
"DATA3",  # channel3 raw data
"DATA4",  # channel4 raw data
"DATA9",  # channel1 analyzed data
"DATA10",  # channel2 analyzed data
"DATA11",  # channel3 analyzed data
"DATA12",  # channel4 analyzed data
"FWO_1",  # base order for channels
"""

# %%

class MakeHtml:
    def __init__(self, ab1_path: str) -> None:
        ab1 = SeqIO.read(ab1_path, "abi")

        self.ab1_path = ab1_path
        self.fastq = ab1.format("fastq")
        self.fasta = ab1.format("fasta")
        self.ab1 = ab1
        self.sample_name = ab1.annotations["abif_raw"]["SMPL1"].decode()

        self.peaks = self.make_df()
        return

    def make_df(self):
        pos_list = list(self.ab1.annotations["abif_raw"]["PLOC2"])
        peaks = pd.DataFrame({
            "DATA9": list(self.ab1.annotations["abif_raw"]["DATA9"]),
            "DATA10": list(self.ab1.annotations["abif_raw"]["DATA10"]),
            "DATA11": list(self.ab1.annotations["abif_raw"]["DATA11"]),
            "DATA12": list(self.ab1.annotations["abif_raw"]["DATA12"]),
        }).reset_index(names=["position"])

        peaks = peaks[peaks["position"].isin(pos_list)]
        ## {G: DATA9, A: DATA10, T:DATA11, C: DATA12}
        annotate_bases = dict(zip([f"DATA{i}" for i in range(9, 13)], list(self.ab1.annotations["abif_raw"]["FWO_1"].decode())))
        peaks = peaks.rename(columns=annotate_bases)
        peaks["annotate"] = list(self.ab1.annotations["abif_raw"]["PBAS2"].decode())
        peaks = peaks.reset_index(drop=True).reset_index(names=["index"])

        return peaks

    def make_ab1_fig(self):
        # Ab1用のグラフ
        fig = go.Figure()
        fig.update_layout(
            width=1500,
            height=500,
        )

        fig.add_trace(go.Scatter(y=self.peaks["A"], mode="lines", name="A"))
        fig.add_trace(go.Scatter(y=self.peaks["T"], mode="lines", name="T"))
        fig.add_trace(go.Scatter(y=self.peaks["G"], mode="lines", name="G"))
        fig.add_trace(go.Scatter(y=self.peaks["C"], mode="lines", name="C"))

        return fig.to_html(full_html=True, include_plotlyjs='cdn')

    def make_fastq_fig(self):
        # FASTQ用のグラフ
        df = pd.DataFrame({
            "score": self.ab1.letter_annotations["phred_quality"],
            "index": range(1, len(self.ab1.letter_annotations["phred_quality"])+1),
        })

        fig = go.Figure()
        fig.update_layout(
            width=1500,
            height=500,
        )
        fig.add_bar(y=df["score"], x=df["index"], name="score")
        fig.add_hrect(y0=0, y1=20, line_width=0, fillcolor="red", opacity=0.2)
        fig.add_hrect(y0=20, y1=28, line_width=0, fillcolor="yellow", opacity=0.2)
        fig.add_hrect(y0=28, y1=50, line_width=0, fillcolor="green", opacity=0.2)
        qc_html_str = fig.to_html(full_html=True, include_plotlyjs='cdn')
        return BeautifulSoup(qc_html_str, "html.parser").find("div")

    def pipe(self):
        ab1_graph_str = self.make_ab1_fig()
        qc_graph_str = self.make_fastq_fig()

        html = BeautifulSoup(ab1_graph_str, "html.parser")

        # Graph前にタイトルを追加
        html.body.insert(0, BeautifulSoup(
            f"""
            <h1>AB1 to FASTA Result</h1>
            <h2>Description</h2>
            <p>Sample Name: {self.sample_name}<br>
            Run Start: {self.ab1.annotations["abif_raw"]["RUND1"]} {self.ab1.annotations["abif_raw"]["RUNT1"]}<br>
            Run Finish: {self.ab1.annotations["abif_raw"]["RUND2"]} {self.ab1.annotations["abif_raw"]["RUNT2"]}<br>
            Convert Date: {pd.to_datetime("today")}<br>
            Convert Input: {self.ab1_path}</p>
            <h2>AB1 Quality</h2>
            """,
            "html.parser")
        )

        html.body.append(BeautifulSoup("<h2>FASTQ Quality</h2>", "html.parser"))
        html.body.append(qc_graph_str)

        fasta_text = self.fasta.replace("\n", "<br>")

        html.body.append(BeautifulSoup(
            f"""
            <h2>FASTA</h2><p>{fasta_text}</p>
            """,
            "html.parser")
        )

        return html

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ab1_path", type=str)
    parser.add_argument("-o", "--output", type=str, default="output.html")
    args = parser.parse_args()

    make_html = MakeHtml(args.ab1_path)
    html = make_html.pipe()
    with open(args.output, "w") as f:
        f.write(str(html))
# %%
