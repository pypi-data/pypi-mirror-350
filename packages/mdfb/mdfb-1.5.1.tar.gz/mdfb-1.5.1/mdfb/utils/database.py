import sqlite3
import platformdirs
import os

def create_db(path: str):
    con = sqlite3.connect(os.path.join(path, "mdfb.db"))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS downloaded_posts (
            user_did TEXT NOT NULL,
            user_post_uri TEXT NOT NULL,
            feed_type TEXT NOT NULL,
            poster_post_uri TEXT NOT NULL,
            PRIMARY KEY (user_post_uri, user_did, feed_type)
        );
    """)
    con.close()

def connect_db() -> sqlite3.Connection:
    con = sqlite3.connect(os.path.join(platformdirs.user_data_path("mdfb"), "mdfb.db"))
    return con

def insert_post(cur: sqlite3.Cursor, rows: list[tuple]) -> bool:
    res = cur.executemany("""
        INSERT OR IGNORE INTO downloaded_posts (user_did, user_post_uri, feed_type, poster_post_uri) 
        VALUES (?, ?, ?, ?)
    """, rows)
    
    if res.rowcount > 0:
        return True
    return False

def check_post_exists(cur: sqlite3.Cursor, user_did: str, user_post_uri: str, feed_type: str) -> bool:
    res = cur.execute("""
        SELECT * FROM downloaded_posts 
        WHERE user_did = ? 
        AND user_post_uri = ?
        AND feed_type = ?
    """, (user_did, user_post_uri, feed_type))

    row = res.fetchone()
    if row:
        return True
    return False

def check_user_has_posts(cur: sqlite3.Cursor, user_did: str, feed_type: str) -> bool:
    res = cur.execute("""
        SELECT * FROM downloaded_posts
        WHERE user_did = ?
        AND feed_type = ?
    """, [user_did, feed_type])

    row = res.fetchone()
    if row:
        return True
    return False

def check_user_exists(did: str) -> bool:
    con = connect_db()
    cur = con.cursor()
    res = cur.execute("""
        SELECT * FROM downloaded_posts
        WHERE user_did = ?
    """, (did,))

    row = res.fetchone()
    if row:
        return True
    return False

def delete_user(did: str):
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        DELETE FROM downloaded_posts
        WHERE user_did = ?
    """, (did,))
    con.commit()

    if cur.rowcount > 0:
        print(f"Deleted {cur.rowcount} row(s)")
    else:
        print("No matching rows found to delete")

def restore_posts(did: str, post_types: dict) -> list[dict]:
    con = connect_db()
    con.row_factory = _dict_factory
    cur = con.cursor()

    uris = []
    conditions = []
    params = []
    query = "SELECT * FROM downloaded_posts"

    if did:
        conditions.append("user_did = ?")
        params.append(did)
    if post_types:
        selected_post_types = [post_type for post_type, wanted in post_types.items() if wanted]
        if selected_post_types:
            conditions.append("feed_type IN ({})".format(",".join(["?"] * len(selected_post_types))))
            params.extend(selected_post_types)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    rows = cur.execute(query, params)
    for row in rows:
        uris.append(row)
    return uris

def _dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

