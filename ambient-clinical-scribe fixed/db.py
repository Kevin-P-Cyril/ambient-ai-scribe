import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # -----------------------------
    # Patients Table
    # -----------------------------
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            metadata TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    # -----------------------------
    # Encounters Table
    # -----------------------------
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS encounters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            transcript TEXT,
            soap_json TEXT,
            ai_soap_json TEXT,
            final_soap_json TEXT,
            icd_json TEXT,
            status TEXT DEFAULT 'Draft',
            created_at TEXT NOT NULL,
            updated_at TEXT,
            finalized_at TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        """
    )

    conn.commit()

    # -----------------------------
    # Backward Compatible Migration
    # -----------------------------
    columns = [
        row["name"]
        for row in cur.execute(
            "PRAGMA table_info(encounters)"
        ).fetchall()
    ]

    migrations = {
        "ai_soap_json": "ALTER TABLE encounters ADD COLUMN ai_soap_json TEXT",
        "final_soap_json": "ALTER TABLE encounters ADD COLUMN final_soap_json TEXT",
        "status": "ALTER TABLE encounters ADD COLUMN status TEXT DEFAULT 'Draft'",
        "updated_at": "ALTER TABLE encounters ADD COLUMN updated_at TEXT",
        "finalized_at": "ALTER TABLE encounters ADD COLUMN finalized_at TEXT",
    }

    for column, sql in migrations.items():
        if column not in columns:
            cur.execute(sql)

    conn.commit()
    conn.close()


# =====================================================
# PATIENTS
# =====================================================

def create_patient(name, metadata=None):
    conn = get_conn()
    cur = conn.cursor()

    now = datetime.utcnow().isoformat()

    cur.execute(
        """
        INSERT INTO patients
        (name, metadata, created_at)
        VALUES (?, ?, ?)
        """,
        (
            name,
            json.dumps(metadata) if metadata else None,
            now,
        ),
    )

    patient_id = cur.lastrowid

    conn.commit()
    conn.close()

    return patient_id


def get_patients():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            name,
            metadata,
            created_at
        FROM patients
        ORDER BY created_at DESC
        """
    )

    rows = cur.fetchall()

    patients = []

    for row in rows:
        patients.append(
            {
                "id": row["id"],
                "name": row["name"],
                "metadata": json.loads(row["metadata"])
                if row["metadata"]
                else None,
                "created_at": row["created_at"],
            }
        )

    conn.close()

    return patients


# =====================================================
# ENCOUNTERS
# =====================================================

def save_encounter(patient_id, transcript, soap_obj, icd_list):
    conn = get_conn()
    cur = conn.cursor()

    now = datetime.utcnow().isoformat()

    soap_json = json.dumps(soap_obj)

    cur.execute(
        """
        INSERT INTO encounters
        (
            patient_id,
            transcript,
            soap_json,
            ai_soap_json,
            final_soap_json,
            icd_json,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            transcript,
            soap_json,
            soap_json,
            soap_json,
            json.dumps(icd_list),
            "Draft",
            now,
            now,
        ),
    )

    encounter_id = cur.lastrowid

    conn.commit()
    conn.close()

    return encounter_id


def get_encounters_for_patient(patient_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM encounters
        WHERE patient_id = ?
        ORDER BY created_at DESC
        """,
        (patient_id,),
    )

    rows = cur.fetchall()

    encounters = []

    for row in rows:
        encounters.append(
            {
                "id": row["id"],
                "transcript": row["transcript"],
                "soap": json.loads(row["soap_json"])
                if row["soap_json"]
                else None,
                "ai_soap": json.loads(row["ai_soap_json"])
                if row["ai_soap_json"]
                else None,
                "final_soap": json.loads(row["final_soap_json"])
                if row["final_soap_json"]
                else None,
                "icd_codes": json.loads(row["icd_json"])
                if row["icd_json"]
                else None,
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "finalized_at": row["finalized_at"],
            }
        )

    conn.close()

    return encounters


def update_encounter(
    encounter_id,
    soap_obj=None,
    icd_list=None,
    transcript=None,
    status=None,
):
    conn = get_conn()
    cur = conn.cursor()

    updates = []
    params = []

    if transcript is not None:
        updates.append("transcript = ?")
        params.append(transcript)

    if soap_obj is not None:
        soap_json = json.dumps(soap_obj)

        updates.append("soap_json = ?")
        params.append(soap_json)

        updates.append("final_soap_json = ?")
        params.append(soap_json)

    if icd_list is not None:
        updates.append("icd_json = ?")
        params.append(json.dumps(icd_list))

    if status is not None:
        updates.append("status = ?")
        params.append(status)

        if status == "Finalized":
            updates.append("finalized_at = ?")
            params.append(datetime.utcnow().isoformat())

    updates.append("updated_at = ?")
    params.append(datetime.utcnow().isoformat())

    if not updates:
        conn.close()
        return 0

    params.append(encounter_id)

    query = f"""
        UPDATE encounters
        SET {', '.join(updates)}
        WHERE id = ?
    """

    cur.execute(query, params)

    conn.commit()

    affected_rows = cur.rowcount

    conn.close()

    return affected_rows