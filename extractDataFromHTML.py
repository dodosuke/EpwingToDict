import codecs
from ExtractFunctions import pretreat, storeWCToDB, extractEntryAndIndex, extractMeaning

# HTML ファイルを前処理し、temp ファイルを出力する
f = codecs.open('KENCOLLO.html', 'r', 'utf-8')
f_temp = codecs.open('temp.out', 'w', 'utf-8')

pretreat(f, f_temp)

f.close()
f_temp.close()

# 前処理した HTML からデータを抜き出す。
f_temp = codecs.open('temp.out', 'r', 'utf-8')

# 品詞の分類を保存
storeWCToDB()

# 項目を抽出し、保存
print("Start extracting entries and indices.")
extractEntryAndIndex(f_temp)
print("Finished extracting."

# 説明文を抽出し、保存
print("Start extracting items.")
extractMeaning(f_temp)
print("Finished extracting.")

f_temp.close()
