<%inherit file='base.mako' />

% if errors:
<ul>
    % for e in errors:
    <li>${ e }</li>
    % endfor
</ul>
% endif

<form method="post" action="${ request.path }">

<h2>Interventions</h2>

<p>Please enter at most 300 characters about the intervention that the student will undergo.</p>
    <textarea style="width:500px"; name="content" rows="10" columns="200">${ content}</textarea>
    <br/>
    <input type="submit" name="submit" value="Submit"/>
</form>