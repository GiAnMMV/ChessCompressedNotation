from tkinter import *
import base64

board = [
    # a   b   c   d   e   f   g   h
    [+2, +3, +4, +5, +6, +4, +3, +2], #1
    [+1, +1, +1, +1, +1, +1, +1, +1], #2
    [ 0,  0,  0,  0,  0,  0,  0,  0], #3
    [ 0,  0,  0,  0,  0,  0,  0,  0], #4
    [ 0,  0,  0,  0,  0,  0,  0,  0], #5
    [ 0,  0,  0,  0,  0,  0,  0,  0], #6
    [-1, -1, -1, -1, -1, -1, -1, -1], #7
    [-2, -3, -4, -5, -6, -4, -3, -2]  #8
]
enpassant = -1
castle = {-1: {0:True, 7:True}, 1: {0:True, 7:True}}
turn = 1
king_pos = {-1: {'x': 4, 'y': 7}, 1: {'x': 4, 'y': 0}}

pieces = {0: '', 1: 'w_pawn', 2: 'w_rook', 3: 'w_knight', 4: 'w_bishop', 5: 'w_queen', 6: 'w_king', -1: 'b_pawn', -2: 'b_rook', -3: 'b_knight', -4: 'b_bishop', -5: 'b_queen', -6: 'b_king'}
pieces2 = {0: ' ', 1: '\u2659', 2: '\u2656', 3: '\u2658', 4: '\u2657', 5: '\u2655', 6: '\u2654', -1: '\u265F', -2: '\u265C', -3: '\u265E', -4: '\u265D', -5: '\u265B', -6: '\u265A'}
piece_letters = ['', '', 'R', 'N', 'B', 'Q', 'K']

xnames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ynames = ['1', '2', '3', '4', '5', '6', '7', '8']


def sign(n):
    if n > 0: return 1
    elif n < 0: return -1
    else: return n

def incheck(x,y,side):
    for d in range(8):
        if   d == 0: tx, ty = x+2*side, y+1*side
        elif d == 1: tx, ty = x+1*side, y+2*side
        elif d == 2: tx, ty = x-1*side, y+2*side
        elif d == 3: tx, ty = x-2*side, y+1*side
        elif d == 4: tx, ty = x-2*side, y-1*side
        elif d == 5: tx, ty = x-1*side, y-2*side
        elif d == 6: tx, ty = x+1*side, y-2*side
        elif d == 7: tx, ty = x+2*side, y-1*side

        if (ty <= 7) and (ty >= 0) and (tx <= 7) and (tx >= 0) and board[ty][tx] == -side*3:
            return True

    for d in range(8):
        tx, ty = x, y
        while True:
            if   d == 0: tx, ty = tx+side, ty
            elif d == 1: tx, ty = tx-side, ty
            elif d == 2: tx, ty = tx,      ty+side
            elif d == 3: tx, ty = tx,      ty-side
            elif d == 4: tx, ty = tx+side, ty+side
            elif d == 5: tx, ty = tx-side, ty-side
            elif d == 6: tx, ty = tx+side, ty-side
            elif d == 7: tx, ty = tx-side, ty+side

            if (ty > 7) or (ty < 0) or (tx > 7) or (tx < 0) or sign(board[ty][tx]) == side: break
            elif board[ty][tx] and sign(board[ty][tx]) != side:
                if d < 4 and (board[ty][tx] == -side*2 or board[ty][tx] == -side*5):
                    return True
                elif d >= 4 and (board[ty][tx] == -side*4 or board[ty][tx] == -side*5):
                    return True
                elif ty == y+side and (tx == x+1 or tx == x-1) and board[ty][tx] == -side*1:
                    return True
                elif abs(ty-y) <= 1 and abs(tx-x) <= 1 and board[ty][tx] == -side*6:
                    return True
                else: break                
    return False
            

def piece_moves(x,y):
    t = []
    side = sign(board[y][x])
    piece = abs(board[y][x])
    if piece == 2 or piece == 4 or piece == 5: #Rook, bishop, queen
        for c in range(2):
            for d in range(4):
                if (piece == 2 or piece == 5) and c == 0:
                    if   d == 0: mx, my =  side,     0
                    elif d == 1: mx, my = -side,     0
                    elif d == 2: mx, my =     0,  side
                    elif d == 3: mx, my =     0, -side
                elif (piece == 4 or piece == 5) and c == 1:
                    if   d == 0: mx, my =  side,  side
                    elif d == 1: mx, my = -side, -side
                    elif d == 2: mx, my =  side, -side
                    elif d == 3: mx, my = -side,  side
                else: break
                tx, ty = x, y
                while True:
                    tx += mx
                    ty += my
                        
                    if (ty > 7) or (ty < 0) or (tx > 7) or (tx < 0):
                        break
                    elif sign(board[ty][tx]) == side:
                        break
                    else:
                        t.append((x,y,tx,ty))
                        if board[ty][tx]:
                            break
    elif piece == 1: #Pawn
        tx, ty = x, y+1*side
        if not board[ty][tx]:
            if (side == 1 and ty == 7) or (side == -1 and ty == 0):
                for p in range(2,6): t.append((x,y,tx,ty,p))
            else:
                t.append((x,y,tx,ty))
            if (side == 1 and y == 1) or (side == -1 and y == 6):
                tx, ty = tx, ty+1*side
                if not board[ty][tx]:
                    t.append((x,y,tx,ty))
        for a in range(-1, 2, 2):
            tx, ty = x+1*side*a, y+1*side
            if (tx <= 7) and (tx >= 0):
                if board[ty][tx] and sign(board[ty][tx]) != side:
                    if (side == 1 and ty == 7) or (side == -1 and ty == 0):
                        for p in range(1,6): t.append((x,y,tx,ty,p))
                    else:
                        t.append((x,y,tx,ty))
                elif enpassant == tx and y == (-3*side)%7:
                    t.append((x,y,tx,ty))
    elif piece == 3: #Knight
        for d in range(8):
            if   d == 0: tx, ty = x+2*side, y+1*side
            elif d == 1: tx, ty = x+1*side, y+2*side
            elif d == 2: tx, ty = x-1*side, y+2*side
            elif d == 3: tx, ty = x-2*side, y+1*side
            elif d == 4: tx, ty = x-2*side, y-1*side
            elif d == 5: tx, ty = x-1*side, y-2*side
            elif d == 6: tx, ty = x+1*side, y-2*side
            elif d == 7: tx, ty = x+2*side, y-1*side
            if (ty <= 7) and (ty >= 0) and (tx <= 7) and (tx >= 0) and sign(board[ty][tx]) != side:
                t.append((x,y,tx,ty))
    elif piece == 6: #King
        for d in range(8):
            if   d == 0: tx, ty = x+side, y
            elif d == 1: tx, ty = x+side, y+side
            elif d == 2: tx, ty = x,      y+side
            elif d == 3: tx, ty = x-side, y+side
            elif d == 4: tx, ty = x-side, y
            elif d == 5: tx, ty = x-side, y-side
            elif d == 6: tx, ty = x,      y-side
            elif d == 7: tx, ty = x+side, y-side
            if (ty <= 7) and (ty >= 0) and (tx <= 7) and (tx >= 0) and sign(board[ty][tx]) != side:
                t.append((x,y,tx,ty))
        if castle[side][0]:
            if not board[y][1] and not board[y][2] and not board[y][3] and not incheck(x,y,side) and not incheck(x-1,y,side):
                t.append((x,y,x-2,y))
        if castle[side][7]:
            if not board[y][6] and not board[y][5] and not incheck(x,y,side) and not incheck(x+1,y,side):
                t.append((x,y,x+2,y))
    return t
        
def do_move(m):
    global turn
    global enpassant

    ax, ay = m[0], m[1]
    bx, by = m[2], m[3]
    a = board[ay][ax]
    b = board[by][bx]
    side = sign(a)
    epset = False
    if (abs(a) == 2 and ax in castle[side] and castle[side][ax] and ay == side%7-side) or (abs(b) == 2 and bx in castle[side] and castle[side][bx] and by == side%7-side):
        castle[side][ax] = False
    elif abs(a) == 6 and (castle[side][0] or castle[side][7]):
        castle[side][0] = False
        castle[side][7] = False
        if bx-ax == 2:
            board[ay][5] = board[ay][7]
            board[ay][7] = 0
        elif m[2]-m[0] == -2:
            board[ay][3] = board[ay][0]
            board[ay][0] = 0
    elif abs(a) == 1:
        if abs(by-ay) == 2:
            enpassant = ax
            epset = True
        elif enpassant == bx and ax != bx:
            board[(-3*turn)%7][bx] = 0

    board[by][bx] = a
    if len(m) == 5:
        board[by][bx] = m[4]*side
    board[ay][ax] = 0

    turn = -turn
    if not epset: enpassant = -1

def legal_moves():
    global enpassant
    global turn

    t = []
    for y in range(8):
        y = turn%7-turn+turn*y
        for x in range(8):
            if sign(board[y][x]) == turn:
                t += piece_moves(x,y)
                if board[y][x] == turn*6:
                    king_pos[turn]['x'], king_pos[turn]['y'] = x, y
    t1 = []
    for m in t:
        ax, ay = m[0], m[1]
        bx, by = m[2], m[3]
        a = board[ay][ax]
        b = board[by][bx]
        kx, ky = king_pos[turn]['x'], king_pos[turn]['y']
        ep = enpassant
        
        c1, c2, c3, c4 = castle[1][0], castle[-1][0], castle[1][7], castle[-1][7]

        do_move(m)
        turn = -turn
        if abs(a) == 6: kx, ky = m[2], m[3]
        
        if not incheck(kx, ky, turn): t1.append(m)
        board[m[1]][m[0]] = a
        board[m[3]][m[2]] = b
        if abs(a) == 1 and ax != bx and bx == ep: board[(-3*turn)%7][m[2]] = -turn*1
        castle[1][0], castle[-1][0], castle[1][7], castle[-1][7] = c1, c2, c3, c4
        enpassant = ep
        if abs(a) == 6:
            if m[2]-m[0] == 2:
                board[m[1]][7] = board[m[1]][m[0]+1]
                board[m[1]][m[0]+1] = 0
            elif m[2]-m[0] == -2:
                board[m[1]][0] = board[m[1]][m[0]-1]
                board[m[1]][m[0]-1] = 0
    return t1

def from_algebraic(alg):
    res = ''
    prom = 0
    piece = 0
    moves_num = 0
    score = 0
    alg = alg.replace('.', '. ')
    for w in alg.split():
        if w == '1-0': score = 2
        elif w == '0-1': score = 1
        elif w == '1/2-1/2': score = 3
        elif w[-1] != '.':
            moves_num += 1
            ax, ay = -1, -1
            bx, by = -1, -1
            l = legal_moves()
            if w[:3] == 'O-O' or w[:3] == '0-0':
                piece = 6
                ax, ay = 4, turn%7-turn
                if len(w) == 5:
                    bx, by = 2, turn%7-turn
                else:
                    bx, by = 6, turn%7-turn
            else:
                w = w.replace('+','').replace('#','').replace('x','')
                if not w[0].isupper():
                    piece = 1
                    if w[-2] == '=':
                        prom = piece_letters.index(w[-1])
                        w = w[:-2]
                else:
                    piece = piece_letters.index(w[0])
                    w = w[1:]
                
                bx, by = xnames.index(w[-2]), ynames.index(w[-1])
                w = w[:-2]
                for a in w:
                    if a.isnumeric():
                        ay = ynames.index(a)
                    else:
                        ax = xnames.index(a)
            error = True
            for m in l:
                if piece == abs(board[m[1]][m[0]]) and m[2] == bx and m[3] == by and (ax == -1 or m[0] == ax) and (ay == -1 or m[1] == ay) and (len(m) == 4 or prom == m[4]):
                    res += bin(l.index(m))[2:].zfill(len(bin(len(l))[2:]))
                    do_move(m)
                    error = False
                    break
            if error: raise Exception('Invalid move.')
    res += '0'*(-len(res)%8)
    print(len(res))
    res = bin(moves_num)[2:].zfill(14) + bin(score)[2:].zfill(2) + res
    res = bytes(int(res[i : i + 8], 2) for i in range(0, len(res), 8))
    res = base64.b64encode(res).decode()
    return res



def from_code(code):
    code = base64.b64decode(code)
    code = ''.join(bin(i)[2:].zfill(8) for i in code)
    moves_num = int(code[:14], 2)
    score = int(code[14:16], 2)
    code = code[16:]
    res = ''
    l = legal_moves()
    for n in range(moves_num):
        m = l[int(code[:len(bin(len(l))[2:])], 2)]
        code = code[len(bin(len(l))[2:]):]

        if abs(board[m[1]][m[0]]) == 6 and abs(m[2] - m[0]) == 2:
            if m[2] - m[0] == 2:
                res += 'O-O'
            else:
                res += 'O-O-O'
        else:
            isEat = False
            isX = False
            isY = False
            if n // 2 == n / 2: res += str(n//2+1) + '. '
            res += piece_letters[abs(board[m[1]][m[0]])]
            for mo in l:
                if mo != m and board[mo[1]][mo[0]] == board[m[1]][m[0]] and mo[2] == m[2] and mo[3] == m[3]:
                    if mo[0] == m[0]:
                        isY = True
                    else:
                        isX = True
            if board[m[3]][m[2]] or (abs(board[m[1]][m[0]]) == 1 and abs(m[2]-m[0]) == 1):
                if abs(board[m[1]][m[0]]) == 1:
                    isX = True
                isEat = True
            res += xnames[m[0]]*isX + ynames[m[1]]*isY + 'x'*isEat + xnames[m[2]] + ynames[m[3]]
            
        do_move(m)
        l = legal_moves()
        if incheck(king_pos[turn]['x'], king_pos[turn]['y'], turn):
            if len(l): res += '+'
            else: res += '#'
        res += ' '
    if score == 2: res += '1-0'
    elif score == 1: res += '0-1'
    elif score == 3: res += '1/2-1/2'
    return res

