import duckdb

# Connect to DuckDB (will create the file)
con = duckdb.connect('data/sakila.duckdb')

# Install and load sqlite extension
con.execute("INSTALL sqlite")
con.execute("LOAD sqlite")

# Get all table names from SQLite database
tables_query = """
    SELECT name 
    FROM sqlite_scan('data/sakila.db', 'sqlite_master')
    WHERE type='table'
"""
tables = con.execute(tables_query).fetchall()

print("Migrating tables from SQLite to DuckDB...")
print(f"Found {len(tables)} tables")

# Copy each table from SQLite to DuckDB
for table in tables:
    table_name = table[0]
    print(f"  Migrating table: {table_name}")
    
    con.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM sqlite_scan('data/sakila.db', '{table_name}')
    """)

print("\n✅ Migration complete!")

# Verify tables were created
print("\nTables in DuckDB:")
result = con.execute("SHOW TABLES").fetchall()
for table in result:
    print(f"  - {table[0]}")

con.close()