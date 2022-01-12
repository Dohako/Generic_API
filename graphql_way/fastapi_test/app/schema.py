from datetime import date
import strawberry
from typing import List, Optional


@strawberry.type
class Fields:
    id: Optional[int] = None
    os: Optional[str] = None
    date: Optional[str] = None

@strawberry.input
class StringAtributes:
    _eq: Optional[str] = None
    _not: Optional[str] = None

@strawberry.input
class IntAttributes:
    _eq: Optional[int] = None

@strawberry.input
class DateAttributes:
    _eq: Optional[str] = None]

@strawberry.input
class WhereInput:
    os: Optional[StringAtributes] = None
    date: Optional[DateAttributes] = None

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
                 where: Optional[WhereInput] = None, 
                 order: Optional[OrderInput] = None) -> Data:
        print(where)
        print(order)
        a = Fields(id = 5)
        a.date = 'aaaaaaaaaaaaa'
        a.os = 'ios'
        return Data(fields=a)
