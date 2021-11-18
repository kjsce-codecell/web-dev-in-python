# SQL

Structured Query Language, is a programming language that allows us to update and query databases.

## Databases

| origin   | destination | duration |
| -------- | ----------- | -------- |
| Mumbai   | Chennia     | 218      |
| Delhi    | Paris       | 430      |
| Istanbul | Tokyo       | 400      |
| Mumbai   | Delhi       | 243      |
| Delhi    | Dubai       | 329      |

## Cloumn Types

- `TEXT`: For strings of text (Ex. a person’s name)
- `NUMERIC`: A more general form of numeric data (Ex. A date or boolean value)
- `INTEGER`: Any non-decimal number (Ex. a person’s age)
- `REAL`: Any real number (Ex. a person’s weight)
- `BLOB` (Binary Large Object): Any other binary data that we may want to store in our database (Ex. an image)

## Tables

```sql
CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```

1. `id`: It is often helpful to have an number that allows us to uniquely identify each row in a table. Here we have specified that id is an integer, and also that it is our primary key, meaning it is our unique identifier. We have additionally specified that it will `AUTOINCREMENT`, which means we will not have to provide an id every time we add to the table because it will be done automatically.
2. `origin`: Here we’ve specified that this will be a text field, and by writing `NOT NULL` we have required that it have a value.
3. `destination`: Again we’ve specified that this will be a text field and prevented it from being `null`.
4. `duration`: Again this value cannot be `null`, but this time it is represented by an integer rather than as text.

We just saw the NOT NULL and PRIMARY KEY constraint when making a column, but there are several other constraints available to us:

- `CHECK`: Makes sure certain constraints are met before allowing a row to be added/modified
- `DEFAULT`: Provides a default value if no value is given
- `NOT NULL`: Makes sure a value is provided
- `PRIMARY` KEY: Indicates this is the primary way of searching for a row in the database
- `UNIQUE`: Ensures that no two rows have the same value in that column.

## INSERT

```sql
INSERT INTO flights
    (origin, destination, duration)
    VALUES ("Mumbai", "Chennia", 218);
INSERT INTO flights (origin, destination, duration) VALUES ("Delhi", "Paris", 430);
INSERT INTO flights (origin, destination, duration) VALUES ("Istanbul", "Tokyo", 400);
INSERT INTO flights (origin, destination, duration) VALUES ("Mumbai", "Delhi", 243);
INSERT INTO flights (origin, destination, duration) VALUES ("Delhi", "Dubai", 329);
```

## SELECT

```sql
-- Format data
.mode cloumns
.headers yes
-- FROM
SELECT * FROM flights;
SELECT origin, destination FROM flights;
-- WHERE
SELECT * FROM flights WHERE id = 3;
SELECT * FROM flights WHERE origin = "Mumbai";
-- AND & OR
SELECT * FROM flights WHERE duration > 400 AND destination = "Paris";
SELECT * FROM flights WHERE duration < 300 OR destination = "Delhi";
```

## Functions

- `AVERAGE`
- `COUNT`
- `MAX`
- `MIN`
- `SUM`

check out details and more [here](https://www.w3schools.com/sql/sql_count_avg_sum.asp)

## UPDATE

```sql
UPDATE flights
    SET duration = 430
    WHERE origin = "Mumbai"
    AND destination = "Delhi";
```

## DELETE

```sql
DELETE FROM flights WHERE destination = "Paris";
```

## Other Clauses

- `LIMIT`: Limits the number of results returned by a query
- `ORDER BY`: Orders the results based on a specified column
- `GROUP BY`: Groups results by a specified column
- `HAVING`: Allows for additional constraints based on the number of results

check out details and more [here](https://www.w3schools.com/sql/sql_top.asp)

## Joining Tables (Foreign Keys)

What if I wanted to save the airport code along with the airport city:

- one way to do so would be to just add more columns

| origin   | origin code | destination | destination code | duration |
| -------- | ----------- | ----------- | ---------------- | -------- |
| Mumbai   | BOM         | Chennia     | MAA              | 218      |
| Delhi    | DEL         | Paris       | CDG              | 430      |
| Istanbul | IST         | Tokyo       | HND              | 400      |
| Mumbai   | BOM         | Delhi       | DEL              | 243      |
| Delhi    | DEL         | Dubai       | DXB              | 329      |

- but that would make the table fairly wide
- there is also some **duplicate data**

One way to resolve this problem is to **seperate out data** into **seperate tables**
that just reference one another.

In this case I might just store all airport codes in a seperate table something similar to:

- Airports Table

| id  | code | city     |
| --- | ---- | -------- |
| 1   | BOM  | Mumbai   |
| 2   | DEL  | Delhi    |
| 3   | IST  | Istanbul |
| 4   | MAA  | Chennia  |
| 5   | CDG  | Paris    |
| 6   | HND  | Tokyo    |
| 7   | DXB  | Dubai    |

Now we have a table relating `codes` and `cities`, rather than storing an entire city name in our flights table,
it will save storage space if we’re able to just save the `id` of that `airport`.
Therefore, we should rewrite the flights table accordingly.
Since we’re using the `id` column of the airports table to populate `origin_id` and `destination_id`,
we call those values [Foreign Keys](https://www.w3schools.com/sql/sql_foreignkey.asp)

- Flights Table

| id  | origin_id | destination_id | duration |
| --- | --------- | -------------- | -------- |
| 1   | 1         | 4              | 218      |
| 2   | 2         | 5              | 430      |
| 3   | 3         | 6              | 400      |
| 4   | 1         | 2              | 243      |
| 5   | 2         | 7              | 329      |

In addition to flights and airports, an airline might also want to store data about its passengers

- Passengers Table (Unoptimized)

| id  | name     | flight_id |
| --- | -------- | --------- |
| 1   | Neelansh | 1         |
| 2   | Devansh  | 1         |
| 3   | Nishit   | 2         |
| 4   | Kevin    | 4         |
| 5   | Jay      | 2         |
| 6   | Tanvi    | 5         |

We can do even better than this though,
as the same person may be on more than one flight.
To account for this, we can create a people table that stores the passenger's name,
and a passengers table that pairs people with flights

- People Table

| id  | name     |
| --- | -------- |
| 1   | Neelansh |
| 2   | Devansh  |
| 3   | Nishit   |
| 4   | Kevin    |
| 5   | Jay      |
| 6   | Tanvi    |

- Passengers Table (Optimized)

| person_id | flight_id |
| --------- | --------- |
| 1         | 1         |
| 2         | 2         |
| 2         | 3         |
| 3         | 1         |
| 4         | 4         |
| 5         | 3         |
| 6         | 5         |

because in this case a single person can be on many flights and a single flight can have many people, we call the relationship between `flights` and `people` a **Many to Many** relationship. The passengers table that connects the two is known as an **association table**.

## JOIN query

let’s say we want to find the origin, destination, and first name of every trip a passenger is taking.

Also for simplicity in this table, we’re going to be using the unoptimized passengers table that includes the flight id, first name, and last name.

```sql
SELECT name, origin, destination
FROM flights JOIN passengers
ON passengers.flight_id = flights.id;
```

## SQL Vulnerabilities

1. SQL Injection.

If this were your query to login a customer

```sql
SELECT * FROM users
WHERE username = "kevin" AND password = "876234";
```

A hacker might type `kevin" --` as a `username`

It turns out that -- stands for a comment in SQL, meaning the query would look like:

```sql
SELECT * FROM users
WHERE username = "harry"--" AND password = "12345";
```

To solve this problem, we can use:

- Escape characters to make sure SQL treats the input as plain text and not as SQL code.
- An abstraction layer on top of SQL which includes its own escape sequence, so we don’t have to write SQL queries ourselves.

2. Race Condition.

A race condition is a situation that occurs when multiple queries to a database occur simultaneously. When these are not adequately handled, problems can arise in the precise times that databases are updated.

For example, let’s say I have Rs. 15,000 in my bank account. A race condition could occur if I log into my bank account on both my phone and my laptop, and attempt to withdraw Rs. 10,000 on each device. If the bank’s software developers did not deal with race conditions correctly, then I may be able to withdraw Rs. 20,000 from an account with only Rs. 15,000 in it.

One potential solution for this problem would be locking the database. We could not allow any other interaction with the database until one transaction has been completed.

In the bank example, after clicking navigating to the "Make a Withdrawl" page on my computer, the bank might not allow me to navigate to that page on my phone.

# Credits

#### `CS50 Web` - week 4 https://cs50.harvard.edu/web/2020/weeks/4/
