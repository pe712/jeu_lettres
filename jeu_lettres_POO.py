import tkinter as tk
import tkinter.font as tkf
import random as rd

class Btn(tk.Button):
    def __init__(self, container, row, text, command):
        super().__init__(container, text=text, command=command)
        self['font'] = tkf.Font(family=container.master.basicFont, size=24)
        self.grid(row=row, column=1)

class Label(tk.Label):
    def __init__(self, container, row, size):
        super().__init__(container, font=(container.master.basicFont, size))
        self.grid(row=row, column=1)

class Main(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1, minsize=200)
        self.rowconfigure(1, weight=1, minsize=200)
        self.rowconfigure(2, weight=1, minsize=200)
        self.rowconfigure(3, weight=1, minsize=200)
        self.columnconfigure(0, weight=1, minsize=800)

        self.labelFinish = Label(self, 1, 30)

        Btn(self, 2, "Jouer", container.partie)
        Btn(self, 3, "Quitter", container.quit)

class Game(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1, minsize=80)
        self.rowconfigure(1, weight=1, minsize=120)
        self.rowconfigure(2, weight=1, minsize=600)
        self.columnconfigure(0, weight=1, minsize=400)

        self.labelConsigne = Label(self, 0, 24)

        self.labelReponse = Label(self, 1, 24)
        
        self.frameToChoose = tk.Frame(self)
        self.frameToChoose.grid(row=2, column=1)
   
class jeu_lettres(tk.Tk):
    polices = ["BelleAllureCE", "Alphas", "Roboto"]
    sizes = [50, 36, 60]
    alphabet = ["A", "B", "C", "D", "E", "F", "G", " H", "I", "J", "K", " L",
                "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", " X", "Y", "Z"]
    count = 5 # nombre de lettre à chercher sur l'écran
    gridcol = 4
    gridrow = 3
    gridsize = gridcol*gridrow
    basicFont = "Arial"    
    
    def __init__(self):
        super().__init__()
        self.title("J'apprends à reconnaître les lettres")
        self.attributes('-toolwindow', True)
        self.attributes('-fullscreen', True)
        self.main = Main(self)
        self.game = Game(self)
        self.start()
    
    def start(self):
        self.game.grid_forget()
        self.main.grid(row=0, column=0)
    
    def partie(self):
        self.main.grid_forget()
        self.game.grid(row=0, column=0)
        for widgets in self.game.frameToChoose.winfo_children():
            widgets.destroy()
        global currentCount
        currentCount = 0
        indextoLook = rd.randrange(0, 26)
        lettertoLook = self.alphabet[indextoLook]
        Letters = self.lettertoDisplay(indextoLook, lettertoLook)

        self.game.labelConsigne.configure(
            text=f"Vous devez choisir la lettre {lettertoLook}. Cliquez dessus")

        def clickEvent(event):
            global currentCount
            letter = event.widget.cget('text').upper()
            if letter == lettertoLook:
                event.widget.grid_forget()
                currentCount += 1
                if currentCount == self.count:
                    self.start()
                    self.main.labelFinish.configure(text="Vous avez gagné")
                    self.game.labelReponse.configure(text="")
                else:
                    self.game.labelReponse.configure(text="Bravo c'est la bonne lettre")
            else:
                self.game.labelReponse.configure(text="Vous vous êtes trompé. Réessayez")
        
        self.fill_grid(Letters, clickEvent)

    def lettertoDisplay(self, indextoLook, lettertoLook):
        # pos of the letter to look in the grid
        A = [k for k in range(self.gridsize)]
        rd.shuffle(A)
        pos_lettertoLook = A[0: self.count]
        Letters = [-1 for k in range(self.gridsize)]
        for pos in pos_lettertoLook:
            Letters[pos] = lettertoLook
        new_alphabet = self.alphabet[:indextoLook]+self.alphabet[indextoLook+1:]
        for k in range(self.gridsize):
            if Letters[k] == -1:
                Letters[k] = new_alphabet[rd.randrange(0, 25)]
        return Letters

    def fill_grid(self, Letters, clickEvent):
        for row in range(self.gridrow):
            for col in range(self.gridcol):
                lettre = Letters[col + row*self.gridcol]
                k = rd.randrange(0, len(self.polices))
                police = self.polices[k]
                size = self.sizes[k]
                if police == "Alphas":
                    lettre = lettre.lower()
                else:
                    if rd.randint(0, 1):
                        lettre = lettre.lower()
                font = tkf.Font(family=police, size=size)
                lab = tk.Label(self.game.frameToChoose, font=font, text=lettre)
                self.game.frameToChoose.rowconfigure(row, weight=1, minsize=250)
                self.game.frameToChoose.columnconfigure(col, weight=1, minsize=250)
                lab.grid(row=row, column=col)
                lab.bind('<Button-1>', clickEvent)

if __name__=="__main__":
    app = jeu_lettres()
    app.mainloop()
    
