from classroom2 import *
import random
import types
import xlsxwriter
from collections import Counter


def convertMain():
    writeOnExcel()


def writeOnExcel():
    teacherTimetable = sort_classroom_timetable()
    workbook = xlsxwriter.Workbook('result_xlsx_files/classroom_time_table.xlsx')
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_border(1)
    k = 0
    for teacher in teacherTimetable:
        print(teacherTimetable)
        name = teacher['name']
        worksheet = workbook.add_worksheet(name)
        table = [
            ['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00','12.00-12.30','12.30-13.00', '13.00-13.30', '13.30-14.00',
                '14.00-14.30', '14.30-15.00', '15.00-15.30', '15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'],
            ['Monday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Tuesday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Wednesday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Thursday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Friday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ]

        for subject in teacher['subjects']:
            subjectName = subject['name']
            for _class in subject['classes']:
                subjectGroup = []
                periods = [int(i) for i in _class['periods']]
                if len(_class['teacher']) != 0:
                    for period in periods:
                        subjectGroup.append(subjectName + '\n' + _class['teacher'][0])
                    if len(periods) != 0:
                        print(table[_class['day'].find('1')+1])
                        print(min(periods))
                        table[_class['day'].find('1')+1][min(periods)] = subjectGroup

                else:
                    for period in periods:
                        subjectGroup.append(subjectName)
                    if len(periods) != 0:
                        table[_class['day'].find('1')+1][min(periods)] = subjectGroup
        print(len(table[2]))
        print('before',table)
        for subject in teacher['subjects']:
            for _class in subject['classes']:
                periods = [int(i) for i in _class['periods']] 
                if len(periods) > 1:
                    print('full', periods)
                    print('day',_class['day'].find('1')+1, 'period', periods[1], max(periods) + 1)
                    del table[_class['day'].find('1')+1][periods[1]: max(periods) + 1]
        print(len(table[2]))
        print('after',table)
        
        for i in range(len(table)):
            p = 0
            j = 0
            while j < len(table[i]):
                print(i, p, table[i][j])
                print(table[i])
                if isinstance(table[i][j], list):
                    worksheet.merge_range(i, p, i, p + len(table[i][j]) -1, table[i][j][0], cell_format)
                    p += len(table[i][j])
                else:
                    worksheet.write(i, p, table[i][j], cell_format)
                    p += 1
                j += 1
            print(table[i])
        
        # worksheet.merge_range(0, 7, 5, 8, 'Break', cell_format)


        if k == 3:
            pass
        k += 1
    workbook.close()

    a = [['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00', '12.00-12.30', '12.30-13.00', '13.00-13.30', '13.30-14.00', '14.00-14.30', '14.30-15.00', '15.00-15.30','15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'], 
         ['Monday', ['13Med,13Com Character Development', '13Med,13Com Character Development'], '', '', '', '', '', '', ["8B Creative Drama\nP'Its", "8B Creative Drama\nP'Its", "8B Creative Drama\nP'Its"], ["8A Creative Drama\nP'Its", "8A Creative Drama\nP'Its", "8A Creative Drama\nP'Its"], '', '', ''], 
         ['Tuesday', '', '', '', ["13 Creative Drama\nP'Its", "13 Creative Drama\nP'Its", "13 Creative Drama\nP'Its"], '', '', '', '', '', ["11 Creative Drama\nP'Its", "11 Creative Drama\nP'Its", "11 Creative Drama\nP'Its"], '', '', ''], 
         ['Wednesday', '', '', '', '', '', '', '', '', '', '', '', ["10 Creative Drama\nP'Its", "10 Creative Drama\nP'Its", "10 Creative Drama\nP'Its"], '', '', ''], 
         ['Thursday', '', '', '', '', '', '', '', '', ["9AB Creative Drama\nP'Its", "9AB Creative Drama\nP'Its", "9AB Creative Drama\nP'Its"], '', '', '', '', '', ''], 
         ['Friday', ["11ABCD IELTS by P'Tong\nP'Tong", "11ABCD IELTS by P'Tong\nP'Tong", "11ABCD IELTS by P'Tong\nP'Tong", "11ABCD IELTS by P'Tong\nP'Tong"], '', '', '', '', '', '', '', ["12 Creative Drama\nP'Its", "12 Creative Drama\nP'Its", "12 Creative Drama\nP'Its"], '', '', '']]
    b = [['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00', '12.00-12.30', '12.30-13.00', '13.00-13.30', '13.30-14.00', '14.00-14.30', '14.30-15.00', '15.00-15.30','15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'], 
         ['Monday', '', '', '', '', '', '', '', '', ['8A Taekwando\nTaekwondo Master', '8A Taekwando\nTaekwondo Master', '8A Taekwando\nTaekwondoMaster'], ['8B Taekwando\nTaekwondo Master', '8B Taekwando\nTaekwondo Master', '8B Taekwando\nTaekwondo Master'], '', '', ''], 
         ['Tuesday', '', '', '', '', '', '', '', '', '', '', '', ['11 Taekwando\nTaekwondo Master', '11 Taekwando\nTaekwondo Master', '11 Taekwando\nTaekwondo Master'], ["8,9 Fundamental Math (Selected Students)\nP'Cee", "8, 9 Fundamental Math(Selected Students)\nP'Cee"], '', ''], 
         ['Wednesday', '', '', '', '', '', '', '', '', '', '', '', ['10 Taekwando\nTaekwondo Master', '10 Taekwando\nTaekwondo Master', '10 Taekwando\nTaekwondo Master'], '', '', ''], 
         ['Thursday', '', '', '', '', '', '', '', '', ["9CD Creative Drama\nP'Its", "9CD Creative Drama\nP'Its", "9CD Creative Drama\nP'Its"], ['9 Taekwando\nTaekwondo Master', '9 Taekwando\nTaekwondo Master', '9 Taekwando\nTaekwondo Master'], '', '', ''], 
         ['Friday', '', '', '', '', '', '', '', '', '', '', '', ['12 Taekwando\nTaekwondo Master', '12 Taekwando\nTaekwondo Master', '12 Taekwando\nTaekwondo Master'], '', '']]

    c = [['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00', '12.00-12.30', '12.30-13.00', '13.00-13.30', '13.30-14.00', '14.00-14.30', '14.30-15.00', '15.00-15.30', '15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'], 
        ['Monday', ['8A Character Development', '8A Character Development'], ["8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju"], '', '', '', '', '', '', '', '', '', ["8,9,10 Fundamental English (Selected Students)\nP'France", "8,9,10 Fundamental English (Selected Students)\nP'France"], '', ''], 
        ['Tuesday', ["8A Chinese\nP'Noon", "8A Chinese\nP'Noon"], ['8A English\nMs.Leelee', '8A English\nMs.Leelee', '8A English\nMs.Leelee', '8A English\nMs.Leelee'], '', '', '', '', ["8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju"], '', ''], 
        ['Wednesday', ['8A English\nMs.Leelee', '8A English\nMs.Leelee', '8A English\nMs.Leelee', '8A English\nMs.Leelee'], ["8A Thai\nP'Prae", "8A Thai\nP'Prae"], '', '', ["8A ICT\nP'Ith", "8A ICT\nP'Ith"], ["8A Science\nP'Amy", "8A Science\nP'Amy"], '', ["8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju"], '', ''], 
        ['Thursday', ["8A Chinese\nP'Noon", "8A Chinese\nP'Noon"], ["8A Thai\nP'Prae", "8A Thai\nP'Prae"], '', '', '', ["8A Science\nP'Amy", "8A Science\nP'Amy"], '', ["8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju", "8A Mathematics\nP'Paoju"], '', ''], 
        ['Friday', ["8A Science\nP'Amy", "8A Science\nP'Amy", "8A Science\nP'Amy", "8A Science\nP'Amy"], ['8A Reading Great Literature\nMs.Leelee', '8A Reading Great Literature\nMs.Leelee'], '', '', '', ['8A English\nMs.Leelee', '8A English\nMs.Leelee', '8A English\nMs.Leelee', '8A English\nMs.Leelee'], '', '', '', '','']]
convertMain()
