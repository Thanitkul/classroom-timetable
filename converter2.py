from classroom2 import *
import random
import types
import xlsxwriter
from collections import Counter


def convertMain():
    writeOnExcel()


def writeOnExcel():
    classroomTimetable = sort_classroom_timetable()
    workbook = xlsxwriter.Workbook("result_xlsx_files/classroom_time_table.xlsx")
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align("center")
    cell_format.set_align("vcenter")
    cell_format.set_border(1)
    
    header_format = workbook.add_format()
    header_format.set_text_wrap()
    header_format.set_align("center")
    header_format.set_align("vcenter")
    header_format.set_border(1)
    header_format.set_bold(True)
    header_format.set_font_size(30)

    blank_format = workbook.add_format()
    blank_format.set_text_wrap()
    blank_format.set_align("center")
    blank_format.set_align("vcenter")
    blank_format.set_bold(True)
    blank_format.set_font_size(20)

    blankodd_format = workbook.add_format()
    blankodd_format.set_text_wrap()
    blankodd_format.set_align("center")
    blankodd_format.set_align("vcenter")
    blankodd_format.set_border(1)
    blankodd_format.set_right_color(right_color= '#ffffff')

    blankeven_format = workbook.add_format()
    blankeven_format.set_text_wrap()
    blankeven_format.set_align("center")
    blankeven_format.set_align("vcenter")
    blankeven_format.set_border(1)
    blankeven_format.set_left_color(left_color= '#ffffff')

    floors = list(classroomTimetable.keys())
    dayDecode = {
        "10000": "Monday",
        "01000": "Tuesday",
        "00100": "Wednesday",
        "00010": "Thursday",
        "00001": "Friday",
    }
    header = [
        "",
        "9.00-9.30",
        "9.30-9.50",
        "10.00-10.30",
        "10.30-10.50",
        "11.00-11.30",
        "11.30-11.50",
        "12.00-12.30",
        "12.30-13.00",
        "13.00-13.30",
        "13.30-13.50",
        "14.00-14.30",
        "14.30-14.50",
        "15.00-15.30",
        "15.30-15.50",
        "16.00-16.30",
        "16.30-16.50",
        "17.00-17.30",
        "17.30-17.50",
    ]
    numberOfPeriod = 18
    periodSpace = ["" for i in range(numberOfPeriod)]

    for floor in floors:
        days = list(classroomTimetable[floor].keys())
        worksheet = workbook.add_worksheet(floor)
        worksheet.set_column(0,0,10)
        rowNumber = 0
        header[0] = floor + " th"

        
        for day in days:
            worksheet.merge_range(
                rowNumber, 0, rowNumber, numberOfPeriod, ' ', blank_format
            ) 
            rowNumber += 1
            worksheet.merge_range(
                rowNumber, 0, rowNumber, numberOfPeriod, dayDecode[day], header_format
            )
            rowNumber += 1        
            for i in range(len(header)):
                worksheet.write(rowNumber, i, header[i], cell_format)
            rowNumber += 1
            rooms = list(classroomTimetable[floor][day].keys())
            for roomName in rooms:
                periodSpace.insert(0, "Class " + roomName)
                room = classroomTimetable[floor][day][roomName]
                allDuplicatedLessons = []
                duplicatedLessons = []
                for i in range(len(room)):
                    if i < len(room) - 1:
                        if room[i + 1]["subjectName"] == room[i]["subjectName"] and (
                            (int(room[i]["period"]) != 6)
                        ):
                            # print(room[i + 1]["subjectName"],'==', room[i]["subjectName"])
                            # print(room[i + 1]["period"])
                            # print(periodSpace)
                            allDuplicatedLessons.append(int(room[i + 1]["period"]))
                            duplicatedLessons.append(int(room[i + 1]["period"]))
                        elif room[i + 1]["subjectName"] != room[i]["subjectName"] or (
                            int(room[i]["period"]) == 6
                        ):
                            print(room[i])
                            # print(len(duplicatedLessons))
                            if len(duplicatedLessons) == 0:
                                firstLessonPeriod = int(room[i]["period"])
                            else:
                                firstLessonPeriod = min(duplicatedLessons) - 1
                            print(duplicatedLessons)
                            print(firstLessonPeriod)
                            if len(room[i]["teacherNames"]) != 0:
                                periodSpace[firstLessonPeriod] = {
                                    "name": room[i]["subjectName"]
                                    + "\n"
                                    + (" ".join(room[i]["teacherNames"])),
                                    "numberOfDuplication": len(duplicatedLessons),
                                }
                            else:
                                periodSpace[firstLessonPeriod] = {
                                    "name": room[i]["subjectName"]
                                    ,
                                    "numberOfDuplication": len(duplicatedLessons),
                                }
                            duplicatedLessons = []

                        else:
                            print("something went wrong")
                    else:
                        if len(duplicatedLessons) == 0:
                            firstLessonPeriod = int(room[i]["period"])
                        else:
                            firstLessonPeriod = min(duplicatedLessons) - 1
                            periodSpace[firstLessonPeriod] = {
                                "name": room[i]["subjectName"]
                                + "\n"
                                + (" ".join(room[i]["teacherNames"])),
                                "numberOfDuplication": len(duplicatedLessons),
                            }

                # print(allDuplicatedLessons)
                # print(periodSpace)
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
                j = 1
                while i < len(periodSpace):
                    # print(i)
                    # print(periodSpace[i])
                    if periodSpace[i] == "":
                        if j % 2 == 1:
                            worksheet.write(rowNumber, j, "", blankodd_format)
                        else:
                            worksheet.write(rowNumber, j, "", blankeven_format)

                    else:
                        worksheet.merge_range(
                            rowNumber,
                            j,
                            rowNumber,
                            j + int(periodSpace[i]["numberOfDuplication"]),
                            periodSpace[i]["name"],
                            cell_format,
                        )
                        j += int(periodSpace[i]["numberOfDuplication"])
                    i += 1
                    j += 1
                worksheet.merge_range(
                            rowNumber,
                            7,
                            rowNumber,
                            8,
                            'Lunch',
                            cell_format,
                        )
                
                rowNumber += 1
                periodSpace = ["" for i in range(numberOfPeriod)]
    workbook.close()


convertMain()
