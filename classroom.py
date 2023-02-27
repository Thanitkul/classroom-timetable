import sys
from bs4 import BeautifulSoup

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
            lessons = timetables.find_all("lesson", {'classroomids': classroom['id']})
            lessons_info = []
            for lesson in lessons:
                lesson_info = {
                    "id": lesson.get('id'),
                    "name": timetables.find('subject', {'id': lesson.get('subjectid')}).get('name'),
                    "classes": []
                }
                
                for i in range(0,5):
                    days = "0" * i + "1" + "0" * (4-i)
                    cards = timetables.find_all("card", {'lessonid': lesson_info['id'], 'days': days})
                    
                    day = {
                        "day": days,
                        "teacher": [],
                        "periods": []
                    }
                    teachers = timetables.find_all("teacher", {'id': lesson.get('teacherids')})
                    for teacher in teachers:
                        day['teacher'].append(teacher.get('name'))
                    for card in cards:
                        day['periods'].append(card.get("period"))
                    lesson_info['classes'].append(day)

                lessons_info.append(lesson_info)
            classroomTimetable[index]['subjects'] = lessons_info
            index+=1
        print(classroomTimetable)
        return classroomTimetable
        
 
def classroom(cards, timetables):
    if (len(cards) != 0) :
        classroom_id = cards[0].get("classroomids")
        name = ""
        if classroom_id == "":
            name = "Not assigned"
        elif ',' in classroom_id:
            classroom_ids = classroom_id.split(",")
            for room_id in classroom_ids:
                name += timetables.find("classroom", {'id': room_id}).get("name") + ','
        else:
            name = timetables.find("classroom", {'id': classroom_id}).get("name")
        return name
    else:
        pass

main()
