import tkinter as tk
import tkinter.font as tkf
import random as rd

polices = ["BelleAllureCE", "Alphas", "Roboto"]
sizes = [50, 36, 60]
n_polices = len(polices)
alphabet = ["A", "B", "C", "D", "E", "F", "G", " H", "I", "J", "K", " L",
            "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", " X", "Y", "Z"]
count = 5 # nombre de lettre à chercher sur l'écran
gridcol = 4
gridrow = 3
gridsize = gridcol*gridrow
basicFont = "Arial"

def lettertoDisplay(indextoLook, lettertoLook):
    # pos of the letter to look in the grid
    A = [k for k in range(gridsize)]
    rd.shuffle(A)
    pos_lettertoLook = A[0: count]
    Letters = [-1 for k in range(gridsize)]
    for pos in pos_lettertoLook:
        Letters[pos] = lettertoLook
    new_alphabet = alphabet[:indextoLook]+alphabet[indextoLook+1:]
    for k in range(gridsize):
        if Letters[k] == -1:
            Letters[k] = new_alphabet[rd.randrange(0, 25)]
    return Letters


def jeu():
    main.grid_forget()
    game.grid(row=0, column=0)
    for widgets in frameToChoose.winfo_children():
        widgets.destroy()
    global currentCount
    currentCount = 0
    indextoLook = rd.randrange(0, 26)
    lettertoLook = alphabet[indextoLook]
    Letters = lettertoDisplay(indextoLook, lettertoLook)

    labelConsigne.configure(
        text=f"Vous devez choisir la lettre {lettertoLook}. Cliquez dessus")

    def clickEvent(event):
        global currentCount
        letter = event.widget.cget('text').upper()
        if letter == lettertoLook:
            event.widget.grid_forget()
            currentCount += 1
            if currentCount == count:
                start_screen()
                labelFinish.configure(text="Vous avez gagné")
                labelReponse.configure(text="")
            else:
                labelReponse.configure(text="Bravo c'est la bonne lettre")
        else:
            labelReponse.configure(text="Vous vous êtes trompé. Réessayez")
    
    fill_grid(Letters, clickEvent)

def fill_grid(Letters, clickEvent):
    for row in range(gridrow):
        for col in range(gridcol):
            lettre = Letters[col + row*gridcol]
            k = rd.randrange(0, n_polices)
            police = polices[k]
            size = sizes[k]
            if police == "Alphas":
                lettre = lettre.lower()
            else:
                if rd.randint(0, 1):
                    lettre = lettre.lower()
            font = tkf.Font(family=police, size=size)
            lab = tk.Label(frameToChoose, font=font, text=lettre)
            frameToChoose.rowconfigure(row, weight=1, minsize=250)
            frameToChoose.columnconfigure(col, weight=1, minsize=250)
            lab.grid(row=row, column=col)
            lab.bind('<Button-1>', clickEvent)

def start_screen():
    game.grid_forget()
    main.grid(row=0, column=0)


def create_start_screen():
    global main
    main = tk.Frame(root)
    main.rowconfigure(0, weight=1, minsize=200)
    main.rowconfigure(1, weight=1, minsize=200)
    main.rowconfigure(2, weight=1, minsize=200)
    main.rowconfigure(3, weight=1, minsize=200)
    main.columnconfigure(0, weight=1, minsize=800)

    global labelFinish
    labelFinish = tk.Label(main, text="", font=(basicFont, 30))
    labelFinish.grid(row=1, column=1)

    btn = tk.Button(main, text="jouer", command=jeu)
    btn['font'] = tkf.Font(family=basicFont, size=24)
    btn.grid(row=2, column=1)

    btn = tk.Button(main, text="Quitter", command=root.quit)
    btn['font'] = tkf.Font(family=basicFont, size=24)
    btn.grid(row=3, column=1)


def create_game_screen():
    global game
    game = tk.Frame(root)
    game.rowconfigure(0, weight=1, minsize=80)
    game.rowconfigure(1, weight=1, minsize=120)
    game.rowconfigure(2, weight=1, minsize=600)
    game.columnconfigure(0, weight=1, minsize=400)

    global labelConsigne
    labelConsigne = tk.Label(game, font=(basicFont, 24))
    labelConsigne.grid(row=0, column=1)

    global labelReponse
    labelReponse = tk.Label(game, font=(basicFont, 24))
    labelReponse.grid(row=1, column=1)

    global frameToChoose
    frameToChoose = tk.Frame(game)
    frameToChoose.grid(row=2, column=1)

if __name__=="__main__":
    root = tk.Tk()
    root.title("J'apprends à reconnaître les lettres")
    root.attributes('-toolwindow', True)
    root.attributes('-fullscreen', True)
    create_start_screen()
    create_game_screen()
    start_screen()
    root.mainloop()
