# JSON WAY

Just a little bit more complicated than url way and maybe a little safier(not guaranteed).

In that way fast API is used for creating endpoit.

Json format example is also here.

## Stack

* fastapi

* uvicorn

* json

* psycopg2 for psql

## Opinion

### PROS

* this way we can create stable connection inside of projects for different clients

* more control of incoming data and easy to understand data structure

### CONS

* sending json in post is not so easy to repeat for quick testing

I find this way best of three. It's not only possible to connect any front/back to that solution,
but also, as I think, this is the way it usualy created generic API's

## Test order

* activate venv

* setup requirements

* start script (`python path_to_folder\json_way\backend\main.py`)

[

* go to [link](http://localhost:8000/docs#) to see fastapi's swagger for testing

* send json to get_info post method

]

OR

[

* send post request with json in body to [link](http://localhost:8000/get_info)

]

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

```json
{
    "select": [
        "channel",
        "country",
        "SUM impressions",
        "SUM clicks"
    ],
    "filter": [
        "date < '2017-06-01'"
    ],
    "group by": [
        "channel",
        "country"
    ],
    "order by": [
        "clicks",
        "desc"
    ]
}
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

```json
{
    "select": [
        "date",
        "SUM installs"
    ],
    "filter": [
        "date > '2017-05-30'",
        "and os = 'ios'"
    ],
    "group by": [
        "date"
    ],
    "order by": [
        "date",
        "desc"
    ]
}
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

```json
{
    "select": [
        "os",
        "SUM revenue"
    ],
    "filter": [
        "date = '2017-06-01'",
        "and country = 'US'"
    ],
    "group by": [
        "os"
    ],
    "order by": [
        "revenue",
        "desc"
    ]
}
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

```json
{
    "select": [
        "channel",
        "CAST CPI = SUM spend / SUM installs"
    ],
    "filter": [
        "country = 'CA'"
    ],
    "group by": [
        "channel"
    ],
    "order by": [
        "CPI",
        "desc"
    ]
}
```
