from abc import ABC, abstractmethod
from typing import Callable, Any


class _Column(str):
    pass


class _Row(dict[_Column, Any]):
    pass


class Table:
    """
    a class for managing the table data.
    """


    def __init__(self, data: list[_Row], columns: list[str]) -> None:
        """
        store the data.

        <code>data: list[_Row]:</code> the data of the table.<br>
        <code>columns: list of strings:</code> the columns of the table.

        <code>return: None. </code>
        """

        self.data = data
        self.length = len(data)
        self.columns = columns

    
    def get(self, row: int, column: str | None = None) -> dict[_Column, Any] | Any | None:
        """
        get the data of the given column.

        <code>column: string:</code> the column to get.

        <code>return: list: </code> the data of the column.
        """
        return self.data[row][column] if column in self.data[row] else None if column else self.data[row] if row < len(self.data) else None


class ReturnedSqlType:
    """
    a class for managing the returned data from the databse.
    """


    def __init__(self, sqlres: list[_Row], rowcount: int, close: Callable, columns: list[str]) -> None:
        """
        store the data.
        
        <code>sqlres: list of dictionarys:</code> the data itself.<br>
        sqlres is build like this:
        [row1, row2, ...]
        each row is:
        {column1: value, column2: value, ...}<br>
        <code>rowcount: integer:</code> the rowcount.<br>
        <code>close: callable:</code> a disconnect function.<br>
        <code>columns: list of strings:</code> the columns of the table.<br>
        
        <code>return: None. </code>
        """
        self.sqlres = Table(sqlres, columns)
        self.rowcount = rowcount
        self.close = close


    def __enter__(self):
        return self


    def __exit__(self, *exc) -> None:
        self.close()


class ConnectionPoolInterface(ABC):
    """
    an interface for the ConnectionPool class.
    """
    @abstractmethod
    def _connect(self):
        pass


    @abstractmethod
    def _disconnect(self):
        pass

    
    @abstractmethod
    def runsql(self, sql: str):
        pass


    @abstractmethod
    def select(self, sql: str) -> ReturnedSqlType:
        pass
