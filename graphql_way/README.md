# GraphQL

As I know, GraphQL is made for situations like this.

This part is TBD for the moment.

[testing](http://localhost:5000/graphql)

## Stack

* fastapi

* GraphQL

* psycopg2 for psql

## Opinion

### PROS

* TBD

### CONS

* TBD

TBD

## Test order

* TBD

## Query examples

### First query

Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order. Hint:

``` sql
select channel, country, sum(impressions) as impressions, sum(clicks) as clicks 
from data 
where date < '2017-06-01' 
group by channel, country 
order by clicks desc;
```

```graphql
TBD
```

### Second query

Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

``` sql
select date, sum(installs) as installs
from data
where date > '2017-05-30' and os = 'ios'
group by date
order by date desc;
```

```graphql
TBD
```

### Third query

Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

```sql
select os, sum(revenue) as revenue
from data
where date = '2017-06-01' and country = 'US'
group by os
order by revenue desc;
```

```graphql
TBD
```

### Fourth query

Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.

```sql
select channel, cast(sum(spend) / sum(installs) as DECIMAL(10,4)) as CPI
from data
where country = 'CA'
group by channel
order by CPI desc;
```

```graphql
TBD
```
