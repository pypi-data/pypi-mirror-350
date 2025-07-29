import pygame as pg
import inspect
def print_all_keys():
    

    print("All defined keys:\n")

    for name, value in inspect.currentframe().f_globals.items():
        if isinstance(value, int) and pg.key.name(value) != "":
            print(f"{name:10} -> {pg.key.name(value)} ({value})")

a = pg.K_a
b = pg.K_b
c = pg.K_c
d = pg.K_d
e = pg.K_e
f = pg.K_f
g = pg.K_g
h = pg.K_h
i = pg.K_i
j = pg.K_j
k = pg.K_k
l = pg.K_l
m = pg.K_m
n = pg.K_n
o = pg.K_o
p = pg.K_p
q = pg.K_q
r = pg.K_r
s = pg.K_s
t = pg.K_t
u = pg.K_u
v = pg.K_v
w = pg.K_w
x = pg.K_x
y = pg.K_y
z = pg.K_z

e0 = pg.K_0
e1 = pg.K_1
e2 = pg.K_2
e3 = pg.K_3
e4 = pg.K_4
e5 = pg.K_5
e6 = pg.K_6
e7 = pg.K_7
e8 = pg.K_8
e9 = pg.K_9

space = pg.K_SPACE
enter = pg.K_RETURN
escape = pg.K_ESCAPE
tab = pg.K_TAB
backspace = pg.K_BACKSPACE
delete = pg.K_DELETE
shift = pg.K_LSHIFT
shiftr = pg.K_RSHIFT
ctrl = pg.K_LCTRL
ctrlr = pg.K_RCTRL
altl = pg.K_LALT;optionl=altl
altr = pg.K_RALT;optionr=altr
com = pg.K_LMETA
comr = pg.K_RMETA
left = pg.K_LEFT
right = pg.K_RIGHT
up = pg.K_UP
down = pg.K_DOWN

f1 = pg.K_F1
f2 = pg.K_F2
f3 = pg.K_F3
f4 = pg.K_F4
f5 = pg.K_F5
f6 = pg.K_F6
f7 = pg.K_F7
f8 = pg.K_F8
f9 = pg.K_F9
f10 = pg.K_F10
f11 = pg.K_F11
f12 = pg.K_F12
if __name__=="__main__":
    print_all_keys()