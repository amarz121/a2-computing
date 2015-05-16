<%inherit file='base.mako' />

% if isAdministrator:
<p>Create a class <a href="${ request.route_url('add_class') }">here</a></p>
% endif

% if isTeacher:
<h2>Your Classes</h2>
% if classesTaught:
<table>
	% for cl in classesTaught:
	<tr>
		<td><a href="${ request.route_url('class', id=cl.id) }">${ cl.id }</a></td>
		<td> ${ cl.name }</td>
	</tr>
	% endfor
</table>
% else:
You are not currently teaching any classes.
% endif
% endif

<h2>All Classes</h2>
% if classes:
<table>
% for cl in classes:
<tr>
	<td><a href="${ request.route_url('class', id=cl.id) }">${ cl.id }</a></td> 
	<td> ${ cl.name }</td>
</tr>
% endfor
</table>
% else:
There are no classes.
% endif