import os
import time
import psycopg2

# Use same DATABASE_URL as the app; docker-compose will inject it
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://student:student123@db:5432/studentdb")


def create_table_and_seed():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS greetings (
                    id SERIAL PRIMARY KEY,
                    message TEXT NOT NULL
                );
            """)
            # Insert a default message if table is empty
            cur.execute("SELECT COUNT(*) FROM greetings;")
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute(
                    "INSERT INTO greetings (message) VALUES (%s);",
                    ("Hello from Flask and PostgreSQL!",)
                )
        conn.commit()
    print("Database initialized")


if __name__ == '__main__':
    # Wait for DB to be available
    for i in range(20):
        try:
            create_table_and_seed()
            break
        except Exception as e:
            print(f"DB not ready yet ({e}), retrying...")
            time.sleep(2)
    else:
        print("Failed to initialize DB after retries")
