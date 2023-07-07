import sys
from bs4 import BeautifulSoup
import re
import more_itertools as mit

classroomTimetable = {}



def sort_classroom_timetable():
    with open(sys.argv[1], 'r') as f:
        data = f.read()
        timetables = BeautifulSoup(data, "xml")
        for club in timetables.find_all("subject", {'name':'Club'}):
            club.decompose()
        
        classroomTimetable = {
            "FL 9": {
                '10000': {},
                '01000': {},
                '00100': {},
                '00010': {},
                '00001': {}
            },
            "FL 9A": {
                '10000': {},
                '01000': {},
                '00100': {},
                '00010': {},
                '00001': {}
            },
            "FL 11": {
                '10000': {},
                '01000': {},
                '00100': {},
                '00010': {},
                '00001': {}
            }
        }

        for classroom in timetables.find_all('classroom'):
            name = classroom.get('name')
            classroomId = classroom.get('id')
            nameSplit = name.split(' ')
            
            if (nameSplit[len(nameSplit) - 1] == '9' and nameSplit[len(nameSplit) - 2] == 'FL'):
                add_room(classroomTimetable, name, 'FL 9')
            elif (nameSplit[len(nameSplit) - 1] == '9A' and nameSplit[len(nameSplit) - 2] == 'FL'):
                add_room(classroomTimetable, name, 'FL 9A')
            elif (nameSplit[len(nameSplit) - 1] == '11' and nameSplit[len(nameSplit) - 2] == 'FL'):
                add_room(classroomTimetable, name, 'FL 11')


        for card in timetables.find_all('card'):
            #print(card)
            lessonId = card.get('lessonid')
            day = card.get('days')
            period = card.get('period')
            classroomIds = card.get('classroomids').split(',')
            if classroomIds[0] == '':
                continue
            classroomNames = []

            if (len(classroomIds) > 1):
                for i in range(0, len(classroomIds)):
                    classroomNames.append(timetables.find('classroom', {'id': classroomIds[i]}).get('name'))
            else:
                classroomNames.append(timetables.find('classroom', {'id': classroomIds[0]}).get('name'))
            
            lesson = timetables.find('lesson', {'id': lessonId})
            subjectid = lesson.get('subjectid')
            subjectName = timetables.find('subject', {'id': subjectid}).get('name')

            teacherids = lesson.get('teacherids').split(',')
            teacherNames = []
            if (len(teacherids) > 1):
                for i in range(0, len(teacherids)):
                    teacherNames.append(timetables.find('teacher', {'id': teacherids[i]}).get('name'))
            elif (len(teacherids) == 1 and teacherids[0] != ''):
                teacherNames.append(timetables.find('teacher', {'id': teacherids[0]}).get('name'))
            
            payload = {
                'subjectName': subjectName,
                'teacherNames': teacherNames,
                'period': period
            }

            for classroomName in classroomNames:
                nameSplit = classroomName.split(' ')
                if (nameSplit[len(nameSplit) - 1] == '9' and nameSplit[len(nameSplit) - 2] == 'FL'):
                    classroomTimetable['FL 9'][day][classroomName].append(payload)
                elif (nameSplit[len(nameSplit) - 1] == '9A' and nameSplit[len(nameSplit) - 2] == 'FL'):
                    classroomTimetable['FL 9A'][day][classroomName].append(payload)
                elif (nameSplit[len(nameSplit) - 1] == '11' and nameSplit[len(nameSplit) - 2] == 'FL'):
                    classroomTimetable['FL 11'][day][classroomName].append(payload)

    #sort by period
    for floor in classroomTimetable:
        for day in classroomTimetable[floor]:
            for classroom in classroomTimetable[floor][day]:
                #sort array of dict by element period
                classroomTimetable[floor][day][classroom] = sorted(classroomTimetable[floor][day][classroom], key=lambda k: int(k['period']))

    #delete duplicate periods in the same day
    for floor in classroomTimetable:
        for day in classroomTimetable[floor]:
            for classroom in classroomTimetable[floor][day]:
                classroomTimetable[floor][day][classroom] = list(mit.unique_everseen(classroomTimetable[floor][day][classroom], key=lambda k: k['period']))



    with open('classroomTimetable.json', 'w') as f:
        f.write(str(classroomTimetable))


def add_room(classroomTimetable, name, floor):
    for i in range(0,5):
        days = "0" * i + "1" + "0" * (4-i)
        classroomTimetable[floor][days][name] = []

def main():
    sort_classroom_timetable()

main()
