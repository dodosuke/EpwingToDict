# EpwingToDict
「研究社 新編 英和活用大辞典（EPWING形式）」を Mac に標準搭載されている辞書アプリで使えるように変換するための python スクリプトです。
This is a tool to make a dictionary for Mac from Kenkyusha Eiwa-Katsuyo-Daijiten.

## Description
EBDump + ebd2html で出力した HTML をスクレイピングし、データベースを作成し、辞書用の XML ファイルを出力する Python スクリプトです。
LogoVista社の 英和活用大辞典（EPWING） 専用であり、他の辞書やバージョンには対応していません。
* preTreatment.py: 変換用に HTML を前処理するためのスクリプト
* extractDataFromHTML.py: HTML からデータを抜き出すスクリプト
* convertDBToXML.py: XML 出力するスクリプト
* database_setup.py: データベースの設定
* checkDB.py: データベースの内容確認用スクリプト（開発用）
* extractWordClass.py: 品詞の分類抜き出し用スクリプト（開発用）

## Demo
![Demo](https://github.com/dodosuke/EpwingToDict/blob/master/demo.png)

## VS.
EPWING版 英和活用大辞典 専用のスクリプトです。
英辞郎 や Coubuild 用の 変換スクリプトは配布されていますが、英和活用大辞典では使えなかったので、作りました。

## Requirement
* 辞書データ：LogoVista 社「徹底英語活用セット」（2002年発売版、EPWING形式）
* HTML変換：Windows + EBDump + ebd2html
* 辞書作成：Mac + Python 3.6.0

## Usage
1. まずは、下記サイトを参考に HTML ファイルを作成します。作成したファイルの名前を "KENCOLLO.html" にします。
http://hp.vector.co.jp/authors/VA000022/ebd2html/ebd2html.html

2. preTreatment.py で 1. で作成したHTMLの前処理をします。"KENCOLLO.out" というファイルが出力されます（所用時間：数十秒）。

3. extractDataFromHTML.py で、前処理したHTMLファイルをスクレイピングし、データをデータベースに格納します（所用時間：20分程度）。

4. convertDBToXML.py で、データベースの情報からXMLファイルを作成します（所用時間：30分程度）。

5. 作成された XML ファイルを使い、Macの辞書を作成し、インストールします（所用時間：数分）。１箇所タグ関連のエラーが出るので、XML ファイルを直接編集してください。

なお、所要時間は、MacBook Pro (2013 late）で実行時のものです。

## Memo
2017.8.16： 初版公開  
リンクが機能しない、かなで検索できない、などについては、気が向いたら対応予定。

## Licence
[MIT Licence](https://github.com/dodosuke/EpwingToDict/LICENCE)

## Author
[dodosuke @ Github](https://github.com/dodosuke)  
[dodosuke0920 @ Twitter](https://twitter.com/dodosuke0920)
