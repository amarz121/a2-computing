<%inherit file='base.mako' />

<h2>Class: ${ cl.name }</h2>

% if teacher:
<h3>Teacher assigned : ${ cl.teacher_id } - ${ teacher.title } ${ teacher.surname }</h3>
	% if isAdministrator:
		<p><a href="${ request.route_url('assign_teacher', id=cl.id) }">Change assigned teacher</a></p>
	% endif
% else:
There is no teacher assigned to this class. 
	% if isAdministrator:
		<p><a href="${ request.route_url('assign_teacher', id=cl.id) }">Assign new teacher</a></p>
	% endif
% endif

<h3>Students enrolled:</h3>

% if isAdministrator or isDirector:
<p><a href="${ request.route_url('enrol_students', id=cl.id) }">Enrol new students</a></p>
% endif

% if cl.students:
<table>
	## Table Headings
	<tr>
		<td><b>Name</b></td>
		<td><b>ID</b></td>
		<td><b>Grade</b></td>
		<td><b>Status</b></td>
		% if not isAssistant:
		<td><b>Edit</b></td>
		% endif
	</tr> 

% for student in cl.students:
	<tr>
		<td> ${ student.surname.upper() }, ${ student.forename } </td>
		<td><a href="${ request.route_url('student', id= student.id )}"> ${ student.id  }</a></td>
		
		% for assoc in student.classlist:
			% if assoc.class_id == cl.id:
				<td align="center"> ${ assoc.grade } </td>
				<td> ${ assoc.status }</td>
			% endif
		% endfor
		% if not isAssistant:
		<td align="center"><a href="${ request.route_url('edit_student_in_class', id=student.id, classId=cl.id) }"> Edit</a></td>
		% endif
	</tr>
% endfor
</table>
% else:
<p>There are currently no students enrolled in this class. </p>
% endif