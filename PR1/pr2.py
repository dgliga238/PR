import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="DanaPR",
    user="postgres",
    password="Dana",
    host="localhost",
    port="8888"
)

# Create a cursor object
cur = conn.cursor()

# Execute a raw SQL query
cur.execute("INSERT INTO devices (name_device, price) VALUES (%s, %s)", ("Laptop", 1200))
conn.commit()

# Fetch and print users
cur.execute("SELECT * FROM devices")
users = cur.fetchall()
for device in devices:
    print(f"Device ID: {device[0]}, Name: {device[1]}, Price: {device[2]}")

# Close the cursor and connection
cur.close()
conn.close()
