import tkinter as tk
import json
import os

dictionary = {
    "Driver 1": [],
    "Driver 2": [],
    "Driver 3": [],
    "Driver 4": [],
    "Driver 5": [],
    "Team": [],
    "Turbo Driver": [],
    "Mega Driver": [],
    "Penalties": [],
    "Wildcard": []
}
lineup = {
    "Mercedes": ["Hamilton", "Bottas"],
    "Red Bull": ["Verstappen", "Perez"],
    "McLaren": ["Ricciardo", "Norris"],
    "Aston Martin": ["Vettel", "Stroll"],
    "Alpine": ["Alonso", "Ocon"],
    "Ferrari": ["Leclerc", "Sainz"],
    "AlphaTauri": ["Gasly", "Tsunoda"],
    "Alfa Romeo": ["Raikkonen", "Giovinazzi"],
    "Haas": ["Schumacher", "Mazepin"],
    "Williams": ["Russell", "Latifi"]
}
races = ["Bahrain", "Imola", "Monaco", "Spain", "Portugal", "Austria"]


def commando(team_dict, x, y):
    team_dict[f'{x}'].extend([y])
    print(team_dict)


def dump_json(out_path, dictionary):
    with open(out_path, 'w') as outfile:
        json.dump(dictionary, outfile, indent=2)
        outfile.write('\n')


def get_config(config_path):
    if config_path:
        with open(config_path, 'r') as f:
            return json.load(f)


dump_json(out_path=os.path.join(os.getcwd(), "test.config"), dictionary=dictionary)
test_dict = get_config(config_path=os.path.join(os.getcwd(), "test.config"))

for race in races:
    root = tk.Tk()
    root.title("Test")
    
    driver_1 = tk.StringVar()
    driver_2 = tk.StringVar()
    driver_3 = tk.StringVar()
    driver_4 = tk.StringVar()
    driver_5 = tk.StringVar()
    team = tk.StringVar()
    turbo = tk.StringVar()
    mega = tk.StringVar()
    penalties = tk.IntVar()
    wildcard = tk.IntVar()

    driver_1_label = tk.Label(root, text="Driver 1: ")
    driver_1_entry = tk.Entry(root, text=driver_1)
    driver_1_label.grid(row=1, column=0)
    driver_1_entry.grid(row=1, column=1)

    driver_2_label = tk.Label(root, text="Driver 2: ")
    driver_2_entry = tk.Entry(root, text=driver_2)
    driver_2_label.grid(row=2, column=0)
    driver_2_entry.grid(row=2, column=1)

    driver_3_label = tk.Label(root, text="Driver 3: ")
    driver_3_entry = tk.Entry(root, text=driver_3)
    driver_3_label.grid(row=3, column=0)
    driver_3_entry.grid(row=3, column=1)

    driver_4_label = tk.Label(root, text="Driver 4: ")
    driver_4_entry = tk.Entry(root, text=driver_4)
    driver_4_label.grid(row=4, column=0)
    driver_4_entry.grid(row=4, column=1)

    driver_5_label = tk.Label(root, text="Driver 5: ")
    driver_5_entry = tk.Entry(root, text=driver_5)
    driver_5_label.grid(row=5, column=0)
    driver_5_entry.grid(row=5, column=1)

    but = tk.Button(
        root,
        text="Update",
        command=lambda: [
            commando(team_dict=test_dict, x="Driver 1", y=driver_1.get()),
            commando(team_dict=test_dict, x="Driver 2", y=driver_2.get()),
            dump_json(out_path=os.path.join(os.getcwd(), "test.config"), dictionary=test_dict),
            root.destroy()])
    but.grid(row=11, column=2)

    root.mainloop()

