import pytesseract
import numpy as np
import src.dataIO as io
import matplotlib.pyplot as plt

from PIL import Image
from pathlib import Path
from fuzzywuzzy import fuzz

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

root = Path().absolute()
image_path = Path(f'{root}/test.png')
image = Image.open(image_path)

info_path = Path(f'{root}/Info.json')
info_dict = io.load_json(file_path=info_path)
managers_dict = info_dict['Managers']
all_teams = []
for key, value in managers_dict.items():
    for team in value:
        all_teams.append(team)

text = pytesseract.image_to_string(image)
print(text)

lines = text.split('\n\n')
print(lines)

names = []
points = []
characters_to_remove = ",\n"
for line in lines:
    for char in characters_to_remove:
        line = line.replace(char, "")
    if line.isdigit():
        points.append(int(line))
    else:
        names.append(line)
print(names, len(names))
print(points, len(points))

best_match = [f'{i}' for i in range(len(names))]
best_score = np.zeros(len(names))
for index, name in enumerate(names):
    for team in all_teams:
        score = fuzz.ratio(name, team)
        if score > best_score[index]:
            best_match[index] = team
            best_score[index] = score

print(names, best_match, best_score)

corrected = {}
sheet = {}
for n, p in zip(names, points):
    sheet.update({n: p})
print(sheet)

i = [i for i in range(len(names))]
for index, match, score, point in zip(i, best_match, best_score, points):
    if score < 75:
        corrected.update({f'Unknown {index}': point})
    else:
        corrected.update({match: point})
print(corrected)
