import tkinter as tk
from gui import Gui


def main():
    root = tk.Tk()
    root.title("Estimator")
    app = Gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
