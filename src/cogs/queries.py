import sqlite3

connection = sqlite3.connect(':memory:')
c = connection.cursor()

class queries:
    c.execute("""CREATE TABLE if NOT EXISTS prefixes (
        id string,
        prefix string
    )""")

    c.execute("""CREATE TABLE if NOT EXISTS mutedRoles (
        id string,
        roleid string
    )""")

    def db_set(key, id_ : str, val):
        c.execute("INSERT INTO {} VALUES (:id, :prefix)".format(key), {'id':id_, 'prefix':val})

    def db_get(key : str, id_ : str):
        with connection:
            c.execute("SELECT * FROM {} WHERE id={}".format(key, id_))
            return c.fetchone()
        
    def db_del(key : str, id_ : str):
        with connection:
            c.execute("DELETE from {} where id={}".format(key, id_))

    def db_update(key : str, id_ : str, val):
        with connection:
            c.execute("UPDATE {} SET prefix=:prefix WHERE id=:id".format(key), {'id' : id_, 'prefix' : val})

connection.commit()