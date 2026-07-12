import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        metadata TEXT,
        created_at TEXT NOT NULL
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS encounters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        transcript TEXT,
        soap_json TEXT,
        icd_json TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    ''')
    conn.commit()
    conn.close()


def create_patient(name, metadata=None):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute('INSERT INTO patients (name, metadata, created_at) VALUES (?, ?, ?)', (name, json.dumps(metadata) if metadata else None, now))
    pid = cur.lastrowid
    conn.commit()
    conn.close()
    return pid


def get_patients():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, metadata, created_at FROM patients ORDER BY created_at DESC')
    rows = cur.fetchall()
    out = []
    for r in rows:
        out.append({
            'id': r['id'],
            'name': r['name'],
            'metadata': json.loads(r['metadata']) if r['metadata'] else None,
            'created_at': r['created_at']
        })
    conn.close()
    return out


def save_encounter(patient_id, transcript, soap_obj, icd_list):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute('INSERT INTO encounters (patient_id, transcript, soap_json, icd_json, created_at) VALUES (?, ?, ?, ?, ?)',
                (patient_id, transcript, json.dumps(soap_obj), json.dumps(icd_list), now))
    eid = cur.lastrowid
    conn.commit()
    conn.close()
    return eid


def get_encounters_for_patient(patient_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, transcript, soap_json, icd_json, created_at FROM encounters WHERE patient_id = ? ORDER BY created_at DESC', (patient_id,))
    rows = cur.fetchall()
    out = []
    for r in rows:
        out.append({
            'id': r['id'],
            'transcript': r['transcript'],
            'soap': json.loads(r['soap_json']) if r['soap_json'] else None,
            'icd_codes': json.loads(r['icd_json']) if r['icd_json'] else None,
            'created_at': r['created_at']
        })
    conn.close()
    return out


def update_encounter(encounter_id, soap_obj=None, icd_list=None, transcript=None):
    conn = get_conn()
    cur = conn.cursor()
    # build set clause
    sets = []
    params = []
    if transcript is not None:
        sets.append('transcript = ?')
        params.append(transcript)
    if soap_obj is not None:
        sets.append('soap_json = ?')
        params.append(json.dumps(soap_obj))
    if icd_list is not None:
        sets.append('icd_json = ?')
        params.append(json.dumps(icd_list))
    if not sets:
        conn.close()
        return 0
    params.append(encounter_id)
    sql = f"UPDATE encounters SET {', '.join(sets)} WHERE id = ?"
    cur.execute(sql, params)
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    return rowcount
