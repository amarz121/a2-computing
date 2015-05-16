from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPForbidden, HTTPFound, HTTPNotFound
from pyramid.view import forbidden_view_config, view_config
from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Authenticated, authenticated_userid, forget, remember, effective_principals

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import datetime

engine = create_engine('sqlite:///studentRecordSystem.db', echo=True)
# engine = create_engine('sqlite:///studentRecordSystem.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

### DEFINE MODEL
class Association(Base):
    __tablename__ = 'association'
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    grade = Column(String(2))
    status = Column(String(9))
    theClass = relationship("Class")
    
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    forename = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    address = Column(String(50), nullable=False)
    classlist = relationship("Association")
    interventionlist = relationship("Intervention", backref='students')

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id')) 
    students = relationship("Student", secondary="association",
                                     backref="classes")
    
class Intervention(Base):
    __tablename__ = 'interventions'
    id = Column(Integer, primary_key=True)
    date_time = Column(String(15))
    content = Column(String(300), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    made_by = relationship("Teacher")
    applies_to = relationship("Student")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    title = Column(String(4), nullable=False)
    surname = Column(String(20), nullable=False)
    username = Column(String(10), nullable=False)
    password = Column(String(8), nullable=False)

    # Method of User object
    def check_password(self, passwd):
        return self.password == passwd
    
class Administrator(User):
    __tablename__ = 'administrators'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
class Teacher(User):
    __tablename__ = 'teachers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    teaches = relationship("Class", backref="taught_by")
    
class Director(Teacher):                
    __tablename__ = 'directors'
    id = Column(Integer, ForeignKey('teachers.id'), primary_key=True)

class Assistant(User):
    __tablename__ = 'assistants'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Commits session to create tables in database.
session.commit()

### MAP GROUPS TO PERMISSIONS

class Root(object):
    # Using Access Control List to assign different permissions to each type of user.
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'administrator', ('register', 'edit', 'enrol')),
	(Allow, 'director', 'enrol'),
        (Allow, 'teacher', ('intervene', 'edit')),
        ]
    def __init__(self, request):
        self.request = request

 
def rolefinder(login, request):
    if session.query(Director).filter_by(username = login).first():
        return [ 'teacher', 'director']
    elif session.query(Teacher).filter_by(username = login).first():
        return [ 'teacher' ]
    elif session.query(Administrator).filter_by(username = login).first():
        return ['administrator']
    elif session.query(Assistant).filter_by(username = login).first():
        return ['assistant']
    else:
        return []

### DEFINE VIEWS

# Copied from Michael Merickel's tutorial, with additional comments
@forbidden_view_config()
def forbidden_view(request):
    # Authorization failure because lacking permission
    if authenticated_userid(request):
        return HTTPForbidden()

    # Authorization failure because not logged in
    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)

@view_config(
    route_name='home',
    permission="view", # invokes forbidden_view if not authenticated
    renderer='home.mako' # template for each view
    )
def home_view(request):
    roles = effective_principals(request)
    # login occurs in roles after 'system.Everyone' and 'system.Authenticated'
    login = roles[2]

    # Obtain user object and all class objects from database
    user = session.query(User).filter_by(username = login).first()
    classes = session.query(Class).all()

    # Determine values of remaining variables required by template
    isAdministrator = isTeacher = False
    interventions = classesTaught = []
    if 'administrator' in roles:
        isAdministrator = True
    elif 'teacher' in roles:
        isTeacher = True
        classesTaught = session.query(Class).filter_by(teacher_id=user.id).all()
	# Shows the 10 most recent interventions created
        interventions = session.query(Intervention).order_by(Intervention.id.desc()).limit(10).all()

    return {
        # Returns values required in templates
        'login' : login,
        'user' : user,
        'classes' : classes,
        'isAdministrator' : isAdministrator,
        'isTeacher' : isTeacher,
        'classesTaught' : classesTaught,
        'interventions': interventions,
        }

# Copied from Michael Merickel's tutorial, replacing one line and removing unused element from dictionary
@view_config(
    route_name='login',
    renderer='login.mako',
)
def login_view(request):
    # Redirect logged in user to home page
    if authenticated_userid(request):
        return HTTPFound(location=request.route_url('home'))
    next = request.params.get('next') or request.route_url('home')
    login = ''
    did_fail = False
    if 'submit' in request.POST:
        login = request.POST.get('login', '')
        passwd = request.POST.get('passwd', '')
        
        # Obtain user object from database
        user = session.query(User).filter_by(username=login).first()

        if user and user.check_password(passwd):
	    # Used to locally store cookie, named auth_tkt, to set users credentials
            headers = remember(request, login)
            return HTTPFound(location=next, headers=headers)
        did_fail = True

    return {
        'login': login,
        'next': next,
        'failed_attempt': did_fail,
    }

# Copied from Michael Merickel's tutorial, changing a route
@view_config(
    route_name='logout',
)
def logout_view(request):
    # 'forget()' used to delete locally stored AuthTkt cookie, to remove credentials provided by user
    headers = forget(request)
    loc = request.route_url('login')
    return HTTPFound(location=loc, headers=headers)

# Copied from Michael Merickel's tutorial and querying through database, instead of through a dictionary	
@view_config(
    route_name='users',
    permission="register",
    renderer='users.mako'
    )
def users_view(request):
    # Obtain all user objects from database
    users = session.query(User).order_by(User.surname.asc(), User.id.asc()).all()
    return {
        'users' : users
        }
	
@view_config(
    route_name='user',
    permission="register",
    renderer='user.mako',
)
def user_view(request):
    id = request.matchdict['id']
    user = session.query(User).filter_by(id = id).first()
    if not user:
        raise HTTPNotFound()
    return {
        'user': user,
        }

def validate_user(surname, username, passwd, password):
    errors = []
	
    # strip() gets rid of leading or trailing characters
    surname = surname.strip()
    if not surname:
        errors.append('Surname must not be empty, please enter surname')
    elif len(surname) > 20:
        errors.append('Please shorten surname to atmost 20 characters')
    # Ensures input contains only letters
    elif  surname.isalpha() == False:
        errors.append('Surname must only contain letters, please re-enter surname')

    username = username.strip()
    if not username:
        errors.append('Username must not be empty, please enter username')
    elif len(username) > 10:
        errors.append('Please shorten username to atmost 10 characters')
    # Checks database to verify username is unique
    usernameInUse = session.query(User).filter_by(username = username).first()
    if usernameInUse:
        errors.append('Username is already in use, please enter a different username')
        
    for p in [passwd, password]:
        p = p.strip()
        if not p:
            errors.append('Password must not be empty, please enter a password')
        elif len(p) < 5 :
            errors.append('Password must be at least 5 characters long, please enter a password')
	
    # confirms password entered is the one desired
    if passwd != password:
        errors.append('Password fields must match, please try again')
    return {
        'surname': surname,
        'username': username,
        'password' : password,
        'passwd': passwd,
        'errors': errors,
    }

@view_config(
    route_name='register',
    permission='register',
    renderer='edit_user.mako'
)
def register_user(request):
    # 'role' extracted from the URL 
    role = request.matchdict['role']
    if not role in ['administrator', 'teacher', 'director', 'assistant']:
        raise HTTPNotFound()
    
    errors = []
    surname = username = password = ''
    
    # Uses template to retrieve values for variables
    if request.method == 'POST':
        title = request.POST.get('title') 
        surname = request.POST.get('surname', '')
        username = request.POST.get('username', '') 
        passwd = request.POST.get('passwd', '')
        password = request.POST.get('password', '') 

        v = validate_user(surname, username, passwd, password)
        surname = v['surname']
        username = v['username']
        passwd = v['passwd']
        password = v['password']
        errors += v['errors']

        # stores all attributes of user in dictionary
        attributes = {'title': title,
                      'surname': surname.capitalize(),
                      'username': username,
                      'password': password
                      }
        if not errors:
            # Use ** operator to unpack dictionary to deliver keyword arguments
            if role == 'administrator':
                newUser = Administrator(**attributes)
            elif role == 'teacher':
                newUser = Teacher(**attributes)
            elif role == 'director':
                newUser = Director(**attributes)
            else: # role == 'assistant':
                newUser = Assistant(**attributes)
            session.add(newUser)
            session.commit()
            
            url = request.route_url('user', id=newUser.id)
            return HTTPFound(location=url)

    return {
        'surname': surname,
        'username': username,
        'password' : password,
        'errors': errors
        }

@view_config(
    route_name='students',
    permission="view",
    renderer='students.mako'
    )
def students_view(request):
    roles = effective_principals(request)
    # login occurs in roles after 'system.Everyone' and 'system.Authenticated'
    login = roles[2]
	
    # Locates user object with the same username as in 'effective_principals'
    user = session.query(User).filter_by(username = login).first()

    # List of all students in alphabetical order
    students = session.query(Student).order_by(Student.surname.asc(), Student.forename.asc(), Student.id.asc()).all()
    isAdministrator = isTeacher = False
    classesTaught = studentsTaught = []

    if 'administrator' in roles:
        isAdministrator = True
    if 'teacher' in roles:
        isTeacher = True
        # Finds all classes taught by the user
        classesTaught = session.query(Class).filter_by(teacher_id = user.id).all()
		
        # Use set comprehension to remove duplicate students
        setOfStudentsTaught = {st for cl in classesTaught for st in cl.students}
        # Use list comprehension to put in alphabetical order 
        studentsTaught = [st for st in students if st in setOfStudentsTaught]    

    return {
        'students' : students,
	'isAdministrator': isAdministrator,
	'isTeacher': isTeacher,
	'classesTaught': classesTaught,
	'studentsTaught': studentsTaught,
    }

@view_config(
    route_name='student',
    permission="view",
    renderer='student.mako'
    )
def student_view(request):
    roles = effective_principals(request)
    login = roles[2]
    id = request.matchdict['id']
    # Finds student object using ID in URL and matching to ID in students table
    student = session.query(Student).filter_by(id = id).first()
    if not student:
        raise HTTPNotFound()
    
    isTeacher = isAssistant = False
    
    if 'teacher' in roles:
        isTeacher = True
    if 'assistant' in roles:
        isAssistant = True
 
    return {
        'student': student,
	'isTeacher': isTeacher,
	'isAssistant': isAssistant,
        }

def validate_student(forename, surname, address):
    errors = []

    forename = forename.strip()
    if not forename:
        errors.append('Forename may not be empty, please enter forename')
    elif len(forename) > 20:
        errors.append('Please shorten forename to atmost 20 characters')
    elif  forename.isalpha() == False:
        errors.append('Forename must only contain letters, please re-enter forename')

    surname = surname.strip()
    if not surname:
        errors.append('Surname may not be empty, please enter surname')
    elif len(surname) > 20:
        errors.append('Please shorten surname to atmost 20 characters')
    elif  surname.isalpha() == False:
        errors.append('Surname must only contain letters, please re-enter surname')
		
    address = address.strip()
    if not address:
        errors.append('Address may not be empty, please enter address')
    elif len(surname) > 50:
        errors.append('Please shorten address to atmost 50 characters')
		
    return {
        'forename': forename,
        'surname': surname,
        'address': address,
        'errors': errors,
    }

@view_config(
    route_name='add_student',
    permission='register',
    renderer='edit_student.mako'
)
def add_student(request): 
    errors = []
    forename = surname = address = ''
    if request.method == 'POST':
        forename = request.POST.get('forename', '')
        surname = request.POST.get('surname', '')
        address = request.POST.get('address', '')

        v = validate_student(forename, surname, address)
        forename = v['forename']
        surname = v['surname']
        address = v['address']
        errors += v['errors']

        if not errors:
            newStudent = Student(forename=forename.capitalize(), surname=surname.capitalize(), address=address)
            session.add(newStudent)
            session.commit()
            url = request.route_url('student', id=newStudent.id)
            return HTTPFound(location=url)

    return {
        'forename': forename,
        'surname': surname,
        'address': address,
        'errors': errors,
    }

def validate_intervention(content):
    errors = []
    content = content.strip()
    if not content:
        errors.append('Content may not be empty, please enter content')
    elif len(content) > 300:
        errors.append('Please shorten content to atmost 300 characters')
    return {
        'content': content,
        'errors': errors,
    }

@view_config(
    route_name='intervene',
    permission='intervene',
    renderer='intervene.mako'
    )
def edit_intervention(request):
    login = authenticated_userid(request)
    # Locates user object with the same username as the one in request, from database
    user = session.query(User).filter(login == User.username).first()
    
    errors = []
    date_time = content = ''
    student_id = request.matchdict['id']
    if request.method == 'POST':
        content = request.POST.get('content', '')

        v = validate_intervention(content)
        content = v['content']
        errors += v['errors']

        if not errors:
	    # Formatted to show date time format as dd/mm/yy HH:MM
            date_time = datetime.now().strftime("%d/%m/%y %H:%M")
            int1 = Intervention(date_time=date_time, content=content)
            session.add(int1)
            # Assigning foreign keys to Intervention object for relationships between tables
            int1.student_id = student_id
            int1.teacher_id = user.id
            session.commit()
            url = request.route_url('student', id=student_id)
            return HTTPFound(location=url)
    return {
        'date_time': date_time,
        'content': content,
        'student_id': student_id,
        'user': user,
        'errors': errors,
    }

@view_config(
    route_name='edit_student_in_class',
    permission="edit",
    renderer='edit.mako'
    )
def edit_student_in_class_view(request):
    student_id = request.matchdict['id']
    class_id = request.matchdict['classId']
	
    roles = effective_principals(request)
    login = roles[2]
    # Finds user object by looking up username with the one from effective_principals
    user = session.query(User).filter_by(username = login).first()
    assoc = session.query(Association).filter_by(student_id=student_id, class_id=class_id).first()
    cl = session.query(Class).filter_by(id = class_id).first()
    
    isAdministrator = isTeacher = teachesClass = isDirector = False

    if 'administrator' in roles:
        isAdministrator = True
    if 'teacher' in roles:
        isTeacher = True
        if cl.teacher_id == user.id:
            teachesClass = True
    if 'director' in roles:
        isDirector = True
	
    if request.method == 'POST':
        # Only teacher can edit grade
        if isTeacher:
            # Only teacher assigned to the class or director is permitted to change the grades
            if teachesClass or isDirector:
                grade = request.POST.get('grade')
                assoc.grade = grade
            else:
                return HTTPForbidden()
        # Only administrator or director can change status
        if isAdministrator or isDirector:
            status = request.POST.get('status')
            assoc.status = status
        session.commit()
        url = request.route_url('student', id=student_id)
        return HTTPFound(location=url)
		
    return {
        'student_id' : student_id,
        'user': user,
        'cl': cl,
        'isAdministrator': isAdministrator,
	'isTeacher': isTeacher,
        'teachesClass': teachesClass,
	'isDirector': isDirector,
        }

@view_config(
    route_name='classes',
    permission="view",
    renderer='classes.mako'
    )
def classes_view(request):
    roles = effective_principals(request)
    login = roles[2]
	
    user = session.query(User).filter_by(username = login).first()
    classes = session.query(Class).all()

    isAdministrator = isTeacher = False
    classesTaught = []
    
    if 'administrator' in roles:
        isAdministrator = True
    if 'teacher' in roles:
        isTeacher = True
        classesTaught = session.query(Class).filter(Class.teacher_id == user.id).all()
    return {
	'classes' : classes,
	'isAdministrator': isAdministrator,
	'isTeacher': isTeacher,
        'classesTaught' : classesTaught,
        }

@view_config(
    route_name='class',
    permission="view",
    renderer='class.mako'
    )
def class_view(request):
    id = request.matchdict['id']
    cl = session.query(Class).filter_by(id = id).first()
    if not cl:
        raise HTTPNotFound()
    
    roles = effective_principals(request)
    login = roles[2]
    teacher = session.query(User).filter(cl.teacher_id == User.id).first()

    isAdministrator = isDirector = isAssistant = False
    
    if 'administrator' in roles:
        isAdministrator = True
    if 'director' in roles:
        isDirector = True
    if 'assistant' in roles:
        isAssistant = True
    return {
        'cl': cl,
        'teacher': teacher,
        'isAdministrator': isAdministrator,
        'isDirector': isDirector,
	'isAssistant': isAssistant,
        }

def validate_class(name):
    errors = []
    
    name = name.strip()
    if not name:
        errors.append('Name must not be empty, please enter the name of the class.')
    elif len(name) > 20:
        errors.append('Please shorten name to atmost 20 characters')
    # Checks database to verify class name is unique
    classNameInUse = session.query(Class).filter_by(name = name).first()
    if classNameInUse:
        errors.append('The name for your class is already in use, please enter another name.')
        
    return {
        'name': name,
        'errors': errors,
    }

@view_config(
    route_name='add_class',
    permission='register',
    renderer='create_class.mako'
    )
def add_class(request):
    errors = []
    name = ''
    if request.method == 'POST':
        name = request.POST.get('name', '')

        v = validate_class(name)
        name = v['name']
        errors += v['errors']

        if not errors: # check class exists
            cl = Class(name=name)
            session.add(cl)
            session.commit()
            url = request.route_url('assign_teacher', id=cl.id)
            return HTTPFound(location=url)

    return {
        'name': name,
        'errors': errors,
    }

@view_config(
    route_name='assign_teacher',
    permission='register',
    renderer='assign.mako'
    )
def assign_teacher(request):
    class_id = request.matchdict['id']
    teachers = session.query(Teacher).all()
    
    if 'submit' in request.POST:
        teacher_id = request.POST.get('teacher_id')
        cl = session.query(Class).filter(Class.id==class_id).first()
        # Assigning value to foreign key to establish relationship
        cl.teacher_id = teacher_id
        session.commit()
        url = request.route_url('class', id = class_id)
        return HTTPFound(location=url)

    return {
        'class_id': class_id,
        'teachers': teachers,		
        'teachers': session.query(Teacher).all(),
        }

@view_config(
    route_name='enrol_students',
    permission='enrol',
    renderer='enrol.mako'
    )
def enrol_students(request):
    class_id = request.matchdict['id']
    currentClass = session.query(Class).filter_by(id=class_id).first()
    students = session.query(Student).all()

    # Check students exist and are not already enrolled in currentClass
    notEnrolledStudents = [st for st in students if not st in currentClass.students]
	
    if request.method == 'POST':
        student_ids = request.POST.getall('student_id')
        
        for student_id in student_ids:
	    # Create new Association object for student with status set by default to 'Active'
            student = Association(class_id=class_id, student_id=student_id, grade='', status='Active')
            session.add(student)
        session.commit()
        url = request.route_url('class', id=class_id)
        return HTTPFound(location=url)
    
    return {
        'currentClass': currentClass,
        'class_id': class_id,
        'notEnrolledStudents': notEnrolledStudents,
        }

# Copied from Merickel's tutorial, with modified routes, and additional parameters in authn_policy
### CONFIGURE PYRAMID

def main(global_settings, **settings):
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        # Callback passes to userid and request, returns a sequence of principal identifiers if the user exists. 
        callback=rolefinder,
        # Used to timeout session based on inactivity
        # The maximum time a newly issued ticket will be considered valid, until expiring
        timeout=1200,
        # time that must pass before an auth_tkt is automatically reissued as the result of a request which requires authentication
        reissue_time=120,
        hashalg='sha512'
        )
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        root_factory=Root,
    )
    
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home', '/')
    
    config.add_route('users', '/users')
    config.add_route('user', '/user/{id}')
    config.add_route('register', '/register/{role}')
    
    config.add_route('students', '/students')
    config.add_route('student', '/student/{id}')
    config.add_route('add_student', '/add_student')
    config.add_route('intervene', '/student/{id}/intervene')
    config.add_route('edit_student_in_class', '/student/{id}/{classId}')

    config.add_route('classes', '/classes')
    config.add_route('class', '/class/{id}')
    config.add_route('add_class', '/add_class')
    config.add_route('assign_teacher', '/class/{id}/assign')
    config.add_route('enrol_students', '/class/{id}/enrol')

    config.scan(__name__)
    return config.make_wsgi_app()

# Copied from Merickels tutorial, changing the auth.secret and switching to a more stable server
### SIMPLE STARTUP
if __name__ == '__main__':
    settings = {
        # secret should be at least as long as the block size of the selected hash algorithm, 64 characters in the case of sha512
        'auth.secret': '584A07CED70EDBF8146A76133B41D4070EEF41645CC77DB0610383B234FC38EB',
        'mako.directories': '%s:templates' % __name__,
    }
    app = main({}, **settings)

    '''from waitress import serve
    serve(app, host='0.0.0.0', port=5000)'''
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
