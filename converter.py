from classroom import *
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
        worksheet = workbook.add_worksheet(name)
        table = [
            ['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00','12.00-12.30','12.30-13.00', '13.00-13.30', '13.30-14.00',
                '14.00-14.30', '14.30-15.00', '15.00-15.30', '15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'],
            ['Monday'],
            ['Tuesday'],
            ['Wednesday'],
            ['Thursday'],
            ['Friday'],
        ]

        for i in range(len(teacher['subjects'])):
            subject = teacher['subjects'][i]
            subjectName = subject['name']
            if i == 0:
                for _class in subject['classes']:
                    periods = _class['periods']
                    for period in range(1,18):
                        if str(period) in periods:
                            if len(_class['teacher']) != 0:
                                table[_class['day'].find('1')+1].append(subjectName + '\n' + _class['teacher'][0])
                                
                            else:
                                table[_class['day'].find('1')+1].append(subjectName)
                        else:
                            table[_class['day'].find('1')+1].append('')
            else:
                for _class in subject['classes']:
                    for period in _class['periods']:
                        if len(_class['teacher']) != 0:
                            
                            table[_class['day'].find('1')+1][int(period)] = subjectName + '\n' + _class['teacher'][0]
                            
                        else:
                            table[_class['day'].find(
                                '1')+1][int(period)] = subjectName

        print(table)
        print(len(table), len(table[1]))
        for i in range(len(table)):
            for j in range(len(table[0])):
                try:
                    worksheet.write(i, j, table[i][j], cell_format)
                except:
                    worksheet.write(i, j, '', cell_format)
        
        worksheet.merge_range(0, 7, 5, 8, 'Break', cell_format)
        print('done!')
        worksheet.set_column(0,17, 14)
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
        list = [['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00', '12.00-12.30', '12.30-13.00', '13.00-13.30', '13.30-14.00', '14.00-14.30', '14.30-15.00', '15.00-15.30', '15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30'], 
                ['Monday', '13Med,13Com Character Development', '13Med,13Com Character Development', '', '', '', '', '', '', "8B Creative Drama\nP'Its", "8B Creative Drama\nP'Its", "8B Creative Drama\nP'Its", "8A Creative Drama\nP'Its", "8A Creative Drama\nP'Its", "8A Creative Drama\nP'Its", '', '', ''], 
                ['Tuesday', '', '', '', "13 Creative Drama\nP'Its", "13 Creative Drama\nP'Its", "13 Creative Drama\nP'Its", '', '', '', '', '', "11 Creative Drama\nP'Its", "11 Creative Drama\nP'Its", "11 Creative Drama\nP'Its", '', '', ''], 
                ['Wednesday', '', '', '', '', '', '', '', '', '', '', '', "10 Creative Drama\nP'Its", "10 Creative Drama\nP'Its", "10 Creative Drama\nP'Its", '', '', ''], 
                ['Thursday', '', '', '', '', '', '', '', '', "9AB Creative Drama\nP'Its", "9AB Creative Drama\nP'Its", "9AB Creative Drama\nP'Its", '', '', '', '', '', ''], 
                ['Friday', "11ABCD IELTS by P'Tong\nP'Tong", "11ABCD IELTS by P'Tong\nP'Tong", "11ABCD IELTS by P'Tong\nP'Tong", "11ABCD IELTS by P'Tong\nP'Tong", '', '', '', '', '', '', '', "12 Creative Drama\nP'Its", "12 Creative Drama\nP'Its", "12 Creative Drama\nP'Its", '', '', '']]
    workbook.close()

convertMain()
