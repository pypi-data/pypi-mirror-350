# allure-db-client

The `allure-db-client` is a Python library designed to facilitate the interaction with PostgreSQL databases. It leverages the `psycopg` library for database connectivity and integrates with the Allure framework for enhanced logging and debugging capabilities. This library simplifies executing SQL queries and retrieving results in various formats, making it particularly useful in testing and debugging environments.

### Features

- Easy connection to PostgreSQL databases using a connection string.
- Methods to fetch query results as lists, dictionaries, or individual values.
- Integration with Allure for logging SQL queries and results.
- Context management for automatic opening and closing of database connections.
- Safe parameter substitution in SQL queries to prevent SQL injection.

### Installation

To install `allure-db-client`, you will need to have Python installed on your system. The library can be installed using pip:

```bash
pip install allure-db-client
```

### Usage

#### Creating a Client Instance

First, import `DBClient` from `allure-db-client` and create an instance with your database connection string:

```python
from allure_db_client import DBClient

db_client = DBClient(connection_string="your_connection_string")
```

#### Executing Queries

You can execute various types of SQL queries using the provided methods:

- `get_list(query, params)`: Fetches the first column of each row as a list.
- `get_dict(query, params)`: Fetches the first two columns of each row as a dictionary.
- `select_all(query, params)`: Executes a query and fetches all rows.
- `get_first_value(query, params)`: Fetches the first column of the first row.
- `get_first_row(query, params)`: Fetches the first row.
- `execute(query, params)`: Executes a non-returning SQL command (e.g., INSERT, UPDATE).

#### Context Management

The `DBClient` can be used as a context manager to automatically handle database connections:

```python
with DBClient(connection_string="your_connection_string") as db_client:
    # Your database operations here
```

### Examples

Here's an example of using `DBClient` to fetch user data from a `users` table:

```python
with DBClient(connection_string="your_connection_string") as db_client:
    users = db_client.select_all("SELECT * FROM users")
    for user in users:
        print(user)
```

### Contributing

Contributions to `allure-db-client` are welcome! Please read our contributing guidelines for details on how to submit pull requests, report issues, or request features.

### License

`allure-db-client` is released under the MIT License. See the LICENSE file for more details.