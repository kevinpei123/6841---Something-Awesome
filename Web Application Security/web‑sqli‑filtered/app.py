#!/usr/bin/env python3
from flask import Flask, request
import sqlite3, os, re

app = Flask(__name__)
DB = os.path.splitext(__file__)[0] + ".db"
FLAG = os.getenv("FLAG") or "flag{sqli_filtered}"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS very_secret(flag TEXT)")
    try:
        cur.executemany("INSERT INTO users VALUES (?,?)", [(1,'alice'), (2,'bob'), (3,'charlie')])
    except Exception:
        pass
    try:
        cur.execute(f"INSERT INTO very_secret VALUES ('{FLAG}')")
    except Exception:
        pass
    conn.commit()
    conn.close()

init_db()

@app.route("/lookup")
def lookup():
    uid = request.args.get("uid", "")
    forbidden = re.compile("[\'\";]")
    if forbidden.search(uid):
        return "Nice try 🖐", 400

    query = "SELECT name FROM users WHERE uid = " + uid
    try:
        c = sqlite3.connect(DB)
        rows = c.execute(query).fetchall()
        c.close()
    except Exception:
        return "SQL error", 400

    if rows:
        return "User name: " + rows[0][0]
    return "Len=" + str(len(rows))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
