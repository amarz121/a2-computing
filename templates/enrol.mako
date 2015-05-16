<%inherit file='base.mako' />

<h3>Enrol students in class ${ class_id }</h3>

<form action="${ request.path }" method="POST">

% for student  in notEnrolledStudents:
    <input type="checkbox" name="student_id" value="${ student.id }" >${ student.id } - ${ student.forename } ${ student.surname }</input><br/> 
% endfor

<p><input type="submit" name="submit" value="Submit"/></p>

</form>