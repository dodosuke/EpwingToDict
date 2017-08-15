import codecs
import re

f = codecs.open('test', 'r', 'utf-8')
f_out = codecs.open('test_out', 'a', 'utf-8')

for line in f:
    # remove all <nobr></nobr> and replace <>
    line = line.replace("<nobr>", "").replace("</nobr>", "")
    line = line.replace("&lt;", "<").replace("&gt;", ">")

    # remove link to the parent words
    line = re.sub('<a href="#[0-9A-Fa-f]{12}">&#xE00C;</a>', '', line)
    f_out.write(line)
f.close()
f_out.close()
