"""Module for parsing WhatsApp database."""

import os
import sqlite3
import tempfile
import subprocess

from whatxtract.utils import get_adb_path

ADB_PATH = get_adb_path()
DB_PATH = '/data/data/com.whatsapp/databases/wa.db'


def extract_valid_contacts(adb_path=ADB_PATH):
    """Extracts valid WhatsApp contacts from the device."""
    with tempfile.TemporaryDirectory() as tmpdir:
        local_db_path = os.path.join(tmpdir, 'wa.db')

        pull_cmd = [adb_path, 'shell', 'su', '-c', f'cat {DB_PATH} > /sdcard/wa.db']
        subprocess.run(pull_cmd, check=True)
        subprocess.run([adb_path, 'pull', '/sdcard/wa.db', local_db_path], check=True)

        contacts = []
        conn = sqlite3.connect(local_db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT display_name, jid 
                FROM wa_contacts 
                WHERE is_whatsapp_user = 1 
                AND 
                jid LIKE '%@s.whatsapp.net'
                """)
            rows = cursor.fetchall()
            for name, jid in rows:
                phone = jid.split('@')[0]
                contacts.append((name or phone, phone))
        finally:
            conn.close()

        return contacts
