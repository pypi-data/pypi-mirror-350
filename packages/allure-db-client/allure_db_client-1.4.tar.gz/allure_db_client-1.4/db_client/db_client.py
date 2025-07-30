from __future__ import annotations

from typing import Any

from psycopg import Connection


class DBClient:
    """
    A database client for performing SQL operations.

    This client uses psycopg to connect to a PostgreSQL database and execute SQL queries. It provides various methods
    for executing queries and fetching results in different formats. It also integrates with Allure for logging
    queries and results, which is helpful for debugging and testing.

    Attributes:
        connection_string (str): A string used to connect to the database.

    Methods:
        get_list: Fetches the first column of each row from a query result as a list.
        get_dict: Fetches the first two columns of each row from a query result as a dictionary.
        select_all: Executes a query and fetches all rows.
        get_first_value: Fetches the first column of the first row from a query result.
        get_first_row: Fetches the first row from a query result.
        execute: Executes a given SQL command without returning any result.
        __enter__: Initiates a database connection upon entering a context.
        __exit__: Closes the database connection upon exiting a context.
    """

    def __init__(self, connection_string: str, with_allure: bool = True) -> None:
        """
        Initializes the DBClient with a given connection string.

        Args:
            connection_string (str): The database connection string.
        """
        self.connection_string = connection_string
        self.with_allure = with_allure

    def _execute(self, query: str, params: dict[str, Any], fetchall: bool) -> Any:
        """
        Execute a SQL query using the provided parameters and return the result.

        This method executes a SQL query on the database, using a cursor attached to the current database session.
        It also logs the query and its result for debugging and tracking purposes using the Allure framework.

        Parameters:
        query (str): The SQL query to be executed.
        params (dict[str, Any]): A dictionary containing the parameters to be used in the SQL query. These parameters
                                 are used to safely inject values into the SQL query, preventing SQL injection.
        fetchall (bool): A flag to determine whether to fetch all rows or just one. If True, fetches all rows,
                         otherwise fetches only the first row.

        Returns:
        Any: The result of the executed SQL query. Returns all fetched rows if `fetchall` is True, otherwise returns
             a single row.

        Note:
        The method uses Allure for logging purposes. It attaches the SQL query and its result to the Allure report for
        better visibility and debugging. This can be particularly useful in testing environments for tracking the
        executed queries and their outcomes.

        Example:
        '>>> self._execute(query="SELECT * FROM users WHERE id = %s", params={'id': 123}, fetchall=False)'
        This would execute the SQL query "SELECT * FROM users WHERE id = %s" with the parameter 'id' set to 123,
        and return the first row of the result.
        """
        self.cursor.execute(query=query, params=params)
        result = self.cursor.fetchall() if fetchall else self.cursor.fetchone()
        if self.with_allure:
            import allure
            with allure.step(title='Query to DataBase'):
                allure.attach(query, name='Query to DataBase', attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(result), name='Query Result', attachment_type=allure.attachment_type.TEXT)
        return result

    def get_list(self, query: str, params: dict[str, Any] | None = None) -> list[Any]:
        """
            Args:
                query (str): The SQL query to execute.
                params (dict[str, Any] | None, optional): The parameters to substitute in the query.
                    Defaults to None.
        """
        return [value[0] for value in self.select_all(query=query, params=params)]

    def get_dict(self, query: str, params: dict[str, Any] | None = None) -> dict[Any, Any] | None:
        """
            Args:
                query (str): The SQL query to execute.
                params (dict[str, Any] | None, optional): The parameters to substitute in the query.
                    Defaults to None.
        """
        result = self.select_all(query=query)
        if not result and len(result) < 1:
            return None
        return {value[0]: value[1] for value in self.select_all(query=query, params=params)}

    def select_all(self, query: str, params: dict[str, Any] | None = None) -> list[tuple]:
        """
            Args:
                query (str): The SQL query to execute.
                params (dict[str, Any] | None, optional): The parameters to substitute in the query.
                    Defaults to None.
        """
        return self._execute(query=query, params=params, fetchall=True)

    def get_first_value(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
            Args:
                query (str): The SQL query to execute.
                params (dict[str, Any] | None, optional): The parameters to substitute in the query.
                    Defaults to None.
        """
        result = self.get_first_row(query=query, params=params)
        if not result:
            return None
        return result[0]

    def get_first_row(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
            Args:
                query (str): The SQL query to execute.
                params (dict[str, Any] | None, optional): The parameters to substitute in the query.
                    Defaults to None.
        """
        return self._execute(query=query, params=params, fetchall=False)

    def execute(self, query: str, params: dict[str, Any] | None = None) -> None:
        """
        Execute a non-returning SQL query against the database.

        This method is used for executing SQL commands that do not return a result set, such as INSERT, UPDATE,
        or DELETE. It uses a cursor from the current database connection to execute the query. After execution,
        it commits the changes to the database. Additionally, it logs the query using Allure for debugging and
        auditing purposes.

        Args:
            query (str): The SQL query or command to be executed.
            params (dict[str, Any] | None, optional): A dictionary containing parameters to safely inject into
                the SQL query. This helps in preventing SQL injection attacks. Defaults to None if no parameters
                are provided.

        Example:
            '>>> execute(query="INSERT INTO users (name, email) VALUES (%s, %s)",
                         params={'name': 'John Doe', 'email': 'john@example.com'})'
            This will insert a new row into the 'users' table with the name 'John Doe' and email 'john@example.com'.

        Note:
            It's important to ensure that the query does not return a result set, as this method does not handle
            fetching results. For queries that retrieve data, use methods like 'select_all' or 'get_first_row'.
        """
        self.cursor.execute(query=query, params=params)
        self.connection.commit()
        if self.with_allure:
            import allure
            with allure.step(title='Query to DataBase'):
                allure.attach(query, name='Query to DataBase', attachment_type=allure.attachment_type.TEXT)
        return

    def __enter__(self) -> DBClient:
        self.connection = Connection.connect(self.connection_string)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cursor.close()
        self.connection.close()
        return
