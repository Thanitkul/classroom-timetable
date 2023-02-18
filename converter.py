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
        print(name)
        worksheet = workbook.add_worksheet(name + id[:3])
        table = [
            ['Date', '1', '2', '3', '4', '5', '6', '7', '8',
                '9', '10', '11', '12', '13', '14', '15'],
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
                    table[_class['day'].find('1')+1][int(period)] = subjectName
        print(table)  
        print('-' * 50)
        for i in range(7):
            for j in range(16):
                worksheet.write(i, j, table[i][j], cell_format)

        worksheet.set_column(0,16, 12)
        worksheet.set_default_row(40)

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
