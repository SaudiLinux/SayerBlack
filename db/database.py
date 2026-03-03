import sqlite3, json

def save_scan(target, results):
    conn = sqlite3.connect("sayerblack_pro.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS scans (target TEXT, data TEXT)")
    c.execute("INSERT INTO scans VALUES (?,?)", (target, json.dumps(results)))
    conn.commit()
    conn.close()
