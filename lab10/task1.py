import psycopg2


def connect_to_db():
    return psycopg2.connect(
    dbname="ex1",
    user="nurislambekbolat",
    password="",  # если не нужен пароль
    host="localhost",
    port="5432"
    )


def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        );
    """)


def insert_from_csv(cursor, connection, filename):
    with open(filename, encoding="utf-8") as file:
        next(file)  # Skip header
        for line in file:
            try:
                name, phone = line.strip().split(",")
                cursor.execute(
                    "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;",
                    (name, phone)
                )
                connection.commit()
            except Exception as e:
                print(f"[WARNING] Skipping line due to error: {e}")
                connection.rollback()


def update_contacts(cursor, connection, updates):
    for type_of_search, a, type_of_new, new_value in updates:
        try:
            cursor.execute(
                f"UPDATE contacts SET {type_of_new} = %s WHERE {type_of_search} = %s",
                (new_value, a)
            )
            connection.commit()
        except Exception as e:
            print(f"[WARNING] Failed to update: {e}")
            connection.rollback()


def delete_contacts(cursor, connection, deletions):
    for field_type, value in deletions:
        try:
            column = "name" if field_type.upper() == "NAME" else "phone"
            cursor.execute(f"DELETE FROM contacts WHERE {column} = %s", (value,))
            connection.commit()
        except Exception as e:
            print(f"[WARNING] Failed to delete: {e}")
            connection.rollback()


def query_contacts(cursor, condition, order_by_name, order_by_phone):
    cursor.execute(
        f"SELECT * FROM contacts WHERE {condition} ORDER BY name {order_by_name}, phone {order_by_phone}"
    )
    return cursor.fetchall()


def main():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        create_table(cursor)
        print("[INFO] Connected and table ensured.")

        insert_from_csv(cursor, connection,"/Users/nurislambekbolat/Desktop/pp2/lab10/EXAMPLE.csv")
        print("[INFO] Data inserted successfully.")

        n = int(input("How many updates? "))
        updates = [input().split() for _ in range(n)]
        update_contacts(cursor, connection, updates)

        n = int(input("How many deletions? "))
        deletions = [input().split() for _ in range(n)]
        delete_contacts(cursor, connection, deletions)

        condition = input("Enter filter condition (e.g. name LIKE 'J%'): ")
        order_by_name, order_by_phone = input("Enter sort order (e.g. ASC DESC): ").split()
        results = query_contacts(cursor, condition, order_by_name, order_by_phone)

        for row in results:
            print(row)

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print(f"[ERROR] {error}")


if __name__ == "__main__":
    main()
