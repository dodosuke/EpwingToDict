# EpwingToDict
「研究社 新編 英和活用大辞典（EPWING形式）」を Mac に標準搭載されている辞書アプリで使えるように変換するための python スクリプトです。
This is a tool to make a dictionary for Mac from Kenkyusha Eiwa-Katsuyo-Daijiten.

## Description
英辞郎 や Coubuild 用の Ruby スクリプトは配布されていますが、上記の辞書には対応していなかったため、自作しました。
EBDump + ebd2html で出力した HTML をスクレイピングし、データベースを作成し、XML を出力するまどろっこしい仕組みです。

## Demo
![Demo](https://github.com/dodosuke/EpwingToDict/demo.png)

## VS.
EPWING版 英和活用大辞典 専用のスクリプトです。
英辞郎 や Coubuild 用の Ruby スクリプトは配布されていますが、当

## Requirement
* 辞書データ：LogoVista 社「徹底英語活用セット」（2002年発売版、EPWING形式）
* HTML変換：Windows + EBDump + ebd2html
* 辞書作成：Mac + Python 3.6.0

## Usage
1. まずは、下記サイトを参考に HTML ファイルを作成します。作成したファイルの名前を "KENCOLLO.html" にします。
http://hp.vector.co.jp/authors/VA000022/ebd2html/ebd2html.html

2. preTreatment.py で 1. で作成したHTMLの前処理をします。"KENCOLLO.out" というファイルが出力されます。

3.



## Licence
[MIT Licence](https://github.com/dodosuke/EpwingToDict/LICENCE)

## Author
[dodosuke @ Github](https://github.com/dodosuke)  
[dodosuke0920 @ Twitter](https://twitter.com/dodosuke0920)
