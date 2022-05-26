from piccolo.table import Table
from piccolo.columns import Varchar


class Task(Table):
    """
    An example table.
    """

    name = Varchar()
