import csv

with open("pythonbyShifu!!/marsk.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for line in csv_reader:
        name = line["names"]
        marks = line["marks"]
        print(f"Name: {name}   Marks:{marks}")