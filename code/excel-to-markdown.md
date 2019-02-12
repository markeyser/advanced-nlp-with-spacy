# SQL Cheat Sheet

The following notes are a summary of the Book: "[Getting Started with SQL](https://www.amazon.com/gp/product/B01BO7HPNC?pf_rd_p=c2945051-950f-485c-b4df-15aac5223b10&pf_rd_r=370SHTH33B60AWHYEXG2)"

![](https://books.google.com/books/content?id=RHOOCwAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&imgtk=AFLRE72OKcJeQSX2mvpX9r6MMkHZjlwqyMIPstZq0RLMxNOKdXtY_cV3kKTn2rXtpwLSg_Au5ZDum0t1XsaPNgWfTArHCx4Pfp4ZVrEI01p5zMOvpy7h7-75m7DfHBvxYz7cDH93mcWA)

## `SELECT` statement

`PRODUCT` table: `PRODUCT_ID`, `DESCRIPTION`, `PRICE`
`CUSTOMER` table: `CUSTOMER_ID`, `NAME`, `REGION`, `STREET_ADDRESS`, `CITY`, `STATE`, `ZIP`

Pull all the columns from the `CUSTOMER` table:
```sql
select *
from customer;
```
Pick `CUSTOMER_ID` and `NAME` from the `CUSTOMER` table:
```sql
SELECT customer_id, name
FROM customer;
```
Generate a calculated column called `TAXED_PRICE` that is 7% higher than `PRICE`. We used an alias to give name to this expression:
```sql
SELECT product_id, description, price,
price * 1.07 AS taxed_price
FROM product;
```
We can also uses aliases to apply a new name to an existing column within the query.
```sql
SELECT product_id, description, price AS untaxed_price,
price * 1.07 AS taxed_price
FROM product;
```
Using the `round()` function to round the `TAXED_PRICE` to two decimals.
```sql
SELECT product_id, description, price,
round(price * 1.07, 2) AS taxed_price
FROM product;
```
Concatenate the `CITY` and `STATE` fields from the `CUSTOMER` table as well as put a comma and space between them to create a `LOCATION` value
```sql
SELECT name, city || ',' || state AS location
FROM customer;
```
You can even concatenate several fields into a single `SHIP_ADDRESS` value. Concatenation should work with any data type (numbers, dates, etc.) and treat it as
text when merging. The `ZIP` field shown here is a number, but it was implicitly converted
to text during concatenation. Many database platforms use double pipes (``||``) to concatenate, but
MySQL and some others require using a `CONCAT()` function.
```sql
SELECT NAME,
STREET_ADDRESS || ' ' || CITY || ', ' || STATE || ' ' || ZIP
AS SHIP_ADDRESS
FROM CUSTOMER;
```
## `WHERE` clause
### Using `WHERE` on Numbers
Get back records where the YEAR field equals 2010
```SQL
SELECT *
FROM station_data
WHERE year = 2010;
```
Get everything but 2010
```sql
SELECT *
FROM station_data
WHERE year != 2010;
```
The same as above
```SQL
SELECT *
FROM station_data
WHERE year <> 2010;
```
Now 2005 and 2010 are included in the range.
```SQL
SELECT *
FROM station_data
WHERE year BETWEEN 2005 AND 2010;
```
### `AND`, `OR`, and `IN` Statements
A `BETWEEN` can alternatively be expressed using greater than or equal to and less than
or equal to expressions and an `AND` statement. It is a little more verbose, but it demonstrates
we can use two conditions with an `AND`. In this case, the year must be greater
than or equal to 2005 and less than or equal to 2010
```SQL
SELECT *
FROM station_data
WHERE year >= 2005 AND year <= 2010;
```
If we wanted everything between 2005 and 2010 exclusively—i.e., not including those
two years—we would just get rid of the `=` characters. Only 2006, 2007, 2008, and 2009
would then qualify
```SQL
SELECT *
FROM station_data
WHERE year > 2005 AND year < 2010;
```
We also have the option of using `OR`. In an `OR` statement, at least one of the criteria
must be true for the record to qualify. If we wanted only records with months 3, 6, 9,
or 12, we could use an `OR` to accomplish that
```SQL
SELECT *
FROM station_data
WHERE MONTH = 3 OR MONTH = 6 OR MONTH = 9 OR MONTH = 12;
```
This is a little verbose. A more efficient way to accomplish this is using an `IN` statement
to provide valid list of values
```SQL
SELECT *
FROM station_data
WHERE MONTH IN (3,6,9,12);
```
If we wanted everything except 3, 6, 9, and 12, we could use NOT IN
```SQL
SELECT *
FROM station_data
WHERE MONTH NOT IN (3,6,9,12);
```
You can use other math expressions in your WHERE statements too. Earlier, we were
trying to filter on months 3, 6, 9, and 12. If you wanted only months divisible by 3
(the “quarter” months), you could use the modulus operator (`%`). The modulus is similar
to the division operator (`/`), but it returns the remainder instead of the quotient. A
remainder of 0 means there is no remainder at all, so you can leverage this logic by
looking for a remainder of 0 with modulus 3.
In English, this means “give me all months where dividing by 3 gives me a remainder
of 0.
Oracle does not support the modulus operator. It instead uses the
MOD() function.
```SQL
SELECT *
FROM station_data
WHERE MONTH % 3 = 0;
```
### Using `WHERE` on Booleans
Booleans are true/false values. In the database world, typically false is expressed as 0 and true is expressed as 1. Some database platforms (like MySQL) allow you to
implicitly use the words true and false to qualify, as shown here
```SQL
SELECT *
FROM station_data
WHERE tornado = true AND hail = true;
```
SQLite, however, does not support this. It expects you to explicitly use 1 for true and
0 for false. If you wanted all records where there was tornado and hail, you would run
this statement:
```SQL
SELECT *
FROM station_data
WHERE tornado = 1 AND hail = 1;
```
If you are looking for just true values, you do not even have to use the = 1 expression.
Because the fields are already Boolean (behind the scenes, every WHERE condition
boils down to a Boolean expression), they inherently qualify by themselves. Hence,
you can achieve the same results by running the following query
```SQL
SELECT *
FROM station_data
WHERE tornado AND hail;
```
However, qualifying for false conditions needs to be explicit. To get all records with
no tornado but with hail, run this query
```SQL
SELECT *
FROM station_data
WHERE tornado = 0 AND hail = 1;
```
You can also use the NOT keyword to qualify tornado as false
```SQL
SELECT *
FROM station_data
WHERE NOT tornado AND hail;
```
### Handling `NULL`
You may have noticed that some columns, such as station_pressure and snow_depth, have null values (Figure 5-3). A null is a value that has no value. It is the complete absence of any content. It is a vacuous state. In layman’s terms, it is blank.

Null values cannot be determined with an =. You need to use the `IS NULL` or `IS NOT
NULL` statements to identify null values. So, to get all records with no recorded
`snow_depth`, you could run this query
```SQL
SELECT *
FROM station_data
WHERE snow_depth IS NULL;
```
Do not confuse nulls with empty text, which is two single quotes
with nothing in them (i.e., ''). This also applies to whitespace text
(i.e., ' '). These will be treated as values and never will be considered
null. A null is definitely not the same as 0 either, because 0 is a
value, whereas null is an absence of a value.

Nulls can be very annoying to handle when composing WHERE statements. If you wanted to query all records where precipitation is less than 0.5, you could write
this statement
```SQL
SELECT *
FROM station_data
WHERE precipitation <= 0.5;
```
But have you considered the null values? What if for this query you wanted nulls to be included? Because null is not 0 or any number, it will not qualify. Nulls rarely qualify
with anything and almost always get filtered out in a WHERE unless you explicitly
handle them. So you have to use an OR to include nulls
```SQL
SELECT *
FROM station_data
WHERE precipitation IS NULL OR precipitation <= 0.5;
```
A more elegant way of handling null values is to use the coalesce() function, which
will turn a possibly null value into a specified default value if it is null. Otherwise, it
will leave the value as is. The first argument is the possibly null value, and the second
is the value to use if it is null. So if we wanted all nulls to be treated as 0 within our
condition, we could coalesce() the precipitation field to convert null to 0
```SQL
SELECT *
FROM station_data
WHERE coalesce(precipitation, 0) <= 0.5;
```
Like any function, a coalesce() can be used in the SELECT statement too, and not just
the WHERE. This is helpful if you want to pretty up a report and not have null values
displayed, but rather have some placeholder—for example, 0, “N/A” or “None”—
which is more meaningful to most people
```SQL
SELECT report_code, coalesce(precipitation, 0) AS rainfall
FROM station_data;
```
### Grouping Conditions
When you start chaining AND and OR together, it is good to group them deliberately.
You need to make sure that you organize each set of conditions between each OR in a
way that groups related conditions

Say you were looking for sleet or snow conditions. For sleet to happen, there must be rain and a temperature less than or equal to 32 degrees Fahrenheit. You can test for that sleet condition or a snow depth greater than 0, as shown here
```SQL
SELECT *
FROM station_data
WHERE rain = 1 AND temperature <= 32 OR snow_depth > 0;
```
But there is one possible problem here. While this technically works, there is a degree
of ambiguity that we were lucky SQLite interpreted correctly. The reason is due to the
unclear question of “What conditions belong to the AND and what conditions belong
to the OR?” The SQL interpreter could derail quickly and incorrectly interpret that we
are looking for rain AND another condition where either the temperature is below 32
OR the snow depth is greater than 0. The semantics are not clear, and in more complicated
SQL this could confuse not only people but also the machine. This is why it is better to explicitly group conditions in parentheses
```SQL
SELECT *
FROM station_data
WHERE (rain = 1 AND temperature <= 32)
OR snow_depth > 0
```
## `GROUP BY` and `ORDER BY`
### Grouping Records
First, perform the simplest aggregation: count the number of records in a table. The `COUNT(*)`` means to count the records
```SQL
SELECT COUNT(*) AS record_count
FROM station_data;
```
The `COUNT(*)` means to count the records. We can also use this in combination with
other SQL operations, like WHERE. To count the number of records where a tornado
was present, input the following
```SQL
SELECT COUNT(*) AS record_count
FROM station_data
WHERE tornado = 1;
```
We identified 3,000 records with tornadoes present. But what if we wanted to separate
the count by year? We can do that too with this query
```SQL
SELECT year, COUNT(*) AS record_count  
FROM station_data
WHERE tornado = 1
GROUP BY year;
```
We can slice this data on more than one field. If we wanted a count by year and
month, we could group on the month field as well
```SQL
SELECT year, month, COUNT(*) AS record_count
FROM station_data
WHERE tornado = 1
GROUP BY year, month;
```
Alternatively, we can use ordinal positions instead of specifying the columns in the
GROUP BY. The ordinal positions correspond to each item’s numeric position in the
SELECT statement
```SQL
SELECT year, month, COUNT(*) AS record_count
FROM station_data
WHERE tornado = 1
GROUP BY 1, 2;
```
Note that not all platforms support ordinal positions. With Oracle and SQL Server,
for example, you will have to rewrite the entire column name or expression in the
GROUP BY.
### Ordering Records
Notice that the month column is not in a natural sort we would expect. This is a good
time to bring up the ORDER BY operator, which you can put at the end of a SQL statement (after any WHERE and GROUP BY). If you wanted to sort by year, and then month, you could just add this command
```SQL
SELECT year, month, COUNT(*) AS record_count
FROM station_data
WHERE tornado = 1
GROUP BY year, month
ORDER BY year, month;
```
However, you are probably more interested in recent data and would like it at the top.
By default, sorting is done with the ASC operator, which orders the data in ascending
order. If you want to sort in descending order instead, apply the DESC operator to the
ordering of year to make more recent records appear at the top of the results
```SQL
SELECT year, month, COUNT(*) AS record_count
FROM station_data
WHERE tornado = 1
GROUP BY year, month
ORDER BY year DESC, month
```
 ### Aggregate Functions
 We already used the `COUNT(*)` function to count records. But there are other aggregation
functions, including `SUM()`, `MIN()`, `MAX()`, and `AVG()`. We can use aggregation
functions on a specific column to perform some sort of calculation on it.

But first let’s look at another way to use `COUNT()`. The `COUNT()` function can be used
for a purpose other than simply counting records. If you specify a column instead of
an asterisk, it will count the number of non-null values in that column. For instance,
we can take a count of snow_depth recordings, which will count the number of non null
values

Aggregate functions such as `COUNT()`, `SUM()`, `AVG()`, `MIN()`, and
`MAX()` will never include null values in their calculations. Only
non-null values will be considered.
