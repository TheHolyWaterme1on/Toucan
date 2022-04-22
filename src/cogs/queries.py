import sqlite3

connection = sqlite3.connect(':memory:')
c = connection.cursor()

class queries:
    c.execute("""CREATE TABLE if NOT EXISTS guilds (
        id string,
        prefix string
    )""")

    def db_set(gid, prefix):
        c.execute("INSERT INTO guilds VALUES (:id, :prefix)", {'id':gid, 'prefix':prefix})

    def db_get(gid):
        with connection:
            c.execute("SELECT * FROM guilds WHERE id=:id", {'id' : gid})
            return c.fetchone()
        
    def db_del(gid):
        with connection:
            c.execute("DELETE from guilds where id={}".format(gid))

    def db_update(gid, prefix):
        with connection:
            c.execute("UPDATE guilds SET prefix=:prefix WHERE id=:id", {'id' : gid, 'prefix' : prefix})

connection.commit()