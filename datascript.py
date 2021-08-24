import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

# Add University
university1 = University_T(universityID='IUB01', universityName='Independent University, Bangladesh', universityAddress='Bashundhara, Dhaka')
university1.save()

university2 = University_T(universityID='BRA02', universityName='Brac University, Bangladesh', universityAdress='Rampura, Dhaka')
university2.save()

"""university3 = University_T(universityID='NSU03', universityName='North South University, Bangladesh')
university3.save()"""

# Add School
school1 = School_T(schoolID='SETS', schoolName='School of Engineering, Technology & Sciences', universityID= 'IUB01')
school1.save()

school2 = School_T(schoolID='SBE', schoolName='School of Business and Entrepreneurship', universityID= 'IUB01')
school2.save()

school3 = School_T(schoolID='SLASS', schoolName='School of Liberal Arts & Social Sciences', universityID= 'IUB01')
school3.save()

school4 = School_T(schoolID='SETS', schoolName='School of Engineering, Technology & Sciences', universityID= 'BRA02')
school4.save()

school5 = School_T(schoolID='SBE', schoolName='School of Business and Entrepreneurship', universityID= 'BRA02')
school5.save()

school6 = School_T(schoolID='SLASS', schoolName='School of Liberal Arts & Social Sciences', universityID= 'BRA02')
school6.save()

#Add Department

d1 = Department_T(departmentID='CSE',departmentName='Computer Science & Engineering',schoolID='SETS')
d1.save()

d2 = Department_T(departmentID='EEE',departmentName='Electrical and Electronics Engineering',schoolID='SETS')
d2.save()

d3 = Department_T(departmentID='ACN',departmentName='Accounting',schoolID='SBE')
d3.save()

d4 = Department_T(departmentID='MIS',departmentName='Management Information Systems',schoolID='SBE')
d4.save()

d5 = Department_T(departmentID='ENG',departmentName='English',schoolID='SLASS')
d5.save()

d6 = Department_T(departmentID='GSG',departmentName='Global Studies & Governance',schoolID='SLASS')
d6.save()

#Add programs

p1 = Program_T(programName='B.Sc. in CSE', departmentID='CSE')
p1.save()

p2 = Program_T(programName='BBA in Accounting', departmentID='ACN')
p2.save()

p3 = Program_T(programName='B.Sc. in EEE', departmentID='EEE')
p3.save()

p4 = Program_T(programName='BBA in MIS', departmentID='MIS')
p4.save()

p5 = Program_T(programName='BA in ENG', departmentID='ENG')
p5.save()

p6 = Program_T(programName='BSS in GSG', departmentID='GSG')
p6.save()



# Add PLO for all programs
programList = list(Program_T.objects.all())
details = ["Knowledge", "Requirement Analysis", "Requirement Analysis", "Design", "Problem Solving", "Implementation",
           "Experiment and Analysis", "Community Engagement and Engineering", "Teamwork", "Communication",
           "Self-Motivated", "Ethics", "Process Management"]

for p in programList:
    for i in range(1, 13):
        plonum = "PLO" + str(i)
        plo = PLO_T(ploNum=plonum, program=p, details=details[i - 1])
        plo.save()

# Add Instructor Information

"""FOR IUB"""

nlist = ["Mahady Hasan", "Sadita Ahmed", "Md. Abu Sayed", "Romasa Qasim", "Mohammad Motiur Rahman", "Asif Bin Khaled", "Ferdows Zahid", "Bijoy R. Arif", "Raihan Bin Rafique",
          "Faisal M. Uddin", "Subrata Kumar Dey", "Mohammad Noor Nabi", "Farruk Ahmed", "Sabrina Alam", "Sanzar Adnan Alam"]

id = 4101

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id="CSE")
    f.save()
    id = id + 1
    i = i + 1

nlist = ["Naheem Mahtab", "Md. Saifuddin ", "Susmita", "Shahriar", "Kamrul", "Nabila", "Abul", "Nadim", "Farzana"]

id = 4201

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="ACN")
    f.save()
    id = id + 1
    i = i + 1



nlist = ["Shahriar", "Feroz", "Kafiul", "Abdur", "Mustafa", "Sajib", "Naziba", "Saila", "Khosru"]


id = 4301

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="EEE")
    f.save()
    id = id + 1
    i = i + 1

nlist = ["Rezwanul", "Arifur Rahman", "Aminul", "Ikramul", "Bushra", "Zakia Binte"]

id = 4401

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="MIS")
    f.save()
    id = id + 1
    i = i + 1

nlist = ["Shafiul", "Sara", "Vikarun", "Adilur", "Mazaharul","Mithila"]

id = 4501

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="ENG")
    f.save()
    id = id + 1
    i = i + 1



nlist = ["Marufa", "Imtiaz", "Ahmed", "Amjad", "Mohammad", "Shahidul"]

id = 4601

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="GSG")
    f.save()
    id = id + 1
    i = i + 1


"""FOR BRAC"""

nlist = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
        
id = 5101

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id="CSE")
    f.save()
    id = id + 1
    i = i + 1

nlist = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]

id = 5201

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="ACN")
    f.save()
    id = id + 1
    i = i + 1



nlist = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]


id = 5301

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="EEE")
    f.save()
    id = id + 1
    i = i + 1

nlist = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]

id = 7701

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="MIS")
    f.save()
    id = id + 1
    i = i + 1

nlist = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"]

id = 8801

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="ENG")
    f.save()
    id = id + 1
    i = i + 1



nlist = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]

id = 4601

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", departmentID="GSG")
    f.save()
    id = id + 1
    i = i + 1
