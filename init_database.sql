def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_kasir (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # CEK USER DEFAULT RUZIQ
    cursor.execute("SELECT * FROM user_kasir WHERE username = ?", ("ruziq354",))
    user = cursor.fetchone()

    if not user:
        cursor.execute("""
        INSERT INTO user_kasir (username, password, role)
        VALUES (?, ?, ?)
        """, ("ruziq354", "ruziq354", "admin"))

    conn.commit()
    conn.close()
