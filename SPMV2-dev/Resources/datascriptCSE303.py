import pandas as pd
import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

course = Course_T(courseID='CSE303', courseName="Database Management", numOfCredits=4, programID=1,
                  courseType="Core") #change
course.save()

# CO
plolist = list(PLO_T.objects.filter(programID=1))

colist = []

colist.append(CO_T(coNum="CO1", course=course, plo=plolist[1])) #chnage
colist.append(CO_T(coNum="CO2", course=course, plo=plolist[2])) #chnage
colist.append(CO_T(coNum="CO3", course=course, plo=plolist[3])) #chnage
colist.append(CO_T(coNum="CO4", course=course, plo=plolist[5])) #chnage

colist[0].save()
colist[1].save()
colist[2].save()
colist[3].save()

faculties = []
faculties.append(Instructor_T.objects.get(pk=4101)) # change: faculty
faculties.append(Instructor_T.objects.get(pk=4102)) # change: faculty
faculties.append(Instructor_T.objects.get(pk=4103)) # change: faculty

dept = Department_T.objects.get(pk="CSE") # change
program = Program_T.objects.get(pk=1) #change


def updatedatabase(d, sem, y):

    CO_Course_T(coID="CO1", courseID=course, co_semester=sem, co_year=y)
    CO_Course_T(coID="CO2", courseID=course, co_semester=sem, co_year=y)
    CO_Course_T(coID="CO3", courseID=course, co_semester=sem, co_year=y)
    CO_Course_T(coID="CO4", courseID=course, co_semester=sem, co_year=y)

    df = pd.read_excel("CSE303.xlsx", sheet_name="Marks") # change

    data = df.values.tolist()

    comid = data[0][5:11]
    cofin = data[0][13:17]
    colab = data[0][19]

    midmarks = data[2][5:11]
    finmarks = data[2][13:17]
    labmark = data[2][19]

    data = data[3:][:]

    for i in data:
        i[1] = int(i[1]) + d
        i[3] = int(int(i[3]))

    currentstudents = list(Student_T.objects.all())
    newstudents = []

    sections = []

    for i in data:
        if i[1] not in currentstudents:
            newstudents.append(i[1])

        if i[3] not in sections:
            sections.append(i[3])

    sections.sort()
    # Students

    for i in newstudents:
        student = Student_T(sAccountID=i, departmentID=dept, programID=program)
        student.save()

    # Sections

    sectionlist = []

    for i in sections:
        faculty = faculties[i - 1]
        section = Section_T(sectionNum=i, courseID=course, instructorID=faculty, sec_semester=sem, year=y)
        section.save()
        sectionlist.append(section)

    # Registration
    reglist = []

    for i in data:
        st = Student_T.objects.get(pk=i[1])
        reg = Registration_T(sAccountID=st, sectionID=sectionlist[i[3] - 1], reg_semester=sem, year=y)
        reg.save()
        reglist.append(reg)

    # Assessment
    assessmentlist = []
    for i in range(1, len(sectionlist) + 1):
        for j in range(1, len(comid) + 1):

            coid = []

            for k in colist:
                if k.coNum == comid[j - 1]:
                    coid = k
                    break

            assessment = Assessment_T(assessmentName="Mid", questionNo=j, totalMarks=midmarks[j - 1], coID=coid,
                                      sectionID=sectionlist[i - 1], weight=30, iAccountID=sectionlist[i - 1].instructorID)
            assessment.save()
            assessmentlist.append(assessment)

        for j in range(1, len(cofin) + 1):

            coid = []

            for k in colist:
                if k.coNum == cofin[j - 1]:
                    coid = k
                    break
            assessment = Assessment_T(assessmentName="Final", questionNo=j, totalMarks=finmarks[j - 1], coID=coid,
                                      sectionID=sectionlist[i - 1], weight=40, iAccountID=sectionlist[i - 1].instructorID)

            assessment.save()
            assessmentlist.append(assessment)

        coid = []

        for k in colist:
            if k.coNum == colab:
                coid = k
                break

        assessment = Assessment_T(assessmentName="Lab", questionNo=1, totalMarks=labmark, coID=coid,
                                  section=sectionlist[i - 1], weight=30, iAccountID=sectionlist[i - 1].instructorID)
        assessment.save()
        assessmentlist.append(assessment)

    # Evaluation

    evlist = []

    for i in range(0, len(data)):
        marks = data[i][5:11]
        marks.extend(data[i][13:17])
        marks.append(data[i][19])

        num = 11 * (data[i][3] - 1)

        for j in range(0, len(marks)):
            tmark = assessmentlist[num+j].totalMarks
            omark = random.randint(0,int(tmark))
            ev = Evaluation_T(obtainedMarks=omark, assessmentID=assessmentlist[num+j], regID=reglist[i], iAccountID=assessmentlist[num+j].instructorID)
            ev.save()
            evlist.append(ev)


updatedatabase(0, "Spring", 2020)
updatedatabase(100, "Summer", 2020)
updatedatabase(200, "Autumn", 2020)
