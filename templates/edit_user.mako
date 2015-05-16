<%inherit file='base.mako' />

% if errors:
<ul>
    % for e in errors:
    <li><font color="red">${ e }</font></li>
    % endfor
</ul>
% endif
<form method="post" action="${ request.path }">
<label for="title">Title</label><br>
<select name="title">
  <option value="Mr">Mr</option>
  <option value="Mrs">Mrs</option>
  <option value="Miss">Miss</option>
  <option value="Ms">Ms</option>
  <option value="Dr">Dr</option>
  <option value="Prof">Prof</option>
</select> 
    <p>
        <label for="surname">Surname</label><br>
        <input type="text" name="surname" value="${ surname }">
    </p>
        <p>
        <label for="username">Username</label><br>
        <input type="text" name="username" value="${ username}">
    </p>
    <p>
        <label for="passwd">Password</label><br>
        <input type="password" name="passwd">
    </p>
    <p>
        <label for="password">Confirm Password</label><br>
        <input type="password" name="password">
    </p>
    	  <input type="submit" name="submit" value="Submit"/>
</form>