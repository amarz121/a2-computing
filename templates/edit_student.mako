<%inherit file='base.mako' />

<h2>Register Student</h2>

% if errors:
<ul>
    % for e in errors:
    <li>${ e }</li>
    % endfor
</ul>
% endif

<form method="post" action="${ request.path }">
<p> 
    <label for="forename">Forename</label><br>
    <input type="text" name="forename" value="${ forename }"/
</p>
<p> 
    <label for="surname">Surname</label><br>
    <input type="text" name="surname" value="${ surname }"/>
</p>
<p>
    <label for="address">Address</label><br>
    <textarea name="address" rows="4" columns="12">${ address }</textarea>
</p>
<p>
    <input type="submit" name="submit" value="Submit"/>
</p>
</form>
