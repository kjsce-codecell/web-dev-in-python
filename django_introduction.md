# Django Introduction

## Installation

- Note: it is recommended that we use virtual environments
- make sure you have `python3` or above and `pip` installed on your machine

- vitual environment

```bash
virtualenv ./virt             # unix
virtualenv %HOMEPATH%\virt    # windows

source ./virt/bin/activate          # unix
%HOMEPATH%\virt\Scripts\activate    # windows
```

- install `Django` using pip

```bash
pip3 install Django
```

- Go through the steps of creating a new Django project:

```bash
django-admin startproject introduction     # create a number of starter files for our project
cd introduction                            # navigate into your new project’s directory
python manage.py runserver                 # run your server
```

- Create app

```bash
python manage.py startapp hello
```

- Add `<APP_NAME>` to `INSTALLED_APPS` in `settings.py`

## Create our very first view

1. In your project's `urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include("hello.urls"))
]
```

2. create a new `urls.py` in your app

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index")
]
```

3. In your app's `views.py`

```python
from django.http.response import HttpResponse

def index(request):
    return HttpResponse("Hello, World")
```

## Hello from url

- main `urls.py`

```python
path('hello/', include('hello.urls'))
```

- app's `urls.py`

```python
path("<str:name>", views.greet, name="greet")
```

- app's `views.py`

```python
def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}")
```

## Django Templates

1. In your app's directory create a new folder `templates/APP_NAME`

2. Inside it create a new file `index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Hello</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```

3. In your `views.py`

```python
def index(request):
    return render(request, "hello/index.html")
```

## Passing params to template

1. `views.py`

```python
def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })
```

2. `greet.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Hello</title>
  </head>
  <body>
    <h1>Hello, {{ name }}!</h1>
  </body>
</html>
```

## Conditionals in template

1. lets create a new app

```bash
python manage.py startapp isitchrismas
```

2. Edit `settings.py`, adding `isitchrismas` as one of our `INSTALLED_APPS`

```pyton
path('isitchrismas/', include("isitchrismas.urls"))
```

3. Create another `urls.py` file within our new app’s directory, and update it to include a path.

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

4. `views.py`

```python
def index(request):
    now = datetime.datetime.now()
    return render(request, "christmas/index.html", {
        "christmas": now.month == 12 and now.day == 25
    })
```

5. `index.html`

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Is It Christmas?</title>
  </head>
  <body>
    {% if christmas %}
        <h1>YES</h1>
    {% else %}
        <h1>NO</h1>
    {% endif %}
  </body>
</html>
```

# Credits

#### `CS50 Web` - week 3 https://cs50.harvard.edu/web/2020/weeks/3/
