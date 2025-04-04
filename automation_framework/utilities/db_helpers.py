import sqlite3

from automation_framework.config import DB_PATH

class DatabaseHelper:
    def __init__(self, db_name=DB_PATH):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT PRIMARY KEY,
                api_temperature REAL,
                feels_like REAL
            )''')

    def ensure_column_exists(self, column_name: str, column_type: str = "TEXT"):
        """ Checks if a column exists in the weather_data table, and adds it if missing."""

        cursor = self.conn.cursor()
        cursor.execute('PRAGMA table_info(weather_data)')
        columns = [col[1] for col in cursor.fetchall()]
        if column_name not in columns:
            alter_sql = f'ALTER TABLE weather_data ADD COLUMN {column_name} {column_type}'
            self.conn.execute(alter_sql)
            self.conn.commit()

    def insert_weather_data(self, city: str, **kwargs):
        """ Universal method to insert or update weather data for a city. Accepts fields as keyword arguments."""

        columns = ["city"] + list(kwargs.keys())
        placeholders = ["?"] * len(columns)
        values = [city] + list(kwargs.values())

        query = f"""
            INSERT OR REPLACE INTO weather_data ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
        """
        with self.conn:
            self.conn.execute(query, values)


    def get_weather_data(self, city: str, fields: list[str] = None):
        """Extracts data from DB by specified city name"""

        cursor = self.conn.cursor()
        cursor.execute(f"""
                    SELECT {', '.join(fields)} FROM weather_data
                    WHERE city = ?
                """, (city,))
        return cursor.fetchone()

    def get_aggregated_value(self, column: str, agg_func: str = "MAX"):
        """ Returns (city, value) where value = AGG(column), e.g. MAX(average_temperature).
        Supports aggregation functions like MAX, MIN, AVG.
        """

        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT city, {agg_func}({column})
            FROM weather_data
        """)
        return cursor.fetchone()

    def get_weather_records(
            self, fields: list[str] = None, where_clause: str = None, params: tuple = ()
    ) -> list[tuple]:
        """ General-purpose method to fetch weather data records with optional filtering.

        @param fields: List of fields to select (defaults to '*')
        @param where_clause: Optional WHERE clause (e.g. "temp_diff > ?")
        @param params: Tuple of parameters to pass into the query for safety

        @return: List of tuples with result rows
        """
        cursor = self.conn.cursor()
        selected_fields = ', '.join(fields) if fields else '*'

        query = f"SELECT {selected_fields} FROM weather_data"
        if where_clause:
            query += f" WHERE {where_clause}"

        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()

