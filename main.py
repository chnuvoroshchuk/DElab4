import psycopg2
import csv
import os

def create_table_script(table_name, columns, primary_key, foreign_keys):
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"

    for column in columns:
        create_table_sql += f"    {column[0]} {column[1]},\n"

    create_table_sql += f"    PRIMARY KEY ({primary_key}),\n"

    for fk in foreign_keys:
        create_table_sql += f"    FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]}({fk[2]}),\n"

    create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

    return create_table_sql

def create_index_script(table_name, index_name, columns):
    return f"CREATE INDEX IF NOT EXISTS idx_{index_name} ON {table_name}({', '.join(columns)});"

def insert_data_into_table(conn, table_name, data_file, columns):
    with open(data_file, 'r', newline='', encoding='utf-8') as csv_file:
        cursor = conn.cursor()
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in row])})"
            cursor.execute(insert_sql, row)

        cursor.close()

def main():
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'abc382',
        'database': 'postgres'
    }

    conn = psycopg2.connect(**db_params)

    csv_folder = 'data'

    sql_folder = 'scripts'

    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]

        with open(os.path.join(csv_folder, csv_file), 'r', newline='', encoding='utf-8') as csv_data:
            csv_reader = csv.reader(csv_data)
            columns = [(column.strip(), 'VARCHAR(256)') for column in next(csv_reader)]
            # перша колонка - PRIMARY KEY
            primary_key = columns[0][0]

        create_table_script_sql = create_table_script(table_name, columns, primary_key, [])
        cursor = conn.cursor()
        cursor.execute(create_table_script_sql)

        for column in columns:
            index_name = f"{table_name}_{column[0]}_idx"
            create_index_script_sql = create_index_script(table_name, index_name, [column[0]])
            cursor.execute(create_index_script_sql)

        insert_data_into_table(conn, table_name, os.path.join(csv_folder, csv_file), [column[0] for column in columns])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
