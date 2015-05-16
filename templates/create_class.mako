<%inherit file='base.mako' />

<h2>Create class</h2>

% if errors:
<ul>
    % for e in errors:
    <li><font color=red>${ e }</font></li>
    % endfor
</ul>
% endif

<form method="post" action="${ request.path }">
    <p>
        <label for="name">Class name</label><br>
        <input type="text" name="name" value="${ name }">
    </p>
    <input type="submit" name="submit" value="Submit"/>
</form>
