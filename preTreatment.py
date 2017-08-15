import codecs
import re

f = codecs.open('KENCOLLO.html', 'r', 'utf-8')
f_out = codecs.open('KENCOLLO.out', 'w', 'utf-8')

for line in f:
    # <nobr>, <sub>, <sup> タグを全削除する
    line = line.replace("<nobr>", "").replace("</nobr>", "")
    line = line.replace("<sub>", "").replace("</sub>", "")
    line = re.sub('<sup>(.+?)</sup>', '', line)

    # 半角文字前の全角数字を削除する
    line = re.sub('[０-９]([a-xA-Z0-9_])', '\\1', line)

    # 全角スペースを半角スペースに変換する
    line = line.replace("　", " ")

    # 不要な改行を削除する
    line = line.replace("\n", "")
    if line.find(" ") == 0 :
        f_out.write(line)
    else:
        f_out.write("\n" + line)

f.close()
f_out.close()
