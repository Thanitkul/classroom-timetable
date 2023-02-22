from teachers import *
import random
import xlsxwriter


def convertMain():
    writeOnExcel()


def writeOnExcel():
    teacherTimetable = sort_teacher_timetable()
    workbook = xlsxwriter.Workbook('result_xlsx_files/teacher_time_table.xlsx')
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_border(1)
    for teacher in teacherTimetable:
        name = teacher['name']
        id = teacher['id']
        worksheet = workbook.add_worksheet(name + id[:3])
        table = [
            ['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00', '13.00-13.30', '13.30-14.00',
                '14.00-14.30', '14.30-15.00', '15.00-15.30', '15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'],
            ['Monday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Tuesday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Wednesday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Thursday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Friday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Saturday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]

        for subject in teacher['subjects']:
            subjectName = subject['name']
            for _class in subject['classes']:
                for period in _class['periods']:
                    if _class['classroom'] != None:
                        table[_class['day'].find('1')+1][int(period)] = subjectName + '\n' + _class['classroom'] 
                    else:
                        table[_class['day'].find(
                            '1')+1][int(period)] = subjectName

        for i in range(7):
            for j in range(16):
                worksheet.write(i, j, table[i][j], cell_format)

        worksheet.set_column(0,16, 14)
        worksheet.set_default_row(105)
        worksheet.set_landscape()

        #         for subject in teacher['subjects']:
        #     subjectName = subject['name']
        #     for _class in subject['classes']:
        #         for period in _class['periods']:
        #             table[_class['day'].find('1')+1][int(period)] = subjectName
        # print(table)  
        # print('-' * 50)
        # for i in range(7):
        #     if i != 0:
        #         periods = np.unique(table[i][1:])
        #         for period in periods:
                    
        #             j = sorted(np.where(table[i] == period))
        #             print(j)
        #             worksheet.merge_range(i, j[0][0], j[0][len(j) - 1], i, table[i][j[0][0]], cell_format)
        #     # else:
        #     #     worksheet.write(i, , table[i][j], cell_format)

    workbook.close()

convertMain()
