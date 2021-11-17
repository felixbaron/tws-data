from psycopg2 import connect
from psycopg2.extensions import AsIs
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from ..tws.helper import read_csv_to_dict

database_name = "stock_data"


def connect_database(db_name=None):
    """Connect to database depending if db_name given or not"""
    if db_name is not None:
        connection = connect(
            f"host=0.0.0.0 dbname={db_name} user=postgres password=postgres"
        )
    else:
        connection = connect("host=0.0.0.0 user=postgres password=postgres")

    return connection


def create_database(cursor):
    """Create database"""
    cursor.execute(f"CREATE DATABASE {database_name};")


def create_table(cursor, table_name):
    """Create schema"""
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name}(id serial PRIMARY KEY, symbol varchar(20), market varchar);"
    )

def create_pricing_table(cursor):
    """Create schema"""
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS prices (id serial PRIMARY KEY, symbol varchar(20), market varchar, price real, date_time date);"
    )

def enhance_schema(cursor, table_name, schema_as_dict: dict):
    """Creates columns in a table with the keys of a dict"""
    statement = f"ALTER TABLE {table_name}"
    for key in schema_as_dict.fieldnames:
        statement = statement + " ADD COLUMN IF NOT EXISTS " + key + " VARCHAR,"

    # Remove trailing comma
    statement = statement[:-1]
    statement = statement + ";"
    cursor.execute(statement)


def commit_and_close(connection, cursor):
    """Commit transaction and close connection"""
    connection.commit()
    cursor.close()
    connection.close()


def fixtures(is_create_db=False, is_create_table=False):
    """Create table"""
    global database_name
    # Create database
    if is_create_db:
        connection = connect_database()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        create_database(cursor)
        commit_and_close(connection, cursor)

    # Create table
    if is_create_table:
        connection = connect_database("stock_data")
        cursor = connection.cursor()
        create_table(cursor, "symbols")
        create_pricing_table(cursor)
        commit_and_close(connection, cursor)


def update_schema(schema_file):
    """Insert columns to table"""
    global database_name
    schema = read_csv_to_dict(schema_file)
    connection = connect_database(database_name)
    cursor = connection.cursor()
    if "kpis" in schema_file:
        enhance_schema(cursor, "symbols", schema)
    commit_and_close(connection, cursor)


def save_row(database, symbol, market, table, csv_file):
    # TODOC: describe arguments
    """Save a row to a table in a database"""
    connection = connect_database(database)
    cursor = connection.cursor()
    rows = read_csv_to_dict(csv_file)

    for row in rows:
        # Add symbol
        row["symbol"] = symbol
        row["market"] = market

        columns = row.keys()
        values = [row[column] for column in columns]
        insert_statement = f"insert into {table} (%s) values %s"

        cursor.execute(insert_statement, (AsIs(",".join(columns)), tuple(values)))

    commit_and_close(connection, cursor)
