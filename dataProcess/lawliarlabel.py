
for i in range(1,4):
    finpath = 'C:\\Users\\28999\\Desktop\\' + str(i) + '-0.txt'
    print(finpath)

    with open(finpath, "r", encoding="utf-8") as f:
        text = f.readlines()

    outext = ''
    for s in text:
        outext = outext + '否 ' + s

    fopath = 'C:\\Users\\28999\\Desktop\\' + str(i) + 'new-0.txt'
    with open(fopath, "w+", encoding="utf-8") as of:
        of.write(outext)