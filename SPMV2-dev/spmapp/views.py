     
import numpy as np
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .queries import *
from spmapp.models import *

# Create your views here.

# list

schoollist = School_T.objects.all()
deptlist = Department_T.objects.all()
programlist = Program_T.objects.all()
courselist = Course_T.objects.all()
sectionlist = Section_T.objects.all()
instructors = Instructor_T.objects.all()

semlist = getAllSemesters()
semesters = []
for s in semlist:
    semesters.append(s[0])


def loginview(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def logoutview(request):
    logout(request)
    return redirect('loginpage')


def userprofile(request):
    return render(request, 'page-user.html', {})


@login_required(login_url="/login/")
def homeview(request):
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

        if group == 'Student':
            return shome(request)
        if group == 'Instructor':
            return fhome(request)
        if group == 'Higher Authority':
            return hahome(request)
        else:
            return redirect('/')


@login_required(login_url="/login/")
def shome(request):
    name = request.user.get_full_name()
    usertype = request.user.groups.all()[0].name

    studentid = 1823001
    st = Student_T.objects.get(pk=1416455)
    dept = st.departmentID

    row = getStudentWisePLO(studentid)
    chart1 = 'PLO Achievement'
    plolabel1 = []
    plodata1 = []

    for i in row:
        plolabel1.append(i[0])
        plodata1.append(i[1])

    row = getDeptWisePLO(dept)
    chart2 = 'PLO Achievement with Department Average'
    plolabel2 = []
    plodata2 = []

    for i in row:
        plolabel2.append(i[0])
        plodata2.append(i[1])

    chart3 = "Student Wise Gpa"
    gpalabel1 = []
    gpadata1 = []

    semlist = getAllSemesters()
    semesters = []
    for s in semlist:
        semesters.append(s[0])

    for s in semesters:
        print(s)
        gpalabel1.append(s)
        gpadata1.append(getStudentWiseGPA(studentid, s))

    chart4 = "Department Wise Gpa"
    gpalabel2 = []
    gpadata2 = []

    for s in semesters:
        gpalabel2.append(s)
        gpadata2.append(getDeptWiseGPA(dept, s))

    return render(request, 'student/studenthome.html', {
        'name': name,
        'usertype': usertype,

        'chart1': chart1,
        'plolabel1': plolabel1,
        'plodata1': plodata1,

        'chart2': chart2,
        'plolabel2': plolabel2,
        'plodata2': plodata2,

        'chart3': chart3,
        'gpalabel1': gpalabel1,
        'gpadata1': gpadata1,

        'chart4': chart4,
        'gpalabel2': gpalabel2,
        'gpadata2': gpadata2,

    })


def cowiseplo(request):
    name = request.user.get_full_name()
    usertype = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.departmentID

    (plo, co, table) = getCOWiseStudentPLO(studentid, 'chart')

    return render(request, 'student/cowise.html', {
        'name': name,
        'usertype': usertype,
        'plo': plo,
        'co': co,
        'table': table

    })


def coursewiseplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.departmentID

    (plo, courses, table) = getCourseWiseStudentPLO(studentid, 'chart')

    return render(request, 'student/coursewise.html', {
        'name': name,
        'usertype': type,
        'plo': plo,
        'courses': courses,
        'table': table,

    })


def plotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.departmentID

    (plo, courses, table) = getCourseWiseStudentPLO(studentid, 'report')
    range = len(courses)
    print(range)

    return render(request, 'student/plotable.html', {
        'name': name,
        'usertype': type,
        'plo': plo,
        'courses': courses,
        'table': table,
        'range': range,

    })


@login_required(login_url="/login/")
def fhome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    deptT = Instructor_T.objects.get(pk=int(request.user.username))

    dept = deptT.departmentID

    row = getDeptWisePLO(dept)
    chart2 = 'PLO Achievement with Department Average'
    plolabel = []
    plodata = []

    for i in row:
        plolabel.append(i[0])
        plodata.append(i[1])

    gpalabel = []
    gpadata = []

    for s in semesters:
        gpadata.append(getDeptWiseGPA(dept, s))
        gpalabel.append(s)

    return render(request, 'Instructorhome.html', {
        'name': name,
        'usertype': type,

        'plolabel': plolabel,
        'plodata': plodata,
        'gpalabel': gpalabel,
        'gpadata': gpadata,

    })


def dataentry(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courselist = Course_T.objects.all()

    courses = []
    for c in courselist:
        courses.append(c.courseID)

    semesters = ["Spring", "Summer", "Autumn"]

    sections = [1, 2, 3]
    year = [2019, 2020]

    return render(request, 'dataentry.html', {
        'name': name,
        'usertype': type,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'year': year,
    })


def courseinfoentry(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courselist = Course_T.objects.all()
    courses = []
    for c in courselist:
        courses.append(c.courseID)

    semesters = ["Spring", "Summer", "Autumn"]

    sections = [1, 2, 3]
    year = [2019, 2020]

    return render(request, 'courseinfoentry.html', {
        'name': name,
        'usertype': type,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'year': year,
    })


def plocomapping(request):
    usertype = request.user.groups.all()[0].name
    if request.method == 'POST':
        courseID = request.POST.get('course')
        coMaps = request.POST.getlist('coMaps')

        course = Course_T.objects.get(pk=courseID)

        plist = PLO_T.objects.all()

        plolist = []

        for p in plist:
            if p.programID == course.programID:
                plolist.append(p)

        for i in range(len(coMaps)):
            k = -1

            for p in range(len(plolist)):
                if plolist[p].ploNum == coMaps[i]:
                    k = p
            co = CO_T(coNum="CO" + str(i + 1), course=course, plo=plolist[k])
            co.save()

        return redirect('plocomapping')
    else:
        return render(request, 'plocomapping.html', {
            'usertype': usertype,
            'clist': courselist,

        })


def assessmentdataentry(request):
    usertype = request.user.groups.all()[0].name

    sections = [1, 2, 3]

    if request.method == 'POST':
        instructorID = request.user.username
        courseID = request.POST.get('course')
        sectionNo = request.POST.get('section')
        semester = request.POST.get('semester')
        totalMarks = request.POST.getlist('totalMarks')
        weightage = request.POST.getlist('weightAge')
        assessmentName = request.POST.getlist('assessmentName')
        questions = request.POST.getlist('questions')
        cos = request.POST.getlist('co')

        sectionID = None
        try:
            sections = Section_T.objects.raw('''
                SELECT *
                FROM spmapp_section_t
                WHERE courseID = '{}' 
                    AND sectionNum = {};
                    AND semester = '{}'
                
            '''.format(courseID, sectionNo, semester))
            sectionID = sections[0].sectionID
        except:
            sectionID = None

        if sectionID is None:
            section = Section_T(sectionNum=sectionNo, courseID=courseID,
                                instructorID=instructorID, semester=semester)
            section.save()
            sectionID = section.sectionID

        for j in range(1, len(totalMarks) + 1):
            conum = cos[j-1]
            coID = CO_T.objects.raw('''
                SELECT *
                FROM spmapp_co_t
                WHERE courseID = '{}' 
                    AND coNum = '{}'
            '''.format(courseID, conum))

            assessment = Assessment_T(sectionID=sectionID, coID=coID[0].coID, totalMarks=totalMarks[j - 1],
                                      assessmentName=assessmentName[j-1], questionNum=questions[j-1], weight=weightage[j-1])
            assessment.save()

        return redirect('assessmentdataentry')

    else:
        return render(request, 'assessmentdataentry.html', {
            'usertype': usertype,
            'clist': courselist,
            'semesters': semesters,
            'sections': sections,

        })


def evaluationdataentry(request):
    usertype = request.user.groups.all()[0].name
    section = [1, 2, 3]

    if request.method == 'POST':
        courseID = request.POST.get('course')
        section = request.POST.get('section')
        semester = request.POST.get('semester')

        print(courseID)
        print(section)
        print(semester)

        accountID = request.POST.getlist('student')
        obtainedMarks = []
        questions = []
        for i in range(len(accountID)):
            obtainedMarks.append(request.POST.getlist(f'obtainedMarks{i}'))
            questions.append(request.POST.getlist(f'questions'))

        sectionID = None
        try:
            sectionID = Section_T.objects.raw('''
                SELECT *
                FROM spmapp_section_t
                WHERE courseID = '{}' 
                    AND sectionNum = '{}'
                    AND semester ='{}';
            '''.format(courseID, section, semester))
            sectionID = sectionID[0].sectionID
            print(sectionID)
        except:
            sectionID = None
        assessment_list = []
        coLength = 0
        try:
            col = CO_T.objects.raw('''
                SELECT count(*)
                FROM spmapp_co_t
                WHERE courseID ='{}'
                '''.format(courseID))
            coLength = col[0][0]+1
        except:
            coLength = 0
        for j in range(1, len(questions[0])+1):
            assessmentID = None
            try:
                assessmentID = Assessment_T.objects.raw('''
                    SELECT *
                    FROM spmapp_assessment_t
                    WHERE sectionID = '{}'
                        AND coID IN (
                        SELECT coID
                        FROM spmapp_co_t
                        WHERE courseID = '{}' 
                            AND questionNum = '{}'
                    )
                '''.format(sectionID, courseID, j))
                assessment_list.append(assessmentID[0].assessmentID)
            except:
                assessmentID = None
                assessment_list.append(assessmentID)

        for i in range(len(accountID)):

            regID = None
            try:
                regID = Registration_T.objects.raw('''
                    SELECT *
                    FROM spmapp_registration_t
                    WHERE accountID = '{}'
                        AND sectionID = '{}'
                '''.format(accountID[i], sectionID))
                regID = regID[0].registrationID
            except:
                regID = None

            if regID is None:
                print(sectionID)
                print(accountID[i])
                registration = Registration_T(
                    accountID=accountID[i], sectionID=sectionID, semester=semester)
                registration.save()
                regID = registration.registrationID

            for j in range(len(assessment_list)):
                evaluation = Evaluation_T(regID=regID, assessmentID=assessment_list[j],
                                          obtainedMarks=obtainedMarks[i][j])
                evaluation.save()
        return redirect('evaluationdataentry')
    else:
        return render(request, 'evaluationdataentry.html', {
            'usertype': usertype,
            'clist': courselist,
            'semesters': semesters,
            'sections': section,

        })


# higher authority

@login_required(login_url="/login/")
def hahome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    totalStudents = len(studentlist)

    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    schools = []
    depts = []
    programs = []
    programnames = []

    schoollist = School_T.objects.all()
    deptlist = Department_T.objects.all()
    programlist = Program_T.objects.all()

    for s in schoollist:
        schools.append(s.schoolID)

    for d in deptlist:
        depts.append(d.departmentID)

    for p in programlist:
        programs.append(p.programID)
        programnames.append(p.programName)

    gpalabel = []

    for s in semesters:
        gpalabel.append(s)

    # schoolwise gpa
    sgpatable = []

    for school in schools:
        gpa = []

        for s in semesters:
            gpa.append(getSchoolWiseGPA(school, s))

        sgpatable.append(gpa)

    # deptwise gpa
    dgpatable = []

    for dept in depts:
        gpa = []

        for s in semesters:
            gpa.append(getDeptWiseGPA(dept, s))

        dgpatable.append(gpa)

    # programwise gpa
    pgpatable = []

    for p in programs:
        gpa = []
        for s in semesters:
            gpa.append(getProgramWiseGPA(p, s))
        pgpatable.append(gpa)

    return render(request, 'hahome.html', {
        'name': name,
        'usertype': type,

        'gpalabel': gpalabel,

        'schools': schools,
        'sgpatable': sgpatable,

        'depts': depts,
        'dgpatable': dgpatable,

        'programs': programnames,
        'pgpatable': pgpatable,

        'totalstudents': totalStudents,
        'segment': 'fadash'

    })


# Enrollment
def enrollment(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        sems = []
        for i in range(b, e + 1):
            sems.append(semesters[i])

        schools = []
        depts = []
        programs = []
        programnames = []

        for s in schoollist:
            schools.append(s.schoolID)

        for d in deptlist:
            depts.append(d.departmentID)

        for p in programlist:
            programs.append(p.programID)
            programnames.append(p.programName)

        # schoolwise students
        snum = []
        for school in schools:
            snum.append(getSchoolWiseEnrolledStudents(school, sems))

        # deptwise students
        dnum = []

        for dept in depts:
            dnum.append(getDeptWiseEnrolledStudents(dept, sems))

        # programwise students
        pnum = []

        for p in programs:
            pnum.append(getProgramWiseEnrolledStudents(p, sems))

        return render(request, 'enrollment.html', {
            'name': name,
            'usertype': type,

            'school': schools,
            'snum': snum,
            'depts': depts,
            'dnum': dnum,
            'program': programnames,
            'pnum': pnum,
            'semesters': semesters,
            'selected1': b,
            'selected2': e,
            'search': 0,
            'segment': 'enrollment',
        })
    else:
        return render(request, 'enrollment.html', {
            'name': name,
            'usertype': type,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
            'segment': 'enrollment',
        })


def studentplotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        studentid = request.POST.get('student-id')
        (plo, courses, table) = getCourseWiseStudentPLO(studentid, 'report')
        range = len(courses)
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'plo': plo,
            'courses': courses,
            'table': table,
            'range': range,
            'sid': studentid,
            'search': 0,

        })
    else:
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'sid': None,
            'search': 1,
        })


def plostats(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        prog = int(request.POST['program'])

        (plo, achieved, attempted) = getProgramWisePLO(prog)

        return render(request, 'plostats.html', {
            'name': name,
            'usertype': type,
            'programs': programlist,
            'plo': plo,
            'achieved': achieved,
            'attempted': attempted,
            'selectedItem': prog,
            'search': 0,

        })
    else:
        return render(request, 'plostats.html', {
            'name': name,
            'usertype': type,
            'programs': programlist,
            'selectedItem': None,
            'search': 1,
        })


def courseverdict(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []
    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':

        course = request.POST['course']

        (table, total) = getCourseReport(course)

        return render(request, 'courseverdict.html', {
            'name': name,
            'usertype': type,
            'table': table,
            'courses': courses,
            'total': total,
            'search': 0,
            'selectedCourse': course,

        })

    else:
        return render(request, 'courseverdict.html', {
            'name': name,
            'usertype': type,
            'courses': courses,
            'search': 1,
            'selectedCourse': None,
        })


# def dataentry(request):
####   name = request.user.get_full_name()
####    type = request.user.groups.all()[0].name

####    courses = []
# for c in courselist:
# courses.append(c.courseID)

####   semesters = ["Spring", "Summer", "Autumn"]

####   sections = [1, 2, 3]
####    year = [2019, 2020]

# return render(request, 'dataentry2.html', {
# 'name': name,
# 'usertype': type,
# 'courses': courses,
# 'semesters': semesters,
# 'sections': sections,
# 'year': year,
# })

# GPA Analysis
def semesterwisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    schools = []
    depts = []
    programs = []
    programnames = []

    for s in schoollist:
        schools.append(s.schoolID)

    for d in deptlist:
        depts.append(d.departmentID)

    for p in programlist:
        programs.append(p.programID)
        programnames.append(p.programName)

    if request.method == "POST":
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []

        for i in range(b, e + 1):
            labels.append(semesters[i])

        # schoolwise gpa
        sgpatable = []

        for school in schools:

            gpa = []

            for i in range(b, e + 1):
                gpa.append(getSchoolWiseGPA(school, semesters[i]))

            sgpatable.append(gpa)

        # deptwise gpa
        dgpatable = []

        for dept in depts:
            gpa = []

            for i in range(b, e + 1):
                gpa.append(getDeptWiseGPA(dept, semesters[i]))

            dgpatable.append(gpa)

        # programwise gpa
        pgpatable = []

        for p in programs:
            gpa = []
            for i in range(b, e + 1):
                gpa.append(getProgramWiseGPA(p, semesters[i]))

            pgpatable.append(gpa)

        return render(request, 'gpa/semesterwisegpa.html', {
            'name': name,
            'usertype': type,

            'semesters': semesters,
            'selected1': b,
            'selected2': e,

            'schools': schools,
            'sgpatable': sgpatable,
            'labels': labels,

            'depts': depts,
            'dgpatable': dgpatable,

            'programs': programnames,
            'pgpatable': pgpatable,

            'search': 0,
            'segment': 'GPA Analysis'

        })
    else:
        return render(request, 'gpa/semesterwisegpa.html', {
            'name': name,
            'usertype': type,

            'semesters': semesters,

            'selected1': None,
            'selected2': None,
            'search': 1,
            'segment': 'GPA Analysis'

        })


def coursewisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []

    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':
        selectedCourses = request.POST.getlist('courses')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        label = []

        for i in range(b, e + 1):
            label.append(semesters[i])

        gpatable = []

        for c in selectedCourses:
            gpa = []
            for i in range(b, e + 1):
                gpa.append(getCourseWiseGPA(c, semesters[i]))
            gpatable.append(gpa)

        return render(request, 'gpa/coursewisegpa.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,

            'selected1': b,
            'selected2': e,
            'selectedCourses': selectedCourses,

            'gpatable': gpatable,
            'labels': label,

            'search': 0,
            'segment': 'GPA Analysis'

        })

    else:
        return render(request, 'gpa/coursewisegpa.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
            'segment': 'GPA Analysis'
        })


def instructorwisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        selectedIns = request.POST.getlist('instructors')

        fnames = []

        for i in range(0, len(selectedIns)):
            selectedIns[i] = int(selectedIns[i])
            for j in instructors:
                if j.instructorID == selectedIns[i]:
                    fnames.append(j.firstName + " " + j.lastName)

        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        label = []

        for i in range(b, e + 1):
            label.append(semesters[i])

        gpatable = []

        for s in selectedIns:
            gpa = []
            for i in range(b, e + 1):
                gpa.append(getInstructorWiseGPA(s, semesters[i]))
            gpatable.append(gpa)

        return render(request, 'gpa/inswisegpa.html', {
            'name': name,
            'usertype': type,

            'instructors': instructors,
            'fnames': fnames,
            'semesters': semesters,

            'selected1': b,
            'selected2': e,
            'selectedIns': selectedIns,

            'gpatable': gpatable,
            'labels': label,
            'search': 0,
            'segment': 'GPA Analysis'

        })

    else:
        return render(request, 'gpa/inswisegpa.html', {
            'name': name,
            'usertype': type,

            'instructors': instructors,

            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'selectedIns': None,
            'search': 1,
            'segment': 'GPA Analysis'
        })


def leaderwisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    headlist = Head_T.objects.all()
    deanlist = Dean_T.objects.all()
    vclist = VC_T.objects.all()

    headlabel = []
    headgpa = []

    deanlabel = []
    deangpa = []

    vclabel = []
    vcgpa = []

    for h in headlist:
        headlabel.append(h.firstName + " " + h.lastName)
        headgpa.append(getHeadWiseGPA(h))

    for d in deanlist:
        deanlabel.append(d.firstName + " " + d.lastName)
        deangpa.append(getDeanWiseGPA(d))

    for v in vclist:
        vclabel.append(v.firstName + " " + v.lastName)
        vcgpa.append(getVCWiseGPA(v))

    return render(request, 'gpa/leaderwisegpa.html', {
        'name': name,
        'usertype': type,

        'headlabel': headlabel,
        'headgpa': headgpa,

        'deanlabel': deanlabel,
        'deangpa': deangpa,

        'vclabel': vclabel,
        'vcgpa': vcgpa,
        'segment': 'GPA Analysis'
    })


def instructorwisegpaforcourse(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []

    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':
        selectedCourse = request.POST['course']
        b = int(request.POST['sem1'])
        end = int(request.POST['sem2'])

        label = []

        for i in range(b, end + 1):
            label.append(semesters[i])

        gpatable = []
        ins = []
        insnames = []
        temp = []

        for i in range(b, end + 1):
            temp.append(getInstructorWiseGPAForCourse(
                selectedCourse, semesters[i]))
        print(temp)

        for t in temp:
            for e in t:
                if e[0] not in ins:
                    ins.append(e[0])

        for i in ins:
            for f in instructors:
                if f.instructorID == i:
                    insnames.append(f.firstName + " " + f.lastName)
            gpa = []
            for t in temp:
                for e in t:
                    if e[0] == i:
                        gpa.append(e[1])
            gpatable.append(gpa)

        return render(request, 'gpa/instructorwisegpaforcourse.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,

            'selected1': b,
            'selected2': end,
            'selectedCourse': selectedCourse,

            'gpatable': gpatable,
            'labels': label,
            'ins': ins,
            'insnames': insnames,

            'search': 0,
            'segment': 'GPA Analysis'

        })

    else:
        return render(request, 'gpa/instructorwisegpaforcourse.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
            'segment': 'GPA Analysis'
        })


# PLO Analysis
def studentplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        student = int(request.POST['student'])

        st = Student_T.objects.get(pk=student)
        dept = st.department
        prog = st.program
        school = dept.school

        row = getStudentWisePLO(student)
        plo1 = []
        table1 = []

        for i in row:
            plo1.append(i[0])
            table1.append(i[1])

        row = getDeptWisePLO(dept.departmentID)

        table2 = []
        plo2 = []
        for i in row:
            plo2.append(i[0])
            table2.append(i[1])

        (plo3, co, table3) = getCOWiseStudentPLO(student, 'chart')
        (plo4, courses, table4) = getCourseWiseStudentPLO(student, 'chart')

        pplo = []
        row = getProgramWisePLO(prog.programID)
        for r in row:
            pplo.append(r[1])

        splo = []

        row = getSchoolWisePLO(school.schoolID)
        for r in row:
            splo.append(r[1])

        response = {
            'name': name,
            'usertype': type,

            'plo1': plo1,
            'table1': table1,

            'plo2': plo2,
            'table2': table2,

            'co': co,
            'plo3': plo3,
            'table3': table3,

            'courses': courses,
            'plo4': plo4,
            'table4': table4,
            'stid': student,

            'pplo': pplo,
            'splo': splo,

            'search': 0,
            'segment': 'PLO Analysis'
        }

        return render(request, 'ploanalysis/studentplo.html', response)
    else:
        return render(request, 'ploanalysis/studentplo.html', {
            'name': name,
            'usertype': type,
            'stid': None,
            'search': 1,
            'segment': 'PLO Analysis'
        })


def programplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        program = int(request.POST['program'])

        print(program)

        row = getProgramWisePLO(program)

        print(row)
        plo1 = []
        table1 = []

        for i in row:
            plo1.append(i[0])
            table1.append(i[1])

        # (plo2, co, table2) = getCOWisePLO(studentid, 'chart')
        # (plo3, courses, table3) = getCourseWisePLO(studentid, 'chart')

        response = {
            'name': name,
            'usertype': type,

            'plo1': plo1,
            'table1': table1,

            # 'plo2': plo2,
            # 'table2': table2,
            # 'co': co,

            # 'plo3': plo3,
            # 'table3': table3,
            # 'courses': courses,
            'pid': program,
            'plist': programlist,

            'search': 0,
            'segment': 'PLO Analysis'
        }

        return render(request, 'ploanalysis/programplo.html', response)
    else:
        return render(request, 'ploanalysis/programplo.html', {
            'name': name,
            'usertype': type,
            'pid': None,
            'search': 1,
            'plist': programlist,
            'segment': 'PLO Analysis'
        })


def deptplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        dept = request.POST['dept']

        row = getDeptWisePLO(dept)
        table1 = []
        plo1 = ['PLO1', 'PLO2', 'PLO3', 'PLO4', 'PLO5', 'PLO6',
                'PLO7', 'PLO8', 'PLO9', 'PLO10', 'PLO11', 'PLO12']

        for p in plo1:
            for r in row:
                if r[0] == p:
                    table1.append(r[1])

        # (plo2, co, table2) = getCOWisePLO(studentid, 'chart')
        # (plo3, courses, table3) = getCourseWisePLO(studentid, 'chart')

        response = {
            'name': name,
            'usertype': type,

            'plo1': plo1,
            'table1': table1,

            # 'plo2': plo2,
            # 'table2': table2,
            # 'co': co,

            # 'plo3': plo3,
            # 'table3': table3,
            # 'courses': courses,
            'did': dept,

            'dlist': deptlist,

            'search': 0,
            'segment': 'PLO Analysis'
        }

        return render(request, 'ploanalysis/deptplo.html', response)
    else:
        return render(request, 'ploanalysis/deptplo.html', {
            'name': name,
            'usertype': type,
            'did': None,
            'dlist': deptlist,
            'search': 1,
            'segment': 'PLO Analysis'
        })


def schoolplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        school = request.POST['school']

        row = getSchoolWisePLO(school)

        table1 = []
        plo1 = ['PLO1', 'PLO2', 'PLO3', 'PLO4', 'PLO5', 'PLO6',
                'PLO7', 'PLO8', 'PLO9', 'PLO10', 'PLO11', 'PLO12']

        for p in plo1:
            for r in row:
                if r[0] == p:
                    table1.append(r[1])

        # (plo2, co, table2) = getCOWisePLO(studentid, 'chart')
        # (plo3, courses, table3) = getCourseWisePLO(studentid, 'chart')

        response = {
            'name': name,
            'usertype': type,

            'plo1': plo1,
            'table1': table1,

            # 'plo2': plo2,
            # 'table2': table2,
            # 'co': co,

            # 'plo3': plo3,
            # 'table3': table3,
            # 'courses': courses,
            'sid': school,

            'slist': schoollist,

            'search': 0,
            'segment': 'PLO Analysis'
        }

        return render(request, 'ploanalysis/schoolplo.html', response)
    else:
        return render(request, 'ploanalysis/schoolplo.html', {
            'name': name,
            'usertype': type,
            'sid': None,
            'slist': schoollist,
            'search': 1,
            'segment': 'PLO Analysis'
        })


def studentplotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        studentid = request.POST.get('student')
        (plo, courses, table) = getCourseWiseStudentPLO(studentid, 'report')
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'plo': plo,
            'table': table,
            'sid': studentid,
            'search': 0,
            'segment': 'plotable'

        })
    else:
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'sid': None,
            'search': 1,
            'segment': 'plotable'
        })


# PLO Statistics
def programwiseplostats(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        prog = int(request.POST['program'])

        (plo, achieved, attempted) = getProgramWisePLOStats(prog)

        return render(request, 'plostats/programwiseplostats.html', {
            'name': name,
            'usertype': type,
            'programs': programlist,
            'plo': plo,
            'achieved': achieved,
            'attempted': attempted,
            'selectedItem': prog,
            'search': 0,
            'segment': 'plostats'

        })
    else:
        return render(request, 'plostats/programwiseplostats.html', {
            'name': name,
            'usertype': type,
            'programs': programlist,
            'selectedItem': None,
            'search': 1,
            'segment': 'plostats'
        })


def deptwiseplostats(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        dept = request.POST['dept']

        (plo, achieved, attempted) = getDeptWisePLOStats(dept)

        return render(request, 'plostats/deptwiseplostats.html', {
            'name': name,
            'usertype': type,
            'dlist': deptlist,
            'plo': plo,
            'achieved': achieved,
            'attempted': attempted,
            'selectedItem': dept,
            'search': 0,
            'segment': 'plostats'

        })
    else:
        return render(request, 'plostats/deptwiseplostats.html', {
            'name': name,
            'usertype': type,
            'dlist': deptlist,
            'selectedItem': None,
            'search': 1,
            'segment': 'plostats'
        })


def schoolwiseplostats(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        school = request.POST['school']

        (plo, achieved, attempted) = getSchoolWisePLOStats(school)

        return render(request, 'plostats/schoolwiseplostats.html', {
            'name': name,
            'usertype': type,
            'slist': schoollist,
            'plo': plo,
            'achieved': achieved,
            'attempted': attempted,
            'selectedItem': school,
            'search': 0,
            'segment': 'plostats'

        })
    else:
        return render(request, 'plostats/schoolwiseplostats.html', {
            'name': name,
            'usertype': type,
            'slist': schoollist,
            'selectedItem': None,
            'search': 1,
            'segment': 'plostats'
        })


# PLO Comparison
def studentplocomp(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        student = int(request.POST['student'])
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []
        for i in range(b, e + 1):
            labels.append(semesters[i])

        expected = []
        actual = []

        for l in labels:
            temp = getStudentWisePLOComp(student, l)

            expected.append(temp[0])
            actual.append(temp[1])

        return render(request, 'plocomp/studentplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'stid': student,
            'search': 0,

            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'plocomp/studentplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'segment': 'PLO Comp'

        })


def courseplocomp(request):
    usertype = request.user.groups.all()[0].name

    courses = []

    for i in courselist:
        courses.append(i.courseID)

    if request.method == 'POST':
        course = request.POST['course']
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []
        for i in range(b, e + 1):
            labels.append(semesters[i])

        expected = []
        actual = []
        plo = []

        for l in labels:
            ptemp, n, atemp = getCourseWisePLOComp(course, l)
            expected.append(n)
            actual.append(atemp)

            for p in ptemp:
                if p not in plo:
                    plo.append(p)

        actual = np.transpose(actual)
        actual = actual.tolist()

        return render(request, 'plocomp/courseplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'selectedCourse': course,
            'courses': courses,
            'search': 0,

            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'plocomp/courseplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'courses': courses,
            'segment': 'PLO Comp'

        })


def programplocomp(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        program = request.POST.get('program')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []
        for i in range(b, e + 1):
            labels.append(semesters[i])

        expected = []
        actual = []
        plo = []

        for l in labels:
            plo, etemp, atemp = getProgramWisePLOComp(program, l)
            expected.append(etemp)
            actual.append(atemp)

        actual = np.transpose(actual)
        actual = actual.tolist()

        expected = np.transpose(expected)
        expected = expected.tolist()

        return render(request, 'plocomp/programplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'selectedProgram': program,
            'plist': programlist,
            'search': 0,

            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'plocomp/programplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'plist': programlist,
            'segment': 'PLO Comp'

        })


def deptplocomp(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        dept = request.POST.get('dept')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []
        for i in range(b, e + 1):
            labels.append(semesters[i])

        expected = []
        actual = []
        plo = []

        for l in labels:
            plo, etemp, atemp = getDeptWisePLOComp(dept, l)
            expected.append(etemp)
            actual.append(atemp)

        actual = np.transpose(actual)
        actual = actual.tolist()

        expected = np.transpose(expected)
        expected = expected.tolist()

        return render(request, 'plocomp/deptplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'selectedDept': dept,
            'dlist': deptlist,
            'search': 0,

            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'plocomp/deptplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'dlist': deptlist,
            'segment': 'PLO Comp'

        })


def schoolplocomp(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        school = request.POST.get('school')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []
        for i in range(b, e + 1):
            labels.append(semesters[i])

        expected = []
        actual = []
        plo = []

        for l in labels:
            plo, etemp, atemp = getSchoolWisePLOComp(school, l)
            expected.append(etemp)
            actual.append(atemp)

        actual = np.transpose(actual)
        actual = actual.tolist()

        expected = np.transpose(expected)
        expected = expected.tolist()

        return render(request, 'plocomp/schoolplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'selectedSchool': school,
            'slist': schoollist,
            'search': 0,

            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'plocomp/schoolplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'slist': schoollist,
            'segment': 'PLO Comp'

        })


# REPORT
def coursereport(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []
    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':

        course = request.POST['course']

        (table, total) = getCourseReport(course)

        return render(request, 'report/coursereport.html', {
            'name': name,
            'usertype': type,
            'table': table,
            'courses': courses,
            'total': total,
            'search': 0,
            'selectedCourse': course,
            'segment': 'PLO-CO'

        })

    else:
        return render(request, 'report/coursereport.html', {
            'name': name,
            'usertype': type,
            'courses': courses,
            'search': 1,
            'selectedCourse': None,
            'segment': 'PLO-CO'

        })


def programreport(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':

        program = int(request.POST.get('prog'))

        table = getProgramReport(program)

        return render(request, 'report/programreport.html', {
            'name': name,
            'usertype': type,
            'table': table,
            'plist': programlist,
            'search': 0,
            'selectedProgram': program,
            'segment': 'PLO-CO'

        })

    else:
        return render(request, 'report/programreport.html', {
            'name': name,
            'usertype': type,
            'plist': programlist,
            'search': 1,
            'selectedProgram': None,
            'segment': 'PLO-CO'

        })


def deptreport(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':

        dept = request.POST.get('dept')

        table = getDeptReport(dept)

        return render(request, 'report/deptreport.html', {
            'name': name,
            'usertype': type,
            'table': table,
            'dlist': deptlist,
            'search': 0,
            'selectedDept': dept,
            'segment': 'PLO-CO'

        })

    else:
        return render(request, 'report/deptreport.html', {
            'name': name,
            'usertype': type,
            'dlist': deptlist,
            'search': 1,
            'selectedDept': None,
            'segment': 'PLO-CO'

        })


def schoolreport(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':

        school = request.POST.get('school')

        table = getSchoolReport(school)

        return render(request, 'report/schoolreport.html', {
            'name': name,
            'usertype': type,
            'table': table,
            'slist': schoollist,
            'search': 0,
            'selectedSchool': school,
            'segment': 'PLO-CO'

        })

    else:
        return render(request, 'report/schoolreport.html', {
            'name': name,
            'usertype': type,
            'slist': schoollist,
            'search': 1,
            'selectedSchool': None,
            'segment': 'PLO-CO'

        })
