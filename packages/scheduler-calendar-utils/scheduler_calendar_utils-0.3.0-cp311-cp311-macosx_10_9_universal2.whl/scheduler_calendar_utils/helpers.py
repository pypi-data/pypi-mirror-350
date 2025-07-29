# helpers.py

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from flask import jsonify
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pymysql
from google.cloud import firestore

def is_duplicate(db, document: str, collection: str) -> bool:
    """
    Check if a document already exists in the specified Firestore collection.

    Parameters:
    - db: An instance of the Firestore client.
    - document (str): The document ID to check for existence.
    - collection (str): The Firestore collection name to look in.

    Returns:
    - bool: True if the document exists, False otherwise.

    Notes:
    - Uses an optimized call to avoid retrieving document fields.
    """
    return db.collection(collection).document(document).get(field_paths=[]).exists

def mark_as_seen(db, document: str, collection: str, trace_id: str | int, **kwargs):
    """
    Mark a Firestore document as seen/processed by writing trace metadata.

    Parameters:
    - db: An instance of the Firestore client.
    - document (str): The document ID to write.
    - collection (str): The Firestore collection name to write into.
    - trace_id (str | int): A unique identifier for tracing the request or operation.
    - **kwargs: Additional fields to store in the document.

    Behavior:
    - Overwrites the document (if it exists) or creates a new one.
    - Adds 'trace_id', 'status', and a server-side timestamp.
    - Merges any additional keyword arguments into the document.
    """
    db.collection(collection).document(document).set({
        "trace_id": trace_id,
        "status": "forwarded",
        "timestamp": firestore.SERVER_TIMESTAMP,
        **kwargs
    })

def query_db(pool: Engine, query: str, params: dict = None, is_select: bool = True):
    """
    Execute a query on the MySQL database using SQLAlchemy Engine.

    Parameters:
        pool (Engine): SQLAlchemy Engine for database connection.
        query (str): SQL query to be executed.
        params (dict, optional): Query parameters. Defaults to None.
        is_select (bool): Whether the query is a SELECT. Defaults to True.

    Returns:
        list[dict] if SELECT query; bool for modification queries.
    """
    compiled_query = text(query)
    with pool.connect() as connection:
        result = connection.execute(compiled_query, params or {})
        if is_select:
            results = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in results]
        else:
            connection.commit()
            return result.rowcount > 0  # Return True if any row was affected

def connection_pool(connection_name, db_user, db_pass, db_name, ip_type=IPTypes.PUBLIC) -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.
    Uses the Cloud SQL Python Connector package.
    """
    # Initialize the Cloud SQL Connector with the specified IP type (public or private)
    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        """
        Establish a new connection to the Cloud SQL instance.
        """
        conn: pymysql.connections.Connection = connector.connect(
            connection_name,  # The Cloud SQL instance connection name
            "pymysql",        # The database driver to use (PyMySQL)
            user=db_user,     # Database username
            password=db_pass, # Database password
            db=db_name,       # Name of the database to connect to
        )
        return conn

    # Create a SQLAlchemy engine with the connection pool managed by the connector
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",  # Database URL format for MySQL with PyMySQL driver
        creator=getconn,     # Function to create new connections using the connector
    )
    return pool  # Return the SQLAlchemy engine

def generate_response(status_code: int, 
                      response_body: dict = None, 
                      message: str = None,
                      additional_heads: dict = None,
                      trace_id: str | int = None):
    """
    Generate a structured HTTP response with trace ID header.

    Parameters:
        status_code (int): HTTP status code.
        response_body (dict, optional): Body of the response. Must be provided if 'message' is not.
        message (str, optional): Message to use if response_body is not provided.
        additional_heads (dict, optional): Any additional headers to include.
        trace_id (str | int, optional): Unique identifier for tracing.

    Returns:
        Flask Response: JSON response with headers.

    Raises:
        ValueError: If neither response_body nor message is provided.
    """
    if response_body is None and message is None:
        raise ValueError("Either 'response_body' or 'message' must be provided.")

    if response_body is None:
        response_body = {"message": message}

    if 'status' not in response_body:
        if 200 <= status_code < 300:
            response_body['status'] = 'success'
        elif 400 <= status_code < 500:
            response_body['status'] = 'client error'
        elif 500 <= status_code:
            response_body['status'] = 'server error'

    response = jsonify(response_body)
    response.status_code = status_code

    if trace_id is not None:
        response.headers['X-Trace-ID'] = trace_id

    if additional_heads:
        for k, v in additional_heads.items():
            response.headers[k] = v

    return response
