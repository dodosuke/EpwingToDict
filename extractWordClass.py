import codecs

# Extract wordclass type from HTML file
f = codecs.open('KENCOLLO2', 'r', 'utf-8')
categories = []
for line in f:
    start = line.find("【")
    if start > 0:
        end = line.rfind("】")
        category = line[start:end+1]
        if category not in categories:
            print(category)
            categories.append(category)
f.close()

print(categories)
