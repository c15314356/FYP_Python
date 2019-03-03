from cassandra.cluster import Cluster
import logging
cluster = Cluster()
session = cluster.connect()

session.set_keyspace('crimes')

rows = session.execute('SELECT * FROM TEST')
for row in rows:
    print(row[0], row[1], row[2], row[3])
    print(row.crime)


session.execute(
    """
    INSERT INTO TEST (id,crime,description,loc)
    VALUES (%s, %s, %s, %s)
    """,
    ('3','Burglary3','died','Dublin')
)
print('Session executed insert')

future = session.execute_async('SELECT * FROM test WHERE id=%s', ['2'])

try:
    rows = future.result()
    for row in rows:
        print(row)
except Exception:
    logging.exception("Operation failed:")