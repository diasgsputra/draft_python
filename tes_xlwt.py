import xlwt

book = xlwt.Workbook()

sheet1 = book.add_sheet('Sheet1')

book.save("tes_xlwt_1.xls")
