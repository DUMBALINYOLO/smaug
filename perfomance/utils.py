from results.models import *
from django.db import transaction
from subjects.models import Subject
from students.models import Student
from institutions.models import StudentClass
import operator
from collections import OrderedDict
from config.utils import Limit
from django.views.decorators.cache import cache_page


def pin_generator(length=8):
    
    '''
    This is to generate alphanumeric ids. 
    the addition of non-alphameric chars increases the uniqueness of the pin 
    e.g Qw21#d seem more unique than 1242
    
    It can also serve as a secrete key generator of any length.
    '''
    
    import random
    
    num = '0123456789'
    chars = '@#$&'
    upper_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_alpha = upper_alpha.lower()
    gen_base = [num,chars,upper_alpha,lower_alpha]
    alphanum = ''.join(gen_base)
    
    pin = ''
    
    # generate some random characters from the alphanum string
    for x in range(length):
        pin += alphanum[random.randint(1,len(alphanum)-1)]
    
    return pin 


def update_results(school):
    for result in Result.objects.filter(school=school):
        result.save()


@transaction.atomic
def import_test_from_csv(csv_file, teacher, is_admin=False):
    """
    Import result CSV data.

    We'll process all rows first and create Result model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.
    
    """
    school = teacher.school
    limit = Limit(school.config.plan, school)
    csv_data = []
    ifile = csv_file.read().decode("utf-8")
    for row in ifile.split('\n'):
        csv_data.append(row.split(','))
    
    result_objects = []
    # Check if headers exists. Skip the first entry if true.
    header_check = ['student', 'subject', 'test_score', 'class', 'term', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    # if all(i in first_row for i in header_check):
    csv_data = csv_data[1:]
    
    new_value = 0 # To get the number of records entered
    update_value = 0

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            if limit.limit_reached(Result):
                raise ValueError("You have exceeded the number of results you can upload. Upgrade your plan for more features")
            else:
                student = Student.objects.get(reg_number=row[0])
                subject = Subject.objects.get(short_code = str(row[1]).upper())
                student_class = StudentClass.objects.get(class_code=row[3])
                existing = Test.objects.filter(student=student, subject=subject, student_class=student_class,term=row[4])
                if existing.count() > 0:
                    if existing[0].test_score == 0.0:
                        existing[0].test_score = row[2]
                        existing[0].save()
                    update_value+=1
                else:
                    Test.objects.create(
                        student=student,
                        subject=subject,
                        school=teacher.school,
                        test_score=row[2],
                        student_class=student_class,
                        term=row[4],
                        session=row[5],
                    )
                    new_value+=1		
    return new_value, update_value


@transaction.atomic
def import_all_from_csv(csv_file, teacher, is_admin=False):
    """
    Import result CSV data.

    We'll process all rows first and create Result model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.
    
    """
    school = teacher.school
    limit = Limit(school.config.plan, school)
    csv_data = []
    ifile = csv_file.read().decode("utf-8")
    for row in ifile.split('\n'):
        csv_data.append(row.split(','))
    
    result_objects = []
    # Check if headers exists. Skip the first entry if true.
    header_check = ['student', 'subject', 'assignment_score', 'test_score', 'exam_score', 'class', 'term', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]
    
    new_value = 0 # To get the number of records entered
    update_value = 0

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            if limit.limit_reached(Result):
                raise ValueError("You have exceeded the number of results you can upload. Upgrade your plan for more features")
            else:
                student = Student.objects.get(reg_number=row[0])
                subject = Subject.objects.get(short_code=str(row[1]).upper())
                student_class = StudentClass.objects.get(class_code=row[5])
                if not is_admin:
                    subject = Subject.objects.get(short_code = str(row[1]).upper(), teachers=teacher)
                exiting = Result.objects.filter(student=student, subject=subject, 
                                                student_class=row[5], term=row[6])
                if exiting.count() > 0:
                    if existing[0].quiz_score == 0.0:
                        exiting[0].test_score = row[3]
                    if existing[0].exam_score == 0.0:
                        existing[0].exam_score = row[4]
                    if existing[0].assignment_score == 0.0:
                        existing[0].assignment_score = row[2]
                    existing[0].save()
                    update_value+=1
                else:
                    Result.objects.create(
                        student=student,
                        subject=subject,
                        school=teacher.school,
                        assignment_score=row[2],
                        quiz_score=row[3],
                        exam_score=row[4],
                        student_class=student_class,
                        term=row[6],
                        session=row[7],
                    )
                    new_value+=1			
    return new_value


@transaction.atomic
def import_assignment_from_csv(csv_file, teacher, is_admin=False):
    """
    Import result CSV data.

    We'll process all rows first and create Result model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.
    
    """
    school = teacher.school
    limit = Limit(school.config.plan, school)
    csv_data = []
    ifile = csv_file.read().decode("utf-8")
    for row in ifile.split('\n'):
        csv_data.append(row.split(','))
    
    result_objects = []
    # Check if headers exists. Skip the first entry if true.
    header_check = ['student', 'subject', 'score', 'class', 'term', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
    csv_data = csv_data[1:]
    
    count_value = 0 # To get the number of records entered
    found_value = 0

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        try:
            if row:
                if limit.limit_reached(Result):
                    raise ValueError("You have exceeded the number of results you can upload. Upgrade your plan for more features")
                else:
                    student = Student.objects.get(reg_number=row[0])
                    subject = Subject.objects.get(short_code = str(row[1]).upper(), teachers=teacher)
                    student_class = StudentClass.objects.get(class_code=row[3])
                    assignment = Assignment.objects.filter(student=student, subject=subject, student_class=student_class, term=row[4])
                    if assignment.exists():
                        assignment[0].assignment_score = row[2]
                        assignment[0].save()
                        found_value+=1
                    else:
                        Assignment.objects.create(
                            student=student,
                            subject=subject,
                            school=teacher.school,
                            assignment_score=row[2],
                            student_class=student_class,
                            term=row[4],
                            session=row[5]
                        )
        except Exception as e:
            raise ValueError(e)	
    return count_value, found_value


@transaction.atomic
def import_exam_from_csv(csv_file, teacher, is_admin=False):
    """
    Import result CSV data.

    We'll process all rows first and create Result model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.
    
    """
    school = teacher.school
    limit = Limit(school.config.plan, school)
    csv_data = []
    ifile = csv_file.read().decode("utf-8")
    for row in ifile.split('\n'):
        csv_data.append(row.split(','))
    
    result_objects = []
    # Check if headers exists. Skip the first entry if true.
    header_check = ['student', 'subject', 'score', 'class', 'term', 'session']
    first_row = [i.lower().strip() for i in csv_data[0]]
   
    csv_data = csv_data[1:]
    
    new_value = 0 # To get the number of records entered
    updated_value = 0
    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            if limit.limit_reached(Result):
                raise ValueError("You have exceeded the number of results you can upload. Upgrade your plan for more features")
            else:
                student = Student.objects.get(reg_number=row[0])
                subject = Subject.objects.get(short_code = str(row[1]).upper())
                student_class = StudentClass.objects.get(class_code=row[3])
                existing = Examination.objects.filter(student=student, subject=subject, student_class=student_class,term=row[4])
                result = Result.objects.filter(student=student, subject=subject, student_class=student_class,term=row[4])
                if result.exists():
                    rs = Result.objects.get(pk=result[0].id)
                    rs.exam_score = row[2]
                    rs.save()
                else:
                    Result.objects.create(
                        student=student, 
                        subject=subject, 
                        school=teacher.school,
                        student_class=student_class,
                        term=row[4], 
                        session=row[5],
                        exam_score=row[2],
                        signed_by=teacher
                    )
                if existing.exists():
                    existing[0].exam_score = row[2]
                    existing[0].save()
                    updated_value+=1
                else:
                    exam = Examination(
                        student=student,
                        subject=subject,
                        school=teacher.school,
                        exam_score=row[2],
                        student_class=student_class,
                        term=row[4],
                        session=row[5],
                    )
                    exam.save()
                    new_value+=1	
    return new_value, updated_value


class StudentReport(object):

    @classmethod
    def student_result(cls, student, school, term=None, year=None):
        data = {}
        results = Result.objects.filter(school=school, student=student)
        if term is not None:
            results = results.filter(term=term, date_created__year=year)
            data['student'] = student
            data['results'] = results
            data['total'] = sum([result.get_score for result in results])
            data['average'] = data['total']/results.count()

        else:
            for i in range(1,4):
                temp_data = {}
                results = results.filter(term=i)
                temp_data['total'] = sum([result.get_score for result in results])
                try:
                    temp_data['average'] = temp_data['total']/results.count()
                except ZeroDivisionError:
                    temp_data['average'] = 0.0
                temp_data['results'] = results
                data['student'] = student
                data['term-'+str(i)] = temp_data
        return data

    
    @classmethod
    def termly_report(cls, student, term=None, student_class=None, session=None):
        temp_data = {}
        try:
            results = Result.objects.filter(student=student, term=term, student_class=student_class)
            total_points = sum([result.get_score for result in results])
            try:
                average = float(total_points/results.count())
            except ZeroDivisionError:
                average = 0
            temp_data['total'] = total_points
            temp_data['average'] = "%.2f" % (average)
            temp_data['results'] = results
            temp_data['grade'] = grade(average, student.school)
        except: 
                pass
        return temp_data

    @classmethod
    def students_termly_reports(cls, student_class, term=None, session=None):
        """Returns a sorted dictionary of all the student's result for this term
        
        Arguments:
            student_class {StudentClass} -- The class a the students
        
        Keyword Arguments:
            term {integer} -- report term (default: {None})
            session {string} -- report session (default: {None})
        
        Returns:
            dict -- dictionary list of all students
        """
       
        
        year = session.split('/') # getting the first index of the list
        
        students = []
        for student in Result.objects.filter(student_class=student_class, 
                        term=term, date_created__year__in=year).values('student').distinct():
            students.append(student)
        
        # get the data from the database now
        data = {}
        for student in students:
            report = cls.termly_report(student, term, student_class, session)

            # we need to pass in something readable to the key of the data
            student_id = "id_{}".format(student.get('student'))
            data[student_id] = [report.get('total', 0.0), report.get('average', 0.0)]
        
        # sort the dictionary by the average
        try:
            sorted_data = OrderedDict(sorted(data.items(), key=lambda x: x[1][1], reverse=True))
        except Exception as e:
            sorted_data = {}
        return sorted_data

    
    @classmethod
    def termly_average(cls, term=None, session=None):
        pass

    @classmethod
    def overall_grade(cls, student, term=None, year=None):
        temp_data = {}
        results = Result.objects.filter(student=student)
        try:
            if term is not None:
                results = results.filter(term=term)
            if year is not None:
                results = results.filter(date_created__year=year)
            total_points = sum([result.get_score for result in results])
            try:
                average = float(total_points/results.count())
            except ZeroDivisionError:
                average = 0
            temp_data['total'] = total_points
            temp_data['average'] = float("%.2f" % (average))
            temp_data['results'] = results
            temp_data['grade'] = grade(average, student.school)
            data[student] = temp_data
        except: 
                pass
        return temp_data

    @classmethod
    def get_student_position(cls, student, student_class, term=None, session=None):
        """Return the student position in a particular class
        
        Arguments:
            student {object} -- student object
            student_class {object} -- class object
        
        Keyword Arguments:
            term {integer} -- term vlaue (default: {None})
            session {string} -- session value (default: {None})
        
        Returns:
            integer -- student's position
        """

        try:
            # coerce the right format for the student id in the sorted dictionary
            student_id = "id_{}".format(student.id)
            
            sorted_data = cls.students_termly_reports(student_class, term=term, session=session)
            return list(sorted_data.keys()).index(student_id)+1
        except Exception as e:
            return -1

    @classmethod
    def board(cls, school, term=None): 
        """Progress award board data for a particular school
        
        Arguments:
            school {integer} -- school id
        
        Keyword Arguments:
            term {integer} -- term number (default: {None})
        
        Returns:
            dict -- sorted dictionary of students grade
        """

        import datetime
        current_year = datetime.date.today().year
        students = Student.objects.filter(school=school)
        data = {student:cls.overall_grade(student, term=term, year=current_year).get('average') for student in students}
        sorted_data = OrderedDict(sorted(data.items(), key=operator.itemgetter(1), reverse=True))
        return sorted_data
    
    @classmethod
    def get_data(cls, student_class, session=None, term=None):
        """Returns the students data in a particular class
        
        Arguments:
            student_class {object} -- student class object
        
        Keyword Arguments:
            session {string} -- session (default: {None})
            term {integer} -- term value (default: {None})
        
        Returns:
            dict -- students data
        """

        data = {'students': [], 'header': [], 'scores': [], 'averages': [], 'position': []}
        sorted_data = cls.students_termly_reports(student_class, term=term, session=session)
        results = Result.objects.filter(student_class=student_class, term=term).select_related('student', 'student_class', 'subject')
        subjects = set([result.subject.name for result in results])
        position = get_position(sorted_data)

        # load the students data
        for student_index, [total, average] in sorted_data.items():
            student = Student.objects.get(id=student_index.split('_')[1])
            
            # compute the total scores
            scores = []
            for result in results.filter(student=student):
                scores.append(result.get_score)
            
            payload = {
                'name': student.full_name,
                'reg_number': student.reg_number,
                'position': next(position),
                'average': average,
                'total': sum(scores),
            }
            rep = Repr(scores, **payload)
            data['students'].append(rep)
            data['obtainable'] = len(subjects) * 100
            data['class_no'] = len(sorted_data)
        for x in subjects:
            data['header'].append(x)
        return data


def grade(score, school):
        score = int(score)
        grades = Grading.objects.filter(institution=school)
        grade = [grade.caption.upper() for grade in grades if score in range(grade.start, grade.end+1)]
        
        return grade[0]

def get_position(sorted_data):
    '''
    [:Generator] Return student's position from a sorted report data.
    This is to factor in possibilities of ties
    '''
    lst = list(sorted_data.values())
    new_list = []
    current = 0
    prev = 0
    for i in range(len(sorted_data)):
        if lst[i] == lst[i-1]:
            prev = current+1
            new_list.append(prev)
        else:
            new_list.append(i+1)
            current = i
    for i in new_list:
        yield i


class Repr:
    def __init__(self, scores, **kwargs):
        self.name = kwargs.pop('name')
        self.reg_number = kwargs.pop('reg_number')
        self.position = kwargs.pop('position')
        self.average = kwargs.pop('average')
        self.total = kwargs.pop('total')
        self.scores = scores




class SubjectGrade:

    def __init__(self, subject_number, subject_full_number):
        self.subject_number = subject_number
        self.subject_full_number = subject_full_number

    def subgrade(self):
        number_aplus = (self.subject_full_number/100)*80
        number_a = (self.subject_full_number/100)*70
        number_aminus = (self.subject_full_number/100)*60
        number_b = (self.subject_full_number/100)*50
        number_c = (self.subject_full_number/100)*40
        number_d = (self.subject_full_number/100)*33
        number_f = (self.subject_full_number/100)*1

        if self.subject_number >= number_aplus and self.subject_number:
            return 'A+'
        elif self.subject_number >= number_a and self.subject_number < (number_aplus):
            return 'A'

        elif self.subject_number >= number_aminus and self.subject_number <(number_a):
            return 'A-'

        elif self.subject_number >= number_b and self.subject_number <(number_aminus):
            return 'B'

        elif self.subject_number >= number_c and self.subject_number <(number_b):
            return 'C'

        elif self.subject_number >= number_d and self.subject_number <(number_c):
            return 'D'

        elif self.subject_number >= number_f and self.subject_number <(number_d):
            return 'F'

        elif self.subject_number == 0:
            return 'F'
        

class SubjectGradePoint:

    def __init__(self, subject_number, subject_full_number):
        self.subject_number = subject_number
        self.subject_full_number = subject_full_number

    def subgrade(self):
        number_aplus = (self.subject_full_number/100)*80
        number_a = (self.subject_full_number/100)*70
        number_aminus = (self.subject_full_number/100)*60
        number_b = (self.subject_full_number/100)*50
        number_c = (self.subject_full_number/100)*40
        number_d = (self.subject_full_number/100)*33
        number_f = (self.subject_full_number/100)*1

        if self.subject_number >= number_aplus and self.subject_number:
            return 5
        elif self.subject_number >= number_a and self.subject_number < (number_aplus):
            return 4

        elif self.subject_number >= number_aminus and  self.subject_number < (number_a):
            return 3.5

        elif self.subject_number >= number_b and self.subject_number < (number_aminus):
            return 3

        elif self.subject_number >= number_c and self.subject_number < (number_b):
            return 2

        elif self.subject_number >= number_d and self.subject_number < (number_c):
            return 1

        elif self.subject_number >= number_f and self.subject_number < (number_d):
            return 0

        elif self.subject_number==0:
            return 0
