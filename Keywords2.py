def prepareChart(workbook):
    global worksheet
    chart1 = workbook.add_chart({'type': 'line'})

    chart1.add_series({
        'name':       '=Frequency',
        'categories': '=Sheet1!$A$2:$A$24',
        'values':     '=Sheet1!$B$2:$B$24'
    })
    chart1.add_series({
        'name':       '=Density',
        'categories': '=Sheet1!$A$2:$A$24',
        'values':     '=Sheet1!$C$2:$C$24'
    })
    chart1.set_title ({'name': 'Results of sample analysis'})
    chart1.set_x_axis({'name': 'Keywords'})
    chart1.set_y_axis({'name': 'Density , Frequency'})

    chart1.set_style(10)

    worksheet.insert_chart('D2', chart1)
    workbook.close()
def writeExcelOutput(cursor):
    import xlsxwriter
    workbook=xlsxwriter.Workbook('OutputExcel.xlsx')
    global worksheet
    worksheet=workbook.add_worksheet()
    worksheet.write('A1', 'Keyword')
    worksheet.write('B1', 'Frequency')
    worksheet.write('C1', 'Density')
    i=2
    print("Keywords  -  Frequency -  Density")
    for data in cursor:
        print(data[0].ljust(8)," - ",str(data[1]).ljust(8)," - ",data[2])
        x='A'+str(i)
        y='B'+str(i)
        z='C'+str(i)
        worksheet.write(x,data[0])
        worksheet.write(y,data[1])
        worksheet.write(z,data[2])
        i=i+1
    prepareChart(workbook)
    print('Successfully wrote')
worksheet=""
import sqlite3
con=sqlite3.connect('mydb2.db')
print('Database created/connected')
cursor=con.execute('select keyword,count,dens from rec')
writeExcelOutput(cursor)
print("To see the chart open the output excel file")
cursor.close()
con.close()