#!/usr/bin/env python3

def size():
    n = 128
    while True:
        yield n
        n = 2*n + 2

gen = size()
sizes = [133118, 266238, 532478, 1064958, 2129918, 4259838, 8519678, 17039358, 34078718, 68157438, 136314878, 272629758, 545259518, 1090519038]

def update(*args):
    dstart, dsize, pstart, psize = tuple(args)
    print(args)
    if dstart < pstart:
        dsize *= 2
        if dstart >= dsize:
            return dstart, dsize, pstart, psize
        else:
            dstart = dsize + pstart
            return dstart, dsize, pstart, psize
    else:
        psize = pstart
        pstart = dstart + psize
        return dstart, dsize, pstart, psize

def check_res(*args):
    dstart, dsize, pstart, psize = tuple(args)
    if dsize >= 8192 and dstart > pstart and dstart < 16384:
        return 1 # win
    if dsize >= 8192:
        return -1 # loss
    return 0

def pprint(*args):
    if not PRINT:
        return
    dstart, dsize, pstart, psize = tuple(args)
    top = 'P' if pstart > dstart else 'D'
    topsize = psize if pstart > dstart else dsize
    bot = 'D' if pstart > dstart else 'P'
    botsize = dsize if pstart > dstart else psize
    print(" ============ ")
    print(" | {:}: {:5d} | ".format(top, topsize))
    print(" ============ ")
    print(" ============ ")
    print(" | {:}: {:5d} | ".format(bot, botsize))
    print(" ============ ")
    gapsize = dstart - dsize if pstart > dstart else pstart - psize
    if gapsize:
        print("   G: {:5d}   ".format(gapsize))
    print("--------------")
    print()

def test_init_conds(*args):
    dstart, dsize, pstart, psize = tuple(args)
    pprint(dstart, dsize, pstart, psize)
    while True:
        dstart, dsize, pstart, psize = update(dstart, dsize, pstart, psize)
        pprint(dstart, dsize, pstart, psize)
        res = check_res(dstart, dsize, pstart, psize)
        if res:
            print(res)
            print(dstart)
            return res

if __name__ == '__main__':
    PRINT = 1
    init_patt = 6
    test_init_conds(1+init_patt, 1, init_patt, init_patt)

    # good = []
    # for init_patt in [i*.1 for i in range(1, 1000)]:
    #     x = test_init_conds(1+init_patt, 1, init_patt, init_patt)
    #     if x == 1:
    #         good.append(init_patt)
    # print(good)


    # found valid: [2, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]
