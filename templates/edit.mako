<%inherit file='base.mako' />

<form action="${ request.path }" method="POST">

% if isTeacher:
	% if teachesClass or isDirector:
		<h3>Change grade of student</h3>
		<select name="grade">
			<option value="A*">A*</option>
			<option value="A">A</option>
			<option value="B">B</option>
			<option value="C">C</option>
			<option value="D">D</option>
			<option value="E">E</option>
			<option value="U">U</option>
		</select> 
		% if not isDirector:
			<p><input type="submit" name="submit" value="Submit"/></p>
		% endif
	% else:
		<p> You do not have access to change the grade of \
			this student, as you do not teach this class.
		<p>Click <a href="${ request.route_url('student', id= student_id )}">here</a> to go back to the student.
	% endif
% endif

% if isAdministrator or isDirector:
<h3>Change status of student</h3>
<select name="status">
  <option value="Active">Active</option>
  <option value="Suspended">Suspended</option>
  <option value="Withdrawn">Withdrawn</option>
</select> 
<p><input type="submit" name="submit" value="Submit"/></p>
</form>
% endif