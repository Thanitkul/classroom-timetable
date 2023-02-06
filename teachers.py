import sys
from bs4 import BeautifulSoup

def main():
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
            lesson_ids = []
            for lesson in lessons:
                lesson_ids.append(lesson.get('id'))
            teacherTimetable[index]['lesson'] = lesson_ids
            index+=1
 

        print(teacherTimetable)
main()