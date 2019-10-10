#补齐0
def getstname(st):
    st = int(st)
    st = str(st)
    name = st
    for i in range(len(st)):
        name = '0' + st
    return name


def getStnameSH(stnamex):
    if (len(stnamex) != 6):
        for i in range(6 - len(stnamex)):
            stnamex = '0' + stnamex
        stnamex = 'sz' + stnamex
    else:
        if(str(stnamex[0])=='6'):
            stnamex = 'sh' + stnamex
        else:
            stnamex = 'sz' + stnamex
    return stnamex