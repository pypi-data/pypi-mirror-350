import logging
import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
from azure.identity import DefaultAzureCredential

logger = logging.getLogger(__name__ + ".base_package")

class LightRAGHelper:
    def __init__(self, env_helper):
        self.env_helper = env_helper
        self.conn = None

    def _create_connection(self):
        """
        Establishes a connection to PostgreSQL using AAD authentication.
        """
        try:
            user = self.env_helper.POSTGRESQL_USER
            host = self.env_helper.POSTGRESQL_HOST
            dbname = self.env_helper.POSTGRESQL_DATABASE

            # Acquire the access token
            credential = DefaultAzureCredential()
            access_token = credential.get_token(
                "https://ossrdbms-aad.database.windows.net/.default"
            )

            # Use the token in the connection string
            conn_string = (
                f"host={host} user={user} dbname={dbname} password={access_token.token}"
            )
            self.conn = psycopg2.connect(conn_string)
            logger.info("Connected to PostgreSQL successfully.")
            return self.conn
        except Exception as e:
            logger.error(f"Error establishing a connection to PostgreSQL: {e}")
            raise

    def get_connection(self):
        """
        Provides a reusable database connection.
        """
        if self.conn is None or self.conn.closed != 0:  # Ensure the connection is open
            self.conn = self._create_connection()
        return self.conn

    def store_vector_and_text(self, vector, text, metadata):
        """
        Stores a vector and associated text in the PostgreSQL database.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                query = """
                    INSERT INTO lightrag_store (vector, text, metadata)
                    VALUES (%s, %s, %s)
                """
                cur.execute(query, (vector, text, metadata))
                conn.commit()
                logger.info("Stored vector and text successfully.")
        except Exception as e:
            logger.error(f"Error storing vector and text: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def retrieve_vectors(self, query_vector, top_k):
        """
        Retrieves the top K vectors similar to the provided query vector.
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT text, metadata
                    FROM lightrag_store
                    ORDER BY vector <=> %s::vector
                    LIMIT %s
                    """,
                    (query_vector, top_k)
                )
                results = cur.fetchall()
                logger.info(f"Retrieved {len(results)} vectors.")
                return results
        except Exception as e:
            logger.error(f"Error retrieving vectors: {e}")
            raise
        finally:
            conn.close()