<%inherit file='base.mako' />

% if isAdministrator == True:
<p>Register a student <a href="${ request.route_url('add_student')}">here</a></p>
% endif

% if isTeacher:
<h2>Your Students</h2>
% if studentsTaught:
<table>
<tr>
	<td><b> Name </b></td>
	<td><b> ID </b></td>
</tr>
% for student in studentsTaught:
<tr>
	<td>${ student.surname.upper() }, ${ student.forename }</td>
	<td><a href="${ request.route_url('student', id=student.id)}">${ student.id }</a></td>
</tr>
% endfor
</table>
% else:
You are not teaching any students.
% endif
% endif


<h2>All Students</h2>
<table>
<tr>
	<td><b> Name </b></td>
	<td><b> ID </b></td>
</tr>
% for student in students:
<tr>
	<td>${ student.surname.upper() }, ${ student.forename }</td>
	<td><a href="${ request.route_url('student', id=student.id)}">${ student.id }</a></td>
</tr>
% endfor
</table>