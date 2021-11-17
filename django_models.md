# Django Models

## Creating our 1st Model

lets start by creating a new project `airline` and an app `flights`.

```bash
django-admin startproject airline
cd airline
python manage.py startapp flights
```

Now we’ll have to go through the process of adding an app as usual:

1. Add flights to the INSTALLED_APPS list in settings.py
2. Add a route for flights in urls.py:

```python
path('flights/', include("flights.urls")),
```

3. Create a `urls.py` file within the `flights` application. And fill it with standard urls.py imports and lists.

```python
from django.urls import path
from . import views

urlpatterns = []
```

Now instead of creating a `view` lets go to `models.py` and create a `Flight` model.

```python
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
```

1. In the first line, we create a new model that **extends** Django’s model class.
2. Below, we add fields for `origin`, `destination`, and `duration`. The first two are `Char Fields`, meaning they store strings, and the third is an `Integer Field`. These are just two of many [built-in Django Field classes](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#built-in-field-classes).
3. We specify maximum lengths of 64 for the two Character Fields. you can check the specifications available for a given field by checking the [documentation](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#built-in-field-classes).

## Migrations

After creating our very first `model`.

1. This command creates some Python files that will create or edit our database to be able to store what we have in our models. If you navigate to your migrations directory, you’ll notice a new file was created for us

```
python manage.py makemigrations
```

2. To apply these migrations to our database, we run the command

```
python manage.py migrate
```

Now, you’ll see some default **migrations** have been applied along with our own, and you’ll also notice that we now have a file called `db.sqlite3` in our project’s directory.

## Shell

```python shell
# Import our flight model
In [1]: from flights.models import Flight
# Create a new flight
In [2]: f = Flight(origin="Mumbai", destination="Chennai", duration=218)
# Instert that flight into our database
In [3]: f.save()
# Query for all flights stored in the database
In [4]: Flight.objects.all()
Out[4]: <QuerySet [<Flight: Flight object (1)>]>
```

When we query our database, we see that we get just one flight called `Flight object (1)`. This isn’t a very informative name, but we can fix that.

Inside `models.py`, we’ll define a `__str__` function that provides instructions for how to turn a `Flight` object into a `string`.

```python
def __str__(self):
    return f"{self.id}: {self.origin} to {self.destination}"
```

Now lets go back to our `shell`

```python shell
# import our Flight model
In [1]: from flights.models import Flight

# Create a variable called flights to store the results of a query
In [2]: flights = Flight.objects.all()

# Displaying all flights
In [3]: flights
Out[3]: <QuerySet [<Flight: 1: Mumbai to Chennai>]>

# Isolating just the first flight
In [4]: flight = flights.first()

# Printing flight information
In [5]: flight
Out[5]: <Flight: 1: Mumbai to Chennai>

# Display flight id
In [6]: flight.id
Out[6]: 1

# Display flight origin
In [7]: flight.origin
Out[7]: 'Mumbai'

# Display flight destination
In [8]: flight.destination
Out[8]: 'Chennai'

# Display flight duration
In [9]: flight.duration
Out[9]: 218
```

## Create other models

Now that we have a basic understaning of how models work let's create some more

```python
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```

We specify that the `origin` and `destination` fields are each [Foreign Keys](https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/), which means they refer to another object.

1. By entering `Airport` as our first argument, we are specifying the type of object this field refers to.

2. The next argument, `on_delete=models.CASCADE` gives instructions for what should happen if an airport is deleted. In this case, we specify that when an airport is deleted, all flights associated with it should also be deleted. There are several [other options](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ForeignKey.on_delete) in addition to `CASCADE`.

3. We provide a [related name](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ForeignKey.related_name), which gives us a way to search for all `flights` with a given `airport` as their `origin` or `destination`.

Every time we make changes in `models.py`, we have to `makemigrations` and then `migrate`.

```bash
# since our Mumbai to Chennai flight does not fit
# in our new schema we will need to delete it
python manage.py flush

# migrations
python manage.py makemigrations
python manage.py migrate
```

## Flights App

1. Inside `urls.py`

```python
urlpatterns = [
    path('', views.index, name="index"),
]
```

2. Inside `views.py`

```python
from django.shortcuts import render
from .models import Flight, Airport

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })
```

3. Lets create a `layout.html`

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Flights</title>
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
```

4. inside our `index.html`

<!-- prettier-ignore -->
```html
{% extends "flights/layout.html" %}

{% block body %}
    <h1>Flights:</h1>
    <ul>
        {% for flight in flights %}
            <li>Flight {{ flight.id }}: {{ flight.origin }} to {{ flight.destination }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

### Add some flights using the `shell`

## Django Admin

## Flight details page

## Many-to-Many Relationships

## Users
