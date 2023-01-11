import sqlite3
from sqlite3 import Error


class Predmeti():
    def __init__(self, id_p, naziv):
        self.id_p = id_p
        self.naziv = naziv

    def Ispis(self):
        print("Predmet: ", self.naziv)


def create_connection(skola):
    connection = None
    try:
        connection = sqlite3.connect(skola)
        return connection
    except Error as e:
        print(e)

    return connection


def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def create_predmet(conn,predmet):
    try:
        sql = """INSERT INTO predmeti (id_p, naziv)
                    VALUES(?,?)"""
        cur = conn.cursor()
        parametri = (predmet.id_p, predmet.naziv)
        cur.execute(sql, parametri)
        conn.commit()
    except Error as e:
        print(e)

def select_all_predmeti(conn):
    sql = """SELECT * FROM predmeti;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def izbrisi_predmet(conn):
    podatak = [int(input("Unesite id predmeta koji zelite da izbrisete: "))]
    cur = conn.cursor()
    sql = ("""DELETE FROM predmeti WHERE id_p=?;""")
    cur.execute(sql, podatak)
    conn.commit()

def izmijeni_predmet(conn):
    id_p = int(input("Unesite id predmeta kojem zelite izmijeniti naziv: "))
    naziv = input("Unesite novi naziv predmeta: ")
    cur = conn.cursor()
    parametri = (naziv, id_p)
    sql = "UPDATE predmeti SET naziv =? WHERE id_p=?"
    cur.execute(sql, parametri)
    conn.commit()

if __name__ == '__main__':
    sql_create_predmeti_table = """CREATE TABLE IF NOT EXISTS predmeti (
                                    id_p integer PRIMARY KEY,
                                    naziv text NOT NULL
                                    )"""
    conn1 = create_connection("skola.db")
    if conn1 is not None:
        create_table(conn1, sql_create_predmeti_table)

        while True:
            cursor = conn1.cursor()
            izbor = int(input("Unesite 0 za kraj programa, 1 za unos novog predmeta, 2 za izmjenu predmeta, 3 za brisanje predmeta, 4 za ispis svih predmeta..: "))
            if izbor == 0:
                break
            elif izbor==1:
                id_p = int(input("Unesite id predmeta: "))
                naziv = input("Unesite naziv predmeta: ")
                p = Predmeti(id_p, naziv)
                create_predmet(conn1, p)
            elif izbor==2:
                izmijeni_predmet(conn1)
            elif izbor == 3:
                izbrisi_predmet(conn1)
            elif izbor==4:
                pr = select_all_predmeti(conn1)
                for i in pr:
                    print(i)
    else:
        print("Error! can't create the database connection.")
