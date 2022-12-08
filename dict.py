def makeColumn(prc):
    tab = []
    tab2 = []
    for i in range(3):
        dict1 = {"a" : int((prc[i]/100)*300)}
        if i > 0:
            dict1["a"] += tab[i-1]["a"]
        tab.append(dict1)
    for i in range(len(tab)): 
        if i > 0:
            x1 = tab[i-1]["a"]
        elif i == 0:
            x1 = 0 
        x2 = tab[i]["a"]
        dict2 = {
            0 : x1,
            1 : x2
        }
        tab2.append(dict2)
    return tab2
for i in range(3):
    print(makeColumn([33,33,33])[i][0], makeColumn([33,33,33])[i][1])
