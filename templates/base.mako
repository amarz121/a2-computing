<%inherit file='logo.mako' />

<p><a href="${ request.route_url('logout') }">Logout</a></p>

<body>
        ${ next.body() }
</body>
