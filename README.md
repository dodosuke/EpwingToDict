# EpwingToDict
LogoVista社製「研究社 新編 英和活用大辞典（EPWING形式）」を Mac に標準搭載されている辞書アプリで使えるように変換するための python スクリプトです。  

This is a tool to make a dictionary for Mac from Kenkyusha Eiwa-Katsuyo-Daijiten.

## Description
EBDump + ebd2html で出力した HTML をスクレイピングし、データベースを作成し、辞書用の XML ファイルを出力する Python スクリプトです。
LogoVista社の 英和活用大辞典（EPWING） 専用であり、他の辞書やバージョンには対応していません。
* extractDataFromHTML.py: HTML からデータを抜き出すスクリプト
* convertDBToXML.py: XML 出力するスクリプト
* DBSetup.py: データベースの設定
* ExtractFunctions: HTML の前処理及び抽出に関するファイル
* checkDB.py: データベースの内容確認用スクリプト（開発用）
* extractWordClass.py: 品詞の分類抜き出し用スクリプト（開発用）
* KENCOLLO.lst: 外字ファイル（参考資料）

なお、今回のスクリプト作成にあたっては、下記のブログを参考にしています。英辞郎やCoubuildの変換に関しては、こちらをご参照ください。  
http://www.binword.com/blog/archives/000588.html

## Demo
![Demo](https://github.com/dodosuke/EpwingToDict/blob/master/demo.png)

## Requirement
* 辞書データ：LogoVista 社「徹底英語活用セット」（2002年発売版、EPWING形式）
* HTML変換：Windows + EBDump + ebd2html
* 辞書作成：Mac + Python 3

## Usage
1. まずは、下記サイトを参考に HTML ファイルを作成します。作成したファイルの名前を "KENCOLLO.html" にします。（外字を修正したい場合は、このタイミングで HTML ファイルを直接編集してください。）
http://hp.vector.co.jp/authors/VA000022/ebd2html/ebd2html.html

2. extractDataFromHTML.py で、HTML を前処理した後、スクレイピングし、データベース(dictionary.db)にデータを格納します（所用時間：20分程度）。

3. convertDBToXML.py で、データベースの情報からXMLファイルを作成します（所用時間：30分程度）。

4. 作成された XML ファイルを使い、Macの辞書を作成し、インストールします（所用時間：数分）。

なお、所要時間は、MacBook Pro (late 2013）で実行時した場合の実測値です。

## Version
2017.8.16 (ver. 1.0): 初版公開。
2017.8.17 (ver. 1.1): Bug Fix 及び コード修正。

外字を自動で書き換えない、リンクが機能しない、かなで検索できない、などについては、気が向いたら対応予定。

## Licence
[MIT Licence](https://github.com/dodosuke/EpwingToDict/LICENCE)

## Author
[dodosuke @ Github](https://github.com/dodosuke)  
[dodosuke0920 @ Twitter](https://twitter.com/dodosuke0920)
