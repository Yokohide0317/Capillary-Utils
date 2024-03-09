import argparse
from pathlib import Path
import os
from Bio import SeqIO

from typing import Union, List, Optional

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src import tools, make_html

class Ab1ToFast:
    def __init__(self, file: Union[str, None]):

        self.file: str = file

        # check if the file is ab1
        if Path(self.file).suffix != ".ab1":
            raise ValueError(f"Invalid file type: {file}")

    def run(self, output_dir: str, to: str) -> str:
        if to != "fastq" and to != "fasta":
            raise ValueError(f"Invalid file type: {to}. Choose fastq or fasta")

        # そんざいしない場合は作成
        if not Path(output_dir).exists():
            Path(output_dir).mkdir()

        output_path = str(Path(output_dir) / f"{Path(self.file).stem}.{to}")
        self.to_fast(self.file, output_path, to=to)

        return output_path

    def to_fast(self, ab1_file: str, save_file: str, to: str):

        seqHandle = SeqIO.parse(ab1_file, "abi")

        for seq in seqHandle:
            break

        SeqIO.write(seq, Path(save_file), to)

        return True

def parse_dir(file_dir: str, output_root_dir: str) -> dict:
    res = {}
    file_list = [str(x) for x in Path(file_dir).glob("*.ab1")]
    for file in file_list:
        res[file] = Path(file).stem

    if not Path(output_root_dir).exists():
        Path(output_root_dir).mkdir()
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utils for capillary sequencing")
    subparsers = parser.add_subparsers(dest="subcommand")

    # convert
    parser_convert = subparsers.add_parser("convert")
    parser_convert.add_argument("-f", "--file", type=str, help="ab1 file path")
    parser_convert.add_argument("-d", "--dir", type=str, help="directory path")
    parser_convert.add_argument("-o", "--output_dir", type=str, help="output dir path")
    parser_convert.add_argument("-t", "--to", type=str, help="output file type. fasta or fastq")

    # all
    parser_convert = subparsers.add_parser("all")
    parser_convert.add_argument("-f", "--file", type=str, help="ab1 file path")
    parser_convert.add_argument("-d", "--dir", type=str, help="directory path")
    parser_convert.add_argument("-o", "--output_dir", type=str, help="output dir path")

    args = parser.parse_args()
    match args.subcommand:
        case "convert":
            if args.file is None and args.dir is None:
                parser.print_help()
                exit(1)

            # 単体入力
            elif args.file is not None:
                output_root_dir = args.output_dir

                if not Path(output_root_dir).exists():
                    Path(output_root_dir).mkdir()
                files = {args.file: Path(args.file).stem}

            # まとめ入力
            elif args.dir is not None:
                output_root_dir = args.output_dir
                files = parse_dir(args.dir, output_root_dir)

            for file, sample_name in files.items():
                output_dir = str(Path(output_root_dir) / sample_name)
                ab1ToFast = Ab1ToFast(file=file)
                ab1ToFast.run(output_dir=output_dir, to=args.to)

        case "all":
            if args.file is None and args.dir is None:
                parser.print_help()
                exit(1)

            # 単体入力
            elif args.file is not None:
                output_root_dir = args.output_dir
                if not Path(output_root_dir).exists():
                    Path(output_root_dir).mkdir()
                files = {args.file: Path(args.file).stem}

            # まとめ入力
            elif args.dir is not None:
                output_root_dir = args.output_dir
                files = parse_dir(args.dir, output_root_dir)

            for file, sample_name in files.items():
                output_dir = str(Path(output_root_dir) / sample_name)
                ab1ToFast = Ab1ToFast(file=file)
                ab1ToFast.run(output_dir=output_dir, to="fastq")
                ab1ToFast.run(output_dir=output_dir, to="fasta")

                # reportの作成
                to_html = make_html.MakeHtml(file)
                html = str(to_html.pipe())
                html_path = str(Path(output_dir) / f"{sample_name}.html")
                with open(html_path, "w") as f:
                    f.write(html)
        case _:
            parser.print_help()
