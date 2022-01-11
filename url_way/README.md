# URL WAY

Simpliest and CHARGE way is to parse direct url request for arguments and then make a request to db.

Currently this way is blocked, but it will be completed.

## First query

Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order. Hint:

``` sql
select channel, country, sum(impressions) as impressions, sum(clicks) as clicks 
from data 
where date < '2017-06-01' 
group by channel, country 
order by clicks desc;
```

goes for [first query](http://127.0.0.1:5000/expose_data?show:channel,country,sum_impressions_as_impressions,sum_clicks&filter:date_<_*2017-06-01*&group:channel,country&order:clicks-desc)

## Second query

Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

``` sql
select date, sum(installs) as installs
from data
where date > '2017-05-30' and os = 'ios'
group by date
order by date desc;
```

goes for [second query](http://127.0.0.1:5000/expose_data?show:date,sum_installs&filter:date_>_*2017-05-30*_and_os_=_*ios*&group:date&order:date-desc)

## Third query

Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

```sql
select os, sum(revenue) as revenue
from data
where date = '2017-06-01' and country = 'US'
group by os
order by revenue desc;
```

goes for [third query](http://127.0.0.1:5000/expose_data?show:os,sum_revenue&filter:date_=_*2017-06-01*_and_country_=_*US*&group:os&order:revenue-desc)

## Fourth query

Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.

```sql
select channel, cast(sum(spend) / sum(installs) as DECIMAL(10,4)) as CPI
from data
where country = 'CA'
group by channel
order by CPI desc;
```

goes for [fourth query](http://127.0.0.1:5000/expose_data?show:channel,cast_cpi=sum_spend^sum_installs&filter:country_=_*US*&group:channel&order:cpi-desc)
