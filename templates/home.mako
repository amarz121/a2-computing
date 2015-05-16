
<%inherit file='base.mako' />

<p> You are logged in as ${ login } </p>

<a href="${ request.route_url('students') }">All Students</a>
<p><a href="${ request.route_url('classes') }">All Classes</a></p>

% if isAdministrator:
<p><a href="${ request.route_url('users') }">All Users</a></p>
<h3>Register User</h3>
<ul>
	<li><a href="${ request.route_url('register', role='administrator') }">Administrator </a></li>
	<li><a href="${ request.route_url('register', role='teacher') }">Teacher</a></li>
	<li><a href="${ request.route_url('register', role='director') }">Director</a></li>
	<li><a href="${ request.route_url('register', role='assistant') }">Assistant</a></li>
</ul>
% endif

% if isTeacher:
<h2>Classes Taught</h2>
% if classesTaught:
<table>
% for cl in classesTaught:
<tr>
	<td><a href="${ request.route_url('class', id=cl.id) }">${ cl.id } </a></td>
	<td>${ cl.name }</td>
</tr>
% endfor
</table>
% else:
You aren't currently assigned to teach any classes.
% endif

% if interventions:
<table>
<h2>Interventions created:</h2>
<tr>
	<td><b> Date - Time  </b></td>
	<td><b> Teacher </b></td>
	<td><b> Student </b></td>
	<td><b> Content </b></td>
</tr>
% for i in interventions:
<tr>
	<td> ${ i.date_time } </td>
	<td> ${ i.made_by.title } ${ i.made_by.surname } </td>
	<td><a  href="${ request.route_url('student', id=i.applies_to.id) }"> ${ i.applies_to.forename } ${ i.applies_to.surname }</a></td>
	<td> ${ i.content }</td>
</tr>
% endfor
</table>
% else:
There are no interventions.
% endif
% endif


