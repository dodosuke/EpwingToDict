import codecs
from functions import pretreat, storeWCToDB, extractEntryAndIndex, extractMeaning

# 入力ファイルのパスを指定
f_path = 'KENCOLLO.html'

# HTML ファイルを前処理し、temp ファイルを出力する
pretreat(f_path)

# 前処理した HTML からデータを抜き出す。
# 品詞の分類を保存
storeWCToDB()

# 項目を抽出し、保存
extractEntryAndIndex()

# 説明文を抽出し、保存
extractMeaning()
