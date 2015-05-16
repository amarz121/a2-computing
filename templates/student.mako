<%inherit file='base.mako' />

<h2>${ student.forename } ${ student.surname.upper() }</h2>

<h3>${ student.address }</h3>

## If student is enrolled in a class
% if student.classlist:
<table>
	## Table Headings
	<tr>
		<td><b>ID</b></td>
		<td><b>Name</b></td>
		<td><b>Teacher</b></td>
		<td><b>Grade</b></td>
		<td><b>Status</b></td>
	</tr>

<h4> Classes enrolled in: </h4>

	% for assoc in student.classlist:
		<tr>
			<td> ${ assoc.theClass.name }</td>
			<td><a href="${ request.route_url('class', id=assoc.theClass.id) }"> ${ assoc.theClass.id }</a></td>  
			% if assoc.theClass.teacher_id:
				<td> ${assoc.theClass.taught_by.title} ${assoc.theClass.taught_by.surname}</td>
			% else:
				<td>TBD</td>
			% endif
			<td align="center">${ assoc.grade }</td>
			<td>${ assoc.status }</td>
			% if not isAssistant:
			<td><a href="${ request.route_url('edit_student_in_class', id=student.id, classId=assoc.theClass.id) }">Edit</a></td>
			% endif
		</tr>
	% endfor
</table>
% else:
	<p>${ student.forename } ${ student.surname } is not enrolled in any classes yet. </p>
% endif

<h4>Interventions:</h4>
% if isTeacher:
<p><a href="${ request.route_url('intervene', id=student.id) }">Create Intervention</a></p>
% endif

% if student.interventionlist:
	% for int1 in student.interventionlist:
			<p><b>${ int1.date_time }</b> - created by ${ int1.made_by.title } ${ int1.made_by.surname } </br>
		${ int1.content }</p>
	% endfor
% else:
<p>There are no interventions for ${ student.forename } ${ student.surname } at the moment.
% endif