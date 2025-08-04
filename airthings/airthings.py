import os, requests
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Airthings API credentials
client_id = os.getenv("AIRTHINGS_CLIENT_ID")
device_id = os.getenv("AIRTHINGS_DEVICE_ID")
secret = os.getenv("AIRTHINGS_SECRET")

# PostgreSQL connection parameters
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password')
}

def get_airthings_token():
    """Get access token from Airthings API"""
    token_resp = requests.post("https://accounts-api.airthings.com/v1/token",
          auth=(client_id, secret),
          data={"grant_type":"client_credentials", "scope":"read:device:current_values"})
    token_resp.raise_for_status()
    return token_resp.json()["access_token"]

def fetch_airthings_data(token):
    """Fetch latest readings from Airthings device"""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
      f"https://ext-api.airthings.com/v1/devices/{device_id}/latest-samples",
      headers=headers
    )
    resp.raise_for_status()
    return resp.json()

def create_table_if_not_exists():
    """Create the airthings_readings table if it doesn't exist"""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Create table query
        create_table_query = """
        CREATE TABLE IF NOT EXISTS airthings_readings (
            id SERIAL PRIMARY KEY,
            time BIGINT NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            battery INTEGER,
            co2 DECIMAL(8,2),
            humidity DECIMAL(5,2),
            pm1 DECIMAL(8,2),
            pm25 DECIMAL(8,2),
            pressure DECIMAL(8,2),
            radon_short_term_avg DECIMAL(8,2),
            relay_device_type VARCHAR(50),
            rssi INTEGER,
            temp DECIMAL(5,2),
            voc DECIMAL(8,2)
        );
        """
        
        # Create indexes query
        create_indexes_query = """
        CREATE INDEX IF NOT EXISTS idx_airthings_time ON airthings_readings(time);
        CREATE INDEX IF NOT EXISTS idx_airthings_recorded_at ON airthings_readings(recorded_at);
        """
        
        # Execute table creation
        cur.execute(create_table_query)
        cur.execute(create_indexes_query)
        conn.commit()
        
        print("Table and indexes created successfully (if they didn't exist)")
        
    except psycopg2.Error as e:
        print(f"Database error during table creation: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Error during table creation: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def insert_reading_to_db(data):
    """Insert Airthings reading into PostgreSQL"""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Extract data from the response
        reading_data = data.get('data', {})
        
        # Insert query
        insert_query = """
        INSERT INTO airthings_readings (
            time, battery, co2, humidity, pm1, pm25, pressure, 
            radon_short_term_avg, relay_device_type, rssi, temp, voc
        ) VALUES (
            %(time)s, %(battery)s, %(co2)s, %(humidity)s, %(pm1)s, %(pm25)s, 
            %(pressure)s, %(radonShortTermAvg)s, %(relayDeviceType)s, %(rssi)s, %(temp)s, %(voc)s
        )
        """
        
        # Execute the insert
        cur.execute(insert_query, reading_data)
        conn.commit()
        
        print(f"Successfully inserted reading with timestamp: {reading_data.get('time')}")
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    try:
        # Ensure table exists
        create_table_if_not_exists()
        
        # Get API token and fetch data
        token = get_airthings_token()
        data = fetch_airthings_data(token)
        
        print("Fetched data:", data)
        
        # Insert into database
        insert_reading_to_db(data)
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
