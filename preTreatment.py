import codecs
import re

f = codecs.open('KENCOLLO.txt', 'r', 'utf-8')
f_out = codecs.open('KENCOLLO.out', 'a', 'utf-8')

for line in f:
    # remove all <nobr></nobr> and redundant break
    line = line.replace("<nobr>", "").replace("</nobr>", "")
    line = line.replace("\n", "")
    if line.find(" ") == 0 :
        f_out.write(line)
    else:
        f_out.write("\n" + line)
        
f.close()
f_out.close()
