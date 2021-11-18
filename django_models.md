# Django Models

## Creating our 1st Model

lets start by creating a new project `airline` and an app `flights`.

```bash
django-admin startproject airline
cd airline
python manage.py startapp flights
```

Now we’ll have to go through the process of adding an app as usual:

1. Add flights to the `INSTALLED_APPS` list in `settings.py`
2. Add a route for flights in `urls.py`:

```python
path('flights/', include("flights.urls")),
```

3. Create a `urls.py` file within the `flights` application. And fill it with standard urls.py imports and lists.

```python
from django.urls import path
from . import views

urlpatterns = []
```

Now before creating a `view` lets go to `models.py` and create a `Flight` model.

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

### Add some flights using the shell

```python
# Import all models
In [1]: from flights.models import *

# Create some new airports
In [2]: bom = Airport(code="BOM", city="Mumbai")
In [3]: delhi = Airport(code="DEL", city="Delhi")
In [4]: ist = Airport(code="IST", city="Istanbul")
In [5]: maa = Airport(code="MAA", city="Chennia")

# Save the airports to the database
In [6]: bom.save()
In [7]: delhi.save()
In [8]: ist.save()
In [9]: maa.save()

# Add a flight and save it to the database
f = Flight(origin=bom, destination=delhi, duration=218)
f.save()

# Display some info about the flight
In [10]: f
Out[10]: <Flight: 1: Mumbai (BOM) to Delhi (DEL)>
In [11]: f.origin
Out[11]: <Airport: Mumbai (BOM)>

# Using the related name to query by airport of arrival:
In [12]: delhi.arrivals.all()
Out[12]: <QuerySet [<Flight: 1: Mumbai (BOM) to Delhi (DEL)>]>
```

## Django Admin

Django comes with a default admin interface that allows us to do create, read, update and delete our data more easily.

1. We must first create an administrative user

```bash
python manage.py createsuperuser
```

2. Now, we must add our models to the admin application by entering the admin.py file within our app

```python
from django.contrib import admin
from .models import Flight, Airport

# Register your models here.
admin.site.register(Flight)
admin.site.register(Airport)
```

## Flight details page

Lets add the ability to click on a flight to get more information about it.

1. To do this, let’s create a URL path that includes the id of a flight:

```python
path("<int:flight_id>", views.flight, name="flight")
```

2. `views.py` we will create a `flight` function that takes in a flight id and renders a new html page

```python
def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight
    })
```

3. create a template to display this flight information with a link back to the home pages. `flight.html`

<!-- prettier-ignore -->
```html
{% extends "flights/layout.html" %}

{% block body %}
    <h1>Flight {{ flight.id }}</h1>
    <ul>
        <li>Origin: {{ flight.origin }}</li>
        <li>Destination: {{ flight.destination }}</li>
        <li>Duration: {{ flight.duration }} minutes</li>
    </ul>
    <a href="{% url 'index' %}">All Flights</a>
{% endblock %}
```

4. Finally, we need to add the ability to link from one page to another, so we’ll modify our index page to include links. `index.html`

<!-- prettier-ignore -->
```html
{% extends "flights/layout.html" %}

{% block body %}
    <h1>Flights:</h1>
    <ul>
        {% for flight in flights %}
            <li>
                <a href="{% url 'flight' flight.id %}">
                    Flight {{ flight.id }}
                </a>: {{ flight.origin }} to {{ flight.destination }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

## Many-to-Many Relationships

1. Lets create a `Passenger` model

```python
class Passenger(models.Model):
    name = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.name}"
```

- `Passengers` have a **Many to Many** relationship with `flights`, which we describe in Django using the `ManyToManyField`.
- The first argument in this field is the class of objects that this one is related to.
- We have provided the argument `blank=True` which means a passenger can have no flights
- We have added a `related_name` that serves the same purpose as it did earlier: it will allow us to find all passengers on a given flight.

To actually make these changes,

1. we must `makemigrations` and `migrate`.

```bash
python manage.py makemigrations
python manage.py migrate
```

2. We can then register the `Passenger` model in `admin.py`.

```python
admin.site.register(Passenger)
```

### Let’s update our flight page so that it displays all passengers on a flight.

1. Visit `views.py` and update our flight view

```python
def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers
    })
```

2. Add a list of passengers to our `flight.html`

<!-- prettier-ignore -->
```html
<h2>Passengers:</h2>
<ul>
    {% for passenger in passengers %}
        <li>{{ passenger }}</li>
    {% empty %}
        <li>No Passengers.</li>
    {% endfor %}
</ul>
```

### Let’s work on giving visitors to our site the ability to book a flight.

1. `urls.py`

```python
path("<int:flight_id>/book", views.book, name="book")
```

2. `views.py`

```python
from django.http.response import HttpResponseRedirect
from django.urls import reverse

def book(request, flight_id):

    # For a post request, add a new flight
    if request.method == "POST":

        # Accessing the flight
        flight = Flight.objects.get(pk=flight_id)

        # Finding the passenger id from the submitted form data
        passenger_id = int(request.POST["passenger"])

        # Finding the passenger based on the id
        passenger = Passenger.objects.get(pk=passenger_id)

        # Add passenger to the flight
        passenger.flights.add(flight)

        # Redirect user to flight page
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
```

3. we’ll add some context to our flight template so that the page has access to everyone who is not currently a passenger on the flight using Django’s ability to exclude certain objects from a query:

```python
def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers
    })
```

4. we’ll add a form to our flight page’s HTML using a select input field. `flight.html`

<!-- prettier-ignore -->
```html
<form action="{% url 'book' flight.id %}" method="post">
    {% csrf_token %}
    <select name="passenger" id="">
        {% for passenger in non_passengers %}
            <option value="{{ passenger.id }}">{{ passenger }}</option>
        {% endfor %}
    </select>
    <input type="submit">
</form>
```

# Credits

#### `CS50 Web` - week 4 https://cs50.harvard.edu/web/2020/weeks/4/
