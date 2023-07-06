from classroom2 import *
import random
import types
import xlsxwriter
from collections import Counter


def convertMain():
    writeOnExcel()


def writeOnExcel():
    classroomTimetable = sort_classroom_timetable()
    workbook = xlsxwriter.Workbook('result_xlsx_files/classroom_time_table.xlsx')
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_border(1)
    

    floors = list(classroomTimetable.keys())
    header = ['', '9.00-9.30', '9.30-10.00', '10.00-10.30', '10.30-11.00', '11.00-11.30', '11.30-12.00','12.00-12.30','12.30-13.00', '13.00-13.30', '13.30-14.00',
                '14.00-14.30', '14.30-15.00', '15.00-15.30', '15.30-16.00', '16.00-16.30', '16.30-17.00', '17.00-17.30', '17.30-17.50']
    numberOfPeriod = 18
    periodSpace = ['' for i in range(numberOfPeriod)]


    for floor in floors:
        days = list(classroomTimetable[floor].keys())
        worksheet = workbook.add_worksheet(floor)
        rowNumber = 0
        header[0] = floor + 'th'
        for i in range(len(header)):
            worksheet.write(rowNumber, i, header[i], cell_format)
        rowNumber += 1 
        for day in days:
            rooms = list(classroomTimetable[floor][day].keys())
            for roomName in rooms:
                periodSpace.insert(0, 'Class ' + roomName)
                room = classroomTimetable[floor][day][roomName]
                allDuplicatedLessons = []
                duplicatedLessons = []
                for i in range(len(room)):
                    if i < len(room) -1 :                        
                        if room[i + 1]["subjectName"] == room[i]["subjectName"]:
                            print(room[i + 1]["subjectName"],'==', room[i]["subjectName"])
                            print(room[i + 1]["period"])
                            # print(periodSpace)
                            allDuplicatedLessons.append(int(room[i + 1]["period"]))
                            duplicatedLessons.append(int(room[i + 1]["period"]))
                        elif room[i + 1]["subjectName"] != room[i]["subjectName"]:
                            # print(len(duplicatedLessons))
                            if len(duplicatedLessons) == 0:
                                firstLessonPeriod = int(room[i]["period"])
                            else:
                                firstLessonPeriod = min(duplicatedLessons) - 1
                            print(duplicatedLessons)
                            print(firstLessonPeriod)
                            periodSpace[firstLessonPeriod] = {"name": room[i]["subjectName"] + '\n' + (' '.join(room[i]["teacherNames"])), "numberOfDuplication": len(duplicatedLessons)}
                            duplicatedLessons = []
                            
                        else:
                            print('something went wrong')
                    else:
                        if len(duplicatedLessons) == 0:
                                firstLessonPeriod = int(room[i]["period"])
                        else:
                            firstLessonPeriod = min(duplicatedLessons) - 1
                            periodSpace[firstLessonPeriod] = {"name": room[i]["subjectName"] + '\n' + (' '.join(room[i]["teacherNames"])), "numberOfDuplication": len(duplicatedLessons)}
                
                # print(allDuplicatedLessons)
                print(periodSpace)
                allDuplicatedLessons.reverse()
                for delPeriod in allDuplicatedLessons:
                    # print(delPeriod)
                    # print(periodSpace)
                    del periodSpace[delPeriod]
                allDuplicatedLessons = []
                # for lesson in room:
                #     periodSpace[int(lesson["period"])] = lesson["subjectName"] + '\n' + (' '.join(lesson["teacherNames"]))
                print(periodSpace)
                worksheet.write(rowNumber, 0, periodSpace[0], cell_format)
                i = 1
                while i < len(periodSpace):
                    
                    if periodSpace[i] == '':
                        worksheet.write(rowNumber, i, 'periodSpace[0]', cell_format)
                        
                    else:
                        worksheet.merge_range(rowNumber, i, rowNumber, i +  int(periodSpace[i]["numberOfDuplication"]), periodSpace[i]["name"], cell_format)
                        i += int(periodSpace[i]["numberOfDuplication"])
                    i += 1
                rowNumber += 1
                periodSpace = ['' for i in range(numberOfPeriod)]

    workbook.close()




convertMain()
