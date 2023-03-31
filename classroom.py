import sys
from bs4 import BeautifulSoup
import re
import more_itertools as mit

def main():
    sort_teacher_timetable()

def sort_teacher_timetable():
    with open(sys.argv[1], 'r') as f:
        data = f.read()
        timetables = BeautifulSoup(data, "xml")
        for club in timetables.find_all("subject", {'name':'Club'}):
            club.decompose()
        classroomTimetable = []

        #teachers
        classrooms = timetables.find_all('classroom')
        for classroom in classrooms:
            classroomTimetable.append({ "id": classroom.get('id'), "name": classroom.get('name')})

        #lessons
        index = 0
        for classroom in classroomTimetable:
            lessons = timetables.find_all("lesson", classroomids = re.compile(classroom['id']))
            #print(lessons)
            lessons_info = []
            for lesson in lessons:
                #print(lesson)
                #print(lesson.get('subjectid'))
                #print(timetables.find('subject', {'id': lesson.get('subjectid')}))
                lesson_info = {
                    "id": lesson.get('id'),
                    "name": timetables.find('subject', {'id': lesson.get('subjectid')}).get('name'),
                    "classes": []
                }
                
                for i in range(0,5):
                    days = "0" * i + "1" + "0" * (4-i)
                    #print(lesson_info['id'])
                    cards = timetables.find_all("card", {'lessonid': lesson_info['id'], 'days': days})
                    #print(cards)
                    
                    day = {
                        "day": days,
                        "teacher": []
                    }
                    teachers = timetables.find_all("teacher", {'id': lesson.get('teacherids')})
                    for teacher in teachers:
                        day['teacher'].append(teacher.get('name'))
                    periods = []
                    for card in cards:
                        #print(card.get("period"))
                        periods.append(int(card.get("period")))
                        periods.sort()
                    groupPeriods = [list(group) for group in mit.consecutive_groups(periods)]
                    day['periods'] = groupPeriods
                    lesson_info['classes'].append(day)

                lessons_info.append(lesson_info)
            classroomTimetable[index]['subjects'] = lessons_info
            index+=1
        outFile = open('resultdata.txt', 'w')
        outFile.write(str(classroomTimetable))
        outFile.close()
        
        days = ['10000', '01000', '00100', '00010', '00001']
        rearrange = {
            "FL 9": [],
            "FL 9A": [],
            "FL 11": []
        }

        for floor in rearrange:
            for day in days:
                thatday = {"day": day}
                for room in classroomTimetable:
                    thatday[room['name']] = []
                    for _subject in room['subjects']:
                        subject = { 'subject': _subject['name'], 'classes': []}
                        for _class in _subject['classes']:
                            print(_class)
                            if thatday['day'] == _class['day']:
                                subject['classes'].append(_class)
                        thatday[room['name']].append(subject)
                        
                    break
                rearrange[floor].append(thatday)
        print(rearrange)

        return rearrange
        

main()
