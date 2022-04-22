import sqlite3

connection = sqlite3.connect(':memory:')
c = connection.cursor()

class queries:
    c.execute("""CREATE TABLE if NOT EXISTS guilds (
        id string,
        prefix string
    )""")

    def db_set(id, prefix):
        c.execute("INSERT INTO guilds VALUES (:id, :prefix)", {'id':id, 'prefix':prefix})

    def db_get(id):
        with connection:
            c.execute("SELECT * FROM guilds WHERE id=:id", {'id' : id})
            return c.fetchone()
        
    def db_del(id):
        with connection:
            c.execute("DELETE from guilds where id={}".format(id))

    def db_update(id, prefix):
        with connection:
            c.execute("UPDATE guilds SET prefix=:prefix WHERE id=:id", {'id' : id, 'prefix' : prefix})

connection.commit()