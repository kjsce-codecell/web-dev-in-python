# Django Database

## SQL

Structured Query Language, is a programming language that allows us to update and query databases.

### Databases

| origin   | destination | duration |
| -------- | ----------- | -------- |
| Mumbai   | Chennia     | 218      |
| Delhi    | Paris       | 430      |
| Istanbul | Tokyo       | 400      |
| Mumbai   | Delhi       | 243      |
| Delhi    | Dubai       | 329      |

### Cloumn Types

- TEXT: For strings of text (Ex. a person’s name)
- NUMERIC: A more general form of numeric data (Ex. A date or boolean value)
- INTEGER: Any non-decimal number (Ex. a person’s age)
- REAL: Any real number (Ex. a person’s weight)
- BLOB (Binary Large Object): Any other binary data that we may want to store in our database (Ex. an image)

### Tables

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

### INSERT

```sql
INSERT INTO flights
    (origin, destination, duration)
    VALUES ("Mumbai", "Chennia", 218);
INSERT INTO flights (origin, destination, duration) VALUES ("Delhi", "Paris", 430);
INSERT INTO flights (origin, destination, duration) VALUES ("Istanbul", "Tokyo", 400);
INSERT INTO flights (origin, destination, duration) VALUES ("Mumbai", "Delhi", 243);
INSERT INTO flights (origin, destination, duration) VALUES ("Delhi", "Dubai", 329);
```

### SELECT

```sql
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

### Functions

- AVERAGE
- COUNT
- MAX
- MIN
- SUM

chech out details and more [here](https://www.w3schools.com/sql/sql_count_avg_sum.asp)

### UPDATE

```sql
UPDATE flights
    SET duration = 430
    WHERE origin = "Mumbai"
    AND destination = "Delhi";
```

### DELETE

```sql
DELETE FROM flights WHERE destination = "Paris";
```

### Other Clauses

- `LIMIT`: Limits the number of results returned by a query
- `ORDER BY`: Orders the results based on a specified column
- `GROUP BY`: Groups results by a specified column
- `HAVING`: Allows for additional constraints based on the number of results

chech out details and more [here](https://www.w3schools.com/sql/sql_top.asp)

### Joining Tables
