import tkinter as tk
from tkinter import ttk

class TurnCounter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pathfinder Turn Counter")
        self.geometry("800x600")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.current_player_index = None

        self.create_widgets()
        self.grid_widgets()

    def reset_names(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.current_player_index = None


    def create_widgets(self):
        self.left_frame = tk.Frame(self, padx=10, pady=10)
        self.top_left_frame = tk.Frame(self.left_frame)

        self.next_turn_button = tk.Button(self.top_left_frame, text="Next Turn", command=self.next_turn)
        self.reset_turn_button = tk.Button(self.top_left_frame, text="Reset", command=self.reset_turn)
        self.turn_label = tk.Label(self.left_frame, text="Turn 1")

        self.name_label = tk.Label(self.left_frame, text="Name")
        self.name_entry = tk.Entry(self.left_frame)
        self.health_label = tk.Label(self.left_frame, text="Health")
        self.health_entry = tk.Entry(self.left_frame)
        self.add_name_button = tk.Button(self.left_frame, text="Add Name", command=self.add_name)

        self.name_entry.bind("<Return>", lambda event: self.health_entry.focus())
        self.health_entry.bind("<Return>", lambda event: (self.add_name(), self.name_entry.focus()))

        self.treeview_frame = tk.Frame(self.left_frame)
        self.treeview = ttk.Treeview(self.treeview_frame, columns=("Name", "Health"), show="headings")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Health", text="Health")
        self.treeview.column("Name", width=200)
        self.treeview.column("Health", width=100)

        self.treeview_scrollbar = ttk.Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar.set)

        self.next_player_button = tk.Button(self.left_frame, text="Next Player", command=self.next_player)

        self.adjust_hp_label = tk.Label(self.left_frame, text="Adjust HP")
        self.adjust_hp_entry = tk.Entry(self.left_frame)
        self.adjust_hp_button = tk.Button(self.left_frame, text="Adjust HP", command=self.adjust_hp)
        self.adjust_hp_entry.bind("<Return>", lambda event: self.adjust_hp())

        self.reset_names_button = tk.Button(self.left_frame, text="Reset Names", command=self.reset_names)

        self.menu = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)


    def grid_widgets(self):
        self.left_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.top_left_frame.grid(row=0, column=0, sticky=tk.NW)
        self.next_turn_button.grid(row=0, column=0, pady=5, padx=(0, 5), sticky=tk.W)
        self.reset_turn_button.grid(row=0, column=1, pady=5, sticky=tk.W)

        self.turn_label.grid(row=1, column=0, pady=10, sticky=tk.W)

        self.name_label.grid(row=2, column=0, pady=5, sticky=tk.W)
        self.name_entry.grid(row=3, column=0, pady=5, sticky=tk.W)
        self.health_label.grid(row=4, column=0, pady=5, sticky=tk.W)
        self.health_entry.grid(row=5, column=0, pady=5, sticky=tk.W)
        self.add_name_button.grid(row=6, column=0, pady=5, sticky=tk.W)

        self.treeview_frame.grid(row=7, column=0, pady=5, sticky=tk.NSEW)
        self.treeview.grid(row=0, column=0, sticky=tk.NSEW)
        self.treeview_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.treeview_frame.columnconfigure(0, weight=1)
        self.treeview_frame.rowconfigure(0, weight=1)

        self.next_player_button.grid(row=8, column=0, pady=5, sticky=tk.W)
        self.reset_names_button.grid(row=9, column=0, pady=5, sticky=tk.W)

        self.adjust_hp_label.grid(row=10, column=0, pady=5, sticky=tk.W)
        self.adjust_hp_entry.grid(row=11, column=0, pady=5, sticky=tk.W)
        self.adjust_hp_button.grid(row=12, column=0, pady=5, sticky=tk.W)

        self.config(menu=self.menu)


    def next_turn(self):
        turn_number = int(self.turn_label.cget("text").split(" ")[1]) + 1
        self.turn_label.config(text=f"Turn {turn_number}")

    def reset_turn(self):
        self.turn_label.config(text="Turn 1")

    def add_name(self):
        name = self.name_entry.get()
        health = self.health_entry.get()
        new_item = None
        if name and health:
            if self.current_player_index is None:
                self.current_player_index = 0
            new_item = self.treeview.insert("", tk.END, values=(name, health))
            if len(self.treeview.get_children()) == 1:
                self.treeview.selection_set(new_item)
                self.current_player_index = 0
            self.name_entry.delete(0, tk.END)
            self.health_entry.delete(0, tk.END)

    def next_player(self):
        player_count = len(self.treeview.get_children())
        if player_count > 0:
            self.treeview.selection_remove(self.treeview.get_children()[self.current_player_index])
            self.current_player_index = (self.current_player_index + 1) % player_count
            self.treeview.selection_add(self.treeview.get_children()[self.current_player_index])

    def adjust_hp(self):
        selected_item = self.treeview.selection()
        hp_adjustment = self.adjust_hp_entry.get()
        if selected_item and hp_adjustment:
            hp_adjustment = int(hp_adjustment)
            current_hp = int(self.treeview.item(selected_item, "values")[1])
            new_hp = current_hp + hp_adjustment

            if new_hp <= 0:
                name = self.treeview.item(selected_item, "values")[0]
                self.treeview.item(selected_item, values=(name, 0))
                self.treeview.tag_configure("strikethrough", font=("Arial", 12, "overstrike"))
                self.treeview.tag_bind("strikethrough", "<1>", lambda e: "break")
                self.treeview.item(selected_item, tags=("strikethrough",))
            else:
                self.treeview.set(selected_item, "Health", new_hp)
                self.treeview.item(selected_item, tags=(""))

            self.adjust_hp_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = TurnCounter()
    app.mainloop()
