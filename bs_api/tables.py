from piccolo.table import Table
from piccolo.columns import Varchar, Integer
from datetime import date

class Expense(Table):
    amount = Integer()
    description = Varchar()

