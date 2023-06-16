import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="BankAPI",
    user="postgres",
    password="abc123")

# database cursor
conn.autocommit = True
cur = conn.cursor()  # TODO: close cursor when finished


def run():
    try:
        migrations_location = os.getcwd()
        migrations_location += "/bank_db/db_migrations/"
        filenames = []

        for filename in os.listdir(migrations_location):
            filenames.append(filename)

        filenames.sort()

        for filename in filenames:
            try:
                print("... Trying file number", filename[:3], "...")

                # open file and read sql script
                file_path = migrations_location + filename

                fd = open(file_path, 'r')
                sql = fd.read()
                fd.close()

                # execute command
                cur.execute(query=sql)
            except Exception as e:
                print(f"\tError running {filename}: ", e)

        cur.close()
    except Exception as e:
        print("Error running migrations: ", e)
