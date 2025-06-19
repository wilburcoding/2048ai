import random
import math
import sys
from gui import App
import matplotlib.pyplot as plt
from history import HistoryDialog


score = 0
board = [[0 for i in range(4)] for j in range(4)]
history = []
vals = {
    "0": 0
}  # bcs log is slow
for i in range(14):
    vals[str(2**i)] = i
colors = {
    "-1": "\033[38;2;0;0;0m",
    "0": "\033[38;2;255;255;255m",
    "2": "\033[38;2;255;239;214m",
    "4": "\033[38;2;255;209;138m",
    "8": "\033[38;2;255;165;97m",
    "16": "\033[38;2;255;131;82m",
    "32": "\033[38;2;255;99;87m",
    "64": "\033[38;2;255;84;71m",
    "128": "\033[38;2;255;251;140m",
    "256": "\033[38;2;255;250;97m",
    "512": "\033[38;2;242;236;53m",
    "1024": "\033[38;2;255;248;28m",
    "2048": "\033[38;2;255;255;0m",
    "4096": "\033[38;2;173;173;173m"
}
bgcolors = {
    "0":[255,255,255],
    "2":[255,239,214],
    "4":[255,209,138],
    "8":[255,165,97],
    "16":[255,131,82],
    "32":[255,99,87],
    "64":[255,84,71],
    "128":[255,251,140],
    "256":[255,250,97],
    "512":[242,236,53],
    "1024":[255,248,28],
    "2048":[255,255,0],
    "4096":[173,173,173]
}
print(vals)
depth = 3
data = {}
# print("2048 Game")
combod = []
scored = []
evald = []
sumsdat = []

def alg():
    global data
    global depth
    global sumsdat
    zcount = sum(cell == 0 for row in board for cell in row)
    if (zcount < 3):
        depth = 4
    elif (zcount < 6):
        depth = 3
    else:
        depth = 2
    data = {}
    combo("")
    combod.append(len(data.keys()))
    scored.append(score)
    evald.append(eval(board))

    data = dict(sorted(data.items(), key=lambda item: item[1]))
    dat = [[0] for i in range(4)]

    # smedians = []
    # for key in data.keys():
    #     dat[int(key[3])-1].append(data[key])
    # try:
    #     smedians = [sorted(x)[math.floor(len(x)-1)] for x in dat]
    # except:
    #     smedians = [sorted(x) for x in dat]
    #     print(smedians)
    #     return
    # # smedians[0]*=1.05
    # smedians[1] *= 0.7
    # # smedians[3]*=1.05

    # # forcing strategy - TESTING
    for key in data.keys():
        dat[int(key[3])-1].append(data[key])
    dat = [sorted(x) for x in dat]
    for i in range(4):
        if (len(dat[i]) > 15):
            dat[i] = dat[i][int(len(dat[i])/6):len(dat[i]) - int(len(dat[i])/8)]
    # return smedians.index(max(smedians))+1
    # return list(data.keys())[0][0]
    sums = [sum(x) for x in dat]
    sumsdat = sums

    # if (sum(sums) == sums[1]):
    #     sums[1] = 0.00001
    #     print(sums)
    # else:
    #     sums[1] = 0
    sums[1] *= 0.0001


    return sums.index(max(sums))+1


def disp(b):
    for l in b:
        print(colors["-1"] + "-------------------------\033[0m")
        nwa = "|"
        for i in range(4):
            nwa += colors[str(l[i])] + str(l[i]) + "\033[0m" + \
                (" " * (5-len(str(l[i])))) + colors["-1"] + "|\033[0m"
        print(nwa)
    print(colors["-1"] + "-------------------------\033[0m")


def shift(newb, dir, save=False):
    global score
    newb = [[y for y in x] for x in newb]
    # 1 = up, 2 = down, 3 = left, 4 = right
    for j in range(4):
        if (dir == 1):
            li = [newb[i][j] for i in range(4)]
        elif (dir == 2):
            li = [newb[3-i][j] for i in range(4)]
        elif (dir == 3):
            li = [newb[j][i] for i in range(4)]
        elif (dir == 4):
            li = [newb[j][3-i] for i in range(4)]
        li = [x for x in li if x != 0]
        while (len(li) < 4):
            li.append(0)
        for i in range(3):
            if (li[i] == li[i+1]):
                li[i] = li[i] + li[i]
                if (save is True):
                    score += li[i]
                li.pop(i+1)
                li.append(0)
        if (dir == 1):
            for i in range(4):
                newb[i][j] = li[i]
        elif (dir == 2):
            for i in range(4):
                newb[3-i][j] = li[i]
        elif (dir == 3):
            for i in range(4):
                newb[j][i] = li[i]
        elif (dir == 4):
            for i in range(4):
                newb[j][3-i] = li[i]
    return newb


def add(newb):
    coords = []
    for i in range(4):
        for j in range(4):
            if (newb[i][j] == 0):
                coords.append([i, j])
    r = (random.choice(coords))
    newb[r[0]][r[1]] = random.choices([2, 4], weights=[90, 10])[0]
    return newb


def addc(newb, coord):
    newb[coord[0]][coord[1]] = random.choices([2, 4], weights=[90, 10])[0]
    return newb

# def eval(board):
#     empty = sum(cell == 0 for row in board for cell in row)
#     max_tile = max(cell for row in board for cell in row)
#     monotonicity = 0
#     for row in board:
#         for i in range(3):
#             if row[i] >= row[i + 1]: monotonicity += 1
#     return empty * 2 + vals[str(max_tile)] * 4 + monotonicity

def hex(rgb):
    rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return "#%02x%02x%02x" % rgb
def eval(newb):
    # Testing for max values (top 3? let's play around with this), favor top right alignment
    val = 0
    boardval = {}
    for i in range(4):
        for j in range(4):
            boardval[f"{i}-{j}"] = newb[i][j]
    boardval = dict(
        sorted(boardval.items(), key=lambda item: item[1], reverse=True))
    # boardval = sorted(boardval.values(), reverse=True)
    # val+=sum(boardval[0:3])
    for key in list(boardval.keys())[0:math.floor(len(boardval.keys())/2 - 1)]:
        # if (boardval[key] == 0):
        #     val += round(10/(math.dist((4, -1),
        #                  (int(key.split("-")[0]), int(key.split("-")[0])))), 4)
        # else:
        # if (int(key.split("-")[0]) - int(key.split("-")[1]) > 0 or int(key.split("-")[0]) > 1):
        #     continue
        #
        if (boardval[key] != 0):
            # val+=(vals[str(boardval[key])] * 0.1 + 1) **3
            val += round((((vals[str(boardval[key])]*9) ** 2)) / (((int(key.split("-")[0])+1) * 11.2)
                         ** 3) / (((((3-int(key.split("-")[1]) if int(key.split("-")[0]) % 2 == 1 else int(key.split("-")[1])) * 5 )+((int(key.split("-")[0])*6)) + 1.1)*6.5) ** 3), 4)
        else:
            val += 1
    # for key in list(boardval.keys())[0:min(5, len(boardval.keys()))]:
    #     # if (boardval[key] == 0):
    #     #     val += round(10/(math.dist((4, -1)
    #     #                  (int(key.split("-")[0]), int(key.split("-")[0])))), 4)
    #     # else
    #     if (boardval[key] != 0):
    #         val += round((vals[str(boardval[key])]) / ((math.dist((-1, 4)
    #                      (int(key.split("-")[0]), int(key.split("-")[1])))+10) **2), 4)
    # print(boardval)
    # print(val)
    # e
    
    mkey = list(boardval.keys())[0]
    # for i in range(4):
    #     for j in range(3):
    #         if (newb[j+1][i] < newb[j][i]):
    #             break
    #         if (j == 3):
    #             val+=max([newb[k][i] for k in range(4)])**2
    # if (max(newb[1]) == newb[1][3] and max(newb[1]) > 8):
    #     val += (vals[str(boardval[key])] * 3 + 1) ** 2

    if (newb[0][0] == list(boardval.values())[0]):
        val+=70
    return round(val, 6)


def combo(k):
    global data
    newb = [[y for y in x] for x in board]
    for item in [k[i:i+4] for i in range(0, len(k), 4)]:
        newb[int(item[0])][int(item[1])] = int(item[2])
        newb = shift(newb, int(item[3]))
    if (len(k) == depth*4):
        data[k] = eval(newb)
        return
    found = False
    for i in range(4):
        sres = shift([[y for y in x] for x in newb], i+1)
        if (sres != newb):
            if (i != 1):
                found = True
            coords = []
            for m in range(4):
                for l in range(4):
                    if (sres[m][l] == 0):
                        coords.append([m, l])
            for coord in coords:
                newbb = [[y for y in x] for x in sres]
                newbb[coord[0]][coord[1]] = 2
                newseq = f"{k}{coord[0]}{coord[1]}{2}{i+1}"
                combo(f"{k}{coord[0]}{coord[1]}{2}{i+1}")

    return


# board[1][0] = 2
# board[2][0] = 4
# board[2][1] = 4
# board[3][0] = 4
# board[3][1] = 4
# Sample1
# board = [
#     [0,2,4,16],
#     [0,0,4,4],
#     [0,0,2,2],
#     [0,0,2,4]
# ]
# Sample2
# board = [
#     [0,2,4,2],
#     [0,0,8,2],
#     [0,0,2,2],
#     [8,0,2,4]
# ]
# print(eval(board))
# disp(board)
# AI TESTING



start = False
step = False
fin = False
board = add(add(board))
app = None
history.append(",".join([",".join([str(y) for y in x]) for x in board]))
def reset():
    global step
    global board
    global combod
    global evald
    global scored
    global score
    score = 0
    if (start is False):
        step = False
        board = [[0 for i in range(4)] for j in range(4)]
        board = add(add(board))
        combod = []
        evald = []
        scored = []
        history = []
        history.append("".join(["".join([str(y) for y in x]) for x in board]))
        for i in range(4):
            for j in range(4):
                app.grid[i][j][1].configure(text=str(board[i][j]) if board[i][j] != 0 else "", bg=hex(
                    [int(x) for x in bgcolors[str(board[i][j])]]), fg="gray1")
                app.grid[i][j][0].configure(bg=hex([int(x) for x in bgcolors[str(board[i][j])]]))
        app.plots[0][0].plot(combod, color='blue', linewidth=1)
        app.plots[0][1].draw()
        app.plots[1][0].plot(evald, color='orange', linewidth=1)
        app.plots[1][1].draw()
        app.search.configure(text="Searched: " )
        app.score.configure(text="Score: ")
        


def run():
    global fin
    global start
    global step
    global board
    try:
        disp(board)
        v = alg()
        board = shift(board, int(v), True)
        board = add(board)
        for i in range(4):
            for j in range(4):
                app.grid[i][j][1].configure(text=str(board[i][j]) if board[i][j] != 0 else "", bg=hex(
                    [int(x) for x in bgcolors[str(board[i][j])]]), fg="gray1")
                app.grid[i][j][0].configure(bg=hex([int(x) for x in bgcolors[str(board[i][j])]]))
        app.plots[0][0].plot(combod, color='blue', linewidth=1)
        app.plots[0][1].draw()
        app.plots[1][0].plot(evald, color='orange', linewidth=1)
        app.plots[1][1].draw()
        sumsa = sum(sumsdat)
        app.search.configure(text="Searched: " + str(combod[-1]))
        app.score.configure(text="Score: " + str(score))

        history.append(",".join([",".join([str(y) for y in x]) for x in board]))

        for i in range(4):
            app.moves[i].configure(text=round(sumsdat[i]))
            app.move_in.grid_rowconfigure(i, minsize=(sumsdat[i] / sumsa) * 500)

    except Exception as e:
        print(e)
        fin = True
        start = False
        step = False
        return
def save():
    global combod
    global scored
    global evald
    print(score)
    fig, axes = plt.subplots(3, 1, figsize=(8, 10))
    axes[0].plot(combod)
    axes[0].set_title('Scenarios Searched')
    axes[0].set_xlabel('Move')
    axes[0].set_ylabel('Value')
    axes[0].grid(True)
    axes[1].plot(scored, color='orange')
    axes[1].set_title('Score')
    axes[1].set_xlabel('Move')
    axes[1].set_ylabel('Value')
    axes[1].grid(True)
    axes[2].plot(evald, color='orange')
    axes[2].set_title('Eval')
    axes[2].set_xlabel('Move')
    axes[2].set_ylabel('Value')
    axes[2].grid(True)
    plt.tight_layout()
    plt.savefig('debugdata.png', dpi=300)  # Save to file

def step():
    global start
    if (start is False):
        run()
def toggle():
    global start
    start = not start
    if (start is True):
        app.start.configure(text="Stop")

    else:
        app.start.configure(text="Start")

    go() 
def go():
    if (start is True):
        run()
        app.sidebar.after(100, go)

def historya():
    if (len(history) > 0):
        HistoryDialog(app, history)



# # Adjust layout and save
# plt.tight_layout()
# plt.savefig('debugdata.png', dpi=300)  # Save to file


# TESTING CODE - leave alone for now
# board = add(board)
# while True:
#     disp(board)
#     dir = 0
#     inp = (str(input(":")))
#     if (inp == "a"):
#         dir = 3
#     elif (inp == "s"):
#         dir = 2
#     elif (inp == "d"):
#         dir = 4
#     else:
#         dir = 1
#     shi = shift([[k for k in x] for x in board], dir)
#     if (shi != board):
#         board = shi
#         board = add(board)


app = App(save, step, toggle, reset, historya)
app.mainloop()
