# Django Authentication

## Users

Lets discuss the idea of authentication, or allowing users to log in and out of a website.

Fortunately, Django makes this very easy for us, so let’s go through an example of how we would do this. We’ll start by creating a new app called users.

Here we’ll go through all the normal steps of creating a new app,

1. create project

```bash
django-admin startproject auth_app
cd auth_app
python manage.py startapp users
```

2. Add `users` in `INSTALLED_APPS`

3. In `auth_app/urls.py`

```python
path('', include('users.urls')),
```

4. In our new `urls.py` file, we’ll add a few more routes:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
```

1. create `layout.html`

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Authentication</title>
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>
```

2. create `login.html`

<!-- prettier-ignore -->
```html
{% extends "users/layout.html" %}

{% block body %}
    {% if message %}
        <div>{{ message }}</div>
    {% endif %}

    <form action="{% url 'login' %}" method="post">
        {% csrf_token %}
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>
{% endblock %}
```

3. `views.py`

```python
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls import reverse

def index(request):
    # If no user is signed in, return to login page:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    return render(request, "users/login.html")

def logout_view(request):
    # Pass is a simple way to tell python to do nothing.
    pass
```

Next, we can head to the admin site and add some users.

```bash
python manage.py migrate
python manage.py createsuperuser
```

After doing that, we’ll go back to `views.py` and update our `login_view` function to handle a `POST` request with a username and password:

```python
# Additional imports we'll need:
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "users/login.html")
```

4. We’ll create the `user.html` file that the index function renders when a user is authenticated

<!-- prettier-ignore -->
```html
{% extends "users/layout.html" %}

{% block body %}
    <h1>Welcome, {{ request.user.first_name }}</h1>
    <ul>
        <li>Username: {{ request.user.username }}</li>
        <li>Email: {{ request.user.email }}</li>
    </ul>

    <a href="{% url 'logout' %}">Log Out</a>
{% endblock %}
```

5. To allow the user to log out, we’ll update the `logout_view` function so that it uses Django’s built-in logout function

```python
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
                "message": "Logged Out"
            })
```

# Credits

#### `CS50 Web` - week 4 https://cs50.harvard.edu/web/2020/weeks/4/
