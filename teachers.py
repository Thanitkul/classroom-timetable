import sys
from bs4 import BeautifulSoup

def main():
    sort_teacher_timetable()

def sort_teacher_timetable():
    with open(sys.argv[1], 'r') as f:
        data = f.read()
        timetables = BeautifulSoup(data, "xml")
        teacherTimetable = []

        #teachers
        teachers = timetables.find_all('teacher')
        for teacher in teachers:
            teacherTimetable.append({ "id": teacher.get('id'), "name": teacher.get('name')})

        #lessons
        index = 0
        for teacher in teacherTimetable:
            lessons = timetables.find_all("lesson", {'teacherids': teacher['id']})
            lessons_info = []
            for lesson in lessons:
                lesson_info = {
                    "id": lesson.get('id'),
                    "name": timetables.find('subject', {'id': lesson.get('subjectid')}).get('name'),
                    "classes": []
                }
                
                for i in range(0,6):
                    days = "0" * i + "1" + "0" * (5-i)
                    cards = timetables.find_all("card", {'lessonid': lesson_info['id'], 'days': days})
                    day = {
                        "day": days,
                        "classroomid": classroom(cards),
                        "periods": []
                    }
                    for card in cards:
                        day['periods'].append(card.get("period"))
                    lesson_info['classes'].append(day)

                lessons_info.append(lesson_info)
            teacherTimetable[index]['periods'] = lessons_info
            index+=1

        print(teacherTimetable)
 
def classroom(cards):
    if (len(cards) != 0) :
        return cards[0].get("classroomids")
    else:
        pass

main()