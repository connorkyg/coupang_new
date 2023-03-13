import psycopg2
from psycopg2.extras import Json
from datetime import datetime

conn = psycopg2.connect(
    host="192.168.203.222",
    database="dbkwon",
    user="connor",
    password="Dudrb12#",
    port="5432"
)
conn.set_client_encoding('UTF8')
cur = conn.cursor()


def insert_request_info(ri_type, ri_raw, ri_payload):
    ri_reg_date = datetime.now()

    query = "INSERT INTO maltipoo.request_info (ri_type, ri_raw, ri_payload, ri_reg_date) VALUES (%s, %s, %s, %s);"
    values = (ri_type, Json(ri_raw), ri_payload, ri_reg_date)
    cur.execute(query, values)

    conn.commit()
    cur.close()
    conn.close()


def insert_response_info(rsi_status_code, rsi_headers, rsi_payload):
    rsi_reg_date = datetime.now()

    query = "INSERT INTO maltipoo.response_info (rsi_status_code, rsi_headers, rsi_payload, rsi_reg_date) VALUES (%s, %s, %s, %s);"
    values = (rsi_status_code, Json(rsi_headers), Json(rsi_payload), rsi_reg_date)
    cur.execute(query, values)

    conn.commit()
    cur.close()
    conn.close()
