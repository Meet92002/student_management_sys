import sqlite3
import os

def sqlite_to_mysql_dump(sqlite_db, output_sql):
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    with open(output_sql, 'w', encoding='utf-8') as f:
        f.write("-- MySQL Dump for Student Management System\n")
        f.write("CREATE DATABASE IF NOT EXISTS student_management;\n")
        f.write("USE student_management;\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

        for table in tables:
            f.write(f"-- Table structure for {table}\n")
            f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
            
            # Get table creation info from SQLite
            cursor.execute(f"PRAGMA table_info(`{table}`)")
            columns = cursor.fetchall()
            
            create_stmt = f"CREATE TABLE `{table}` (\n"
            cols_def = []
            pk = []
            
            for col in columns:
                # cid, name, type, notnull, dflt_value, pk
                col_name = col[1]
                col_type = col[2].upper()
                not_null = " NOT NULL" if col[3] else ""
                default = f" DEFAULT {col[4]}" if col[4] else ""
                
                # Map types
                if "VARCHAR" in col_type or "STRING" in col_type or col_type == "":
                    # Estimate size if missing
                    col_type = "VARCHAR(255)"
                elif "JSON" in col_type:
                    col_type = "JSON"
                elif "BOOLEAN" in col_type:
                    col_type = "TINYINT(1)"
                
                cols_def.append(f"  `{col_name}` {col_type}{not_null}{default}")
                if col[5]: # is primary key
                    pk.append(f"`{col_name}`")
            
            create_stmt += ",\n".join(cols_def)
            if pk:
                create_stmt += ",\n  PRIMARY KEY (" + ", ".join(pk) + ")"
            create_stmt += "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
            f.write(create_stmt)

            # Dump Data
            cursor.execute(f"SELECT * FROM `{table}`")
            rows = cursor.fetchall()
            if rows:
                f.write(f"-- Dumping data for {table}\n")
                for row in rows:
                    values = []
                    for val in row:
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        else:
                            # Escape single quotes for MySQL
                            escaped = str(val).replace("'", "''")
                            values.append(f"'{escaped}'")
                    f.write(f"INSERT INTO `{table}` VALUES ({', '.join(values)});\n")
                f.write("\n")

        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    conn.close()
    print(f"MySQL dump created at {output_sql}")

if __name__ == "__main__":
    db_file = 'student_management.db'
    output = 'student_management_mysql.sql'
    if os.path.exists(db_file):
        sqlite_to_mysql_dump(db_file, output)
    else:
        print("Database not found!")
