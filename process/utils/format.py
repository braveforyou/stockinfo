#补齐0
def getstname(st):
    st = int(st)
    st = str(st)
    name = st
    for i in range(len(st)):
        name = '0' + st
    return name


