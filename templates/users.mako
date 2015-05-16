<%inherit file='base.mako' />

<h3>Register User</h3>
<ul>
	<li><a href="${ request.route_url('register', role='administrator') }">Administrator </a></li>
	<li><a href="${ request.route_url('register', role='teacher') }">Teacher</a></li>
	<li><a href="${ request.route_url('register', role='director') }">Director</a></li>
	<li><a href="${ request.route_url('register', role='assistant') }">Assistant</a></li>
</ul>

% if users:
<h2>All Users</h2>
<table>
% for u in users:
<tr>
	<td> ${ u.title  } ${ u.surname }</td>
	<td><a href="${ request.route_url('user', id=u.id) }">${ u.id }</a></td>
</tr>
% endfor
</table>
% endif