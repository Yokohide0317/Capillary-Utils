import argparse
from pathlib import Path
import os
import sys
from Bio import SeqIO

from typing import Union, List, Optional


class Ab1ToFast:
    def __init__(self, file_dir: Union[str, None]=None, file: Union[str, None]=None):

        if (file_dir is None) and (file is None):
            raise ValueError("file_dir and file cannot be None at the same time")
        elif (file_dir is not None) and (file is not None):
            raise ValueError("file_dir and file cannot select at the same time")

        if file_dir is not None:
            files = [str(file) for file in Path(file_dir).glob("*.ab1")]
            if len(files) == 0:
                raise ValueError(f"No file in the directory: {file_dir}")
        else:
            files: List[str] = [file]

        self.files: List[str] = files

        # check if the file is ab1
        for file in files:
            if Path(file).suffix != ".ab1":
                raise ValueError(f"Invalid file type: {file}")

    def run(self, output_dir: str, to: str) -> List[str]:
        if to != "fastq" and to != "fasta":
            raise ValueError(f"Invalid file type: {to}. Choose fastq or fasta")

        # そんざいしない場合は作成
        if not Path(output_dir).exists():
            Path(output_dir).mkdir()

        output_files = []
        for file in self.files:
            output_path = str(Path(output_dir) / f"{Path(file).stem}.{to}")
            self.to_fast(file, output_path, to=to)
            output_files.append(output_path)

        return output_files

    def to_fast(self, ab1_file: str, save_file: str, to: str):

        seqHandle = SeqIO.parse(ab1_file, "abi")

        for seq in seqHandle:
            break

        SeqIO.write(seq, Path(save_file), to)

        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utils for capillary sequencing")
    subparsers = parser.add_subparsers(dest="subcommand")

    # to_fastq
    parser_convert = subparsers.add_parser("convert")
    parser_convert.add_argument("-f", "--file", type=str, help="ab1 file path")
    parser_convert.add_argument("-d", "--dir", type=str, help="directory path")
    parser_convert.add_argument("-o", "--output_dir", type=str, help="output dir path")
    parser_convert.add_argument("-t", "--to", type=str, help="output file type. fasta or fastq")

    args = parser.parse_args()
    match args.subcommand:
        case "convert":
            ab1ToFast = Ab1ToFast(file=args.file, file_dir=args.dir)
            ab1ToFast.run(output_dir=args.output_dir, to=args.to)
        case "bar":
            pass