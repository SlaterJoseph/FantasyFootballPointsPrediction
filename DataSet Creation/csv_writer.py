import csv


def write_csv(pos: str, name: str) -> None:
    writer = csv.writer(open('../CSV Files/' + pos + "_data.csv", 'w'))
    writer.writerow([name])
