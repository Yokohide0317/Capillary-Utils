#!/bin/bash

pip3 install -r Capillary-Utils/requirements.txt -q

INPUT="/content/input"
if [ ! -d $INPUT ]; then
    mkdir $INPUT
fi

echo "左のファイルタブを開き、「input」の中に.ab1ファイルを入れてください。"
echo "※複数ファイルもOKです。"
echo "入れたら、次のセルを実行します。"
