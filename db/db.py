import psycopg2

conn = psycopg2.connect(
    host="192.168.203.222",
    database="dbkwon",
    user="connor",
    password="Dudrb12#",
    port="5432"
)

cur = conn.cursor()

query = "select * from maltipoo.keyword_list"

cur.execute(query)
conn.commit()
print(cur.fetchall())


cur.close()
conn.close()