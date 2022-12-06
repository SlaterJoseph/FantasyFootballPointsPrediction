# Creating the CSVs of the 6 positions for fantasy football
from xlwt import Workbook

ff_pos = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

for pos in ff_pos:
    wb = Workbook()
    sheet1 = wb.add_sheet(pos + "_data")
    wb.save("../CSV Files/" + pos + "_data.csv")
