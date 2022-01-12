import strawberry
from typing import List, Optional


@strawberry.type
class Fields:
    id: Optional[int] = None
    os: Optional[str] = None
    date: Optional[str] = None

@strawberry.input
class OSInput:
    _eq: Optional[str] = None

@strawberry.input
class Where:
    os: Optional[OSInput] = None
    date: Optional[bool] = None

@strawberry.type
class Group:
    os: int
    date: int

@strawberry.input
class OrderInput:
    os: Optional[str] = None
    date: Optional[str] = None

@strawberry.type
class Data:
    fields: Optional[Fields] = None
    # group: Optional[Group]
    # order: Optional[Order]

@strawberry.type
class Query:
    @strawberry.field
    def get_data(self, 
                 where: Optional[Where] = None, 
                 order: Optional[OrderInput] = None) -> Data:
        print(where)
        print(order)
        a = Fields(id = 5)
        a.date = 'aaaaaaaaaaaaa'
        a.os = 'ios'
        return Data(fields=a)
