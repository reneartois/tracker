import tkinter as tk
from gui import Gui


def main():
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
