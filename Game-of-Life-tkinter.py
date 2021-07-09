import tkinter as tk
import numpy as np
from scipy.signal import fftconvolve
from tkinter import ttk

def instantiate_grid():
    global grid, cell_height, cell_width, n
    n = size.get()
    print(n)
    grid = np.zeros(n*n).reshape(n,n)
    cell_width = canvas_width/(n)
    cell_height = canvas_height/(n)
    update_canvas()


def evolve():
    global grid, n, running
    neighbour_count = np.round(fftconvolve(grid,neighbour_kernel,mode='same'))
    
    # R1 = (A==1) & (neighbour_count<2)
    R2 = (grid==1) & ((neighbour_count>1) & (neighbour_count<4))
    # R3 = (A==1) & (neighbour_count>3)
    R4 = (grid==0) & (neighbour_count==3)
    
    grid = np.zeros(n*n).reshape(n,n)
    grid[R2|R4] = 1
    update_canvas()
    if running:
        canvas.after(100,evolve)

def give_life(event):
    global grid, cell_height, cell_width, n
    x,y = event.x,event.y
    row = int(x/cell_width)
    col= int(y/cell_height)
    grid[row,col] = 1
    canvas.create_rectangle(row*cell_width+1,col*cell_height+1,
                            (row+1)*cell_width-1,(col+1)*cell_height-1,
                            fill='#FFFFFF')

def remove_life(event):
    global grid, cell_height, cell_width, n
    x,y = event.x,event.y
    row = int(x/cell_width)
    col = int(y/cell_height)
    grid[row,col] = 0
    canvas.create_rectangle(row*cell_width+1,col*cell_height+1,
                            (row+1)*cell_width-1,(col+1)*cell_height-1,
                            fill='#000000')

def update_canvas():
    global grid, cell_height, cell_width, n
    canvas.delete('all')
    for i in range(n):
        for j in range(n):
            if grid[i,j]==1:
                canvas.create_rectangle(i*cell_width+1,j*cell_height+1,
                                        (i+1)*cell_width-1,(j+1)*cell_height-1,
                                        fill='#FFFFFF')
            else:
                canvas.create_rectangle(i*cell_width+1,j*cell_height+1,
                                        (i+1)*cell_width-1,(j+1)*cell_height-1,
                                        fill='#000000')


def reset_func():
    global running
    running = False
    instantiate_grid()

def run_game():
    global running
    running = True
    evolve()

win = tk.Tk()
win.title('Game of Life')
win.geometry('550x500')

main_screen = tk.Frame(win, padx=5, pady=5)
main_screen.pack(side='left')

side_menu = tk.Frame(win, padx=5, pady=5)
side_menu.pack(side='right')


size_select_label = tk.Label(side_menu, text='Select Size')
size_select_label.pack()
size = tk.IntVar()
size_select = ttk.Combobox(side_menu, width = 10, textvariable = size)
size_select['values'] = (30,40,50,60,70,80,90,100)
size_select.pack()
size_select.current(2)

reset_button = ttk.Button(side_menu, text='Reset', command=reset_func)
reset_button.pack()

run_button = ttk.Button(side_menu, text='Run!', command=run_game)
run_button.pack()

exit_button = ttk.Button(side_menu, text='Quit', command=lambda:[print(grid),win.destroy()])
exit_button.pack()

neighbour_kernel = np.ones(9).reshape(3,3)
neighbour_kernel[1,1] = 0

canvas_width = 400
canvas_height = canvas_width
canvas = tk.Canvas(main_screen, width = canvas_width, height = canvas_height, background = "#0000ff")

canvas.bind('<B1-Motion>', give_life)
canvas.bind('<Button-1>', give_life)
canvas.bind('<B3-Motion>', remove_life)
canvas.bind('<Button-3>', remove_life)
canvas.pack()

running = True
instantiate_grid()
win.mainloop()