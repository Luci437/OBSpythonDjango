import xlrd
from obsapp.models import *

alldata = xlrd.open_workbook("final questions.xlsx")
sheets = alldata.sheet_by_index(0)

datas = []

for i in range(1,5):
    for y in range(6):
        datas.append(sheets.cell_value(i,y))
    qstobj = Questions()
    qstobj.qsttype = datas[0]
    qstobj.question = datas[1]
    qstobj.option1 = datas[2]
    qstobj.option2 = datas[3]
    qstobj.option3 = datas[4]
    qstobj.option4 = datas[5]
    qstobj.answer = datas[6]
    qstobj.save()
    datas.clear()
print("All data added to Database successfully.")

