<%inherit file='base.mako' />

<h3>Assign Teacher to Class ${ class_id }</h3>

%if not teachers:
	<p> There are no teachers registered. Click <a href="${ request.route_url('register', role='teacher')}">here</a> to register a teacher.</p>
% else:
	<form action="${ request.path }" method="POST">
	% for t in teachers:
		<input type="radio" name="teacher_id" value="${ t.id }">${ t.id } - ${ t.title } ${ t.surname }</input></br>
	% endfor
	<p><input type="submit" name="submit" value="Submit"/></p>
	</form>
% endif