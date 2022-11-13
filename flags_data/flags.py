import json

try:
    flags_pl = json.load(open("flags_data\\FlagsData_PL.json", 'r', encoding="utf-8"))
    flags_en = json.load(open("flags_data\\FlagsData_EN.json", 'r', encoding="utf-8"))
    language_flags = {"PL": flags_pl, "EN": flags_en}
except FileNotFoundError:
    print("Some language files are missing. Donwload them from here: ")
    input("Press enter to close the program.")
    quit()
