import csv
import os


def main():
    file_size = os.stat("text.csv").st_size
    with open("text.csv", 'a', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "Balance", "winnings"])
        if file_size == 0:
            print("going")
            writer.writeheader()
        writer.writerow({
            "name": "Krishna",
            "Balance": 2000,
            "winnings": 150
        })

main()