import psycopg2
from psycopg2 import Error


def start_connection():
    try:
        conn = psycopg2.connect(user="postgres", password="5432", host="127.0.0.1", port="5432", database="frinx")
        cursor = conn.cursor()
        print("Connection successfully created.")
    except (Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    return conn, cursor

def close_connection(conn, cursor):
    if conn and cursor:
        cursor.close()
        conn.close()
        print("PostgreSQL connection closed.")

def create_schema(conn, cursor):
    sql = '''
        CREATE TABLE interface (
            id SERIAL PRIMARY KEY,
            connection INTEGER,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            config json,
            type VARCHAR(50),
            infra_type VARCHAR(50),
            port_channel_id INTEGER,
            max_frame_size INTEGER
        );

        CREATE TABLE port_channel (
            id SERIAL PRIMARY KEY,
            number INTEGER,
            mode VARCHAR(20)
        );
        '''
    cursor.execute(sql)
    conn.commit()
