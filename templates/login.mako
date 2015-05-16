<%inherit file='logo.mako' />

% if failed_attempt:
<p><font color="red">Invalid credentials, try again.</font></p>
% endif
<form method="post" action="${ request.path }">
    <p>
        <label for="login"><b>Login</b></label><br>
        <input type="text" name="login" value="${ login }">
    </p>
    <p>
        <label for="passwd"><b>Password</b></label><br>
        <input type="password" name="passwd">
    </p>
    <input type="hidden" name="next" value="${ next }">
    <input type="submit" name="submit">
</form>

