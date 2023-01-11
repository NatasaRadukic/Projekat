import sqlite3
from sqlite3 import Error


class Ucenici:
    def __init__(self, id_u, ime, prezime, razred):
        self.id_u = id_u
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return "Ime: " + self.ime + ", prezime: " + self.prezime + ", razred: " + self.razred


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


def create_ucenik(conn, ucenik):
    try:
        sql = ''' INSERT INTO ucenici(id_u,ime,prezime,razred)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        parametri = (ucenik.id_u,ucenik.ime,ucenik.prezime,ucenik.razred)
        cur.execute(sql, parametri)
        conn.commit()
    except Error as e:
        print(e)


def select_all_ucenici(conn):
    sql = ''' SELECT * FROM ucenici;'''
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def delete_ucenik(conn):
    id_u = [int(input('Unesite id ucenika kojeg zelite izbrisati: '))]
    cur = conn.cursor()
    izbrisi = ('''DELETE FROM ucenici where id_u=?''')
    cur.execute(izbrisi,id_u)
    conn.commit()

def update_ucenik(conn):
    curr=conn.cursor()
    id_u = int(input("Unesite id ucenika kojem zelite da izmijenite razred: "))
    razred = input("Unesite razred ucenika: ")
    sql = "UPDATE ucenici SET razred = ? WHERE id_u = ?"
    curr.execute(sql,(razred,id_u))
    conn.commit()



if __name__=='__main__':
    sql_create_ucenici_table = """CREATE TABLE IF NOT EXISTS ucenici (
                                    id_u integer PRIMARY KEY,
                                    ime text NOT NULL,
                                    prezime text NOT NULL,
                                    razred text NOT NULL
                                    ); """
    conn =create_connection("skola.db")

    if conn is not None:
        create_table(conn,sql_create_ucenici_table)

        while True:
            cur = conn.cursor()
            izbor = int(input("Unesite 0 za kraj programa, 1 za unos ucenika, 2 za brisanje ucenika, 3 za izmjenu podataka o uceniku, 4 za ispis svih ucenika...: "))
            if izbor == 0:
                break
            elif izbor==1:
                id_u = int(input("Unesite id ucenika: "))
                ime = input("Unesite ime ucenika: ")
                prezime = input("Unesite prezime ucenika: ")
                razred = input("Unesite razred ucenika: ")
                u = Ucenici(id_u,ime,prezime,razred)
                create_ucenik(conn,u)
            elif izbor==2:
                delete_ucenik(conn)
            elif izbor==3:
                update_ucenik(conn)
            elif izbor==4:
                r = select_all_ucenici(conn)
                for i in r:
                    print(i)
    else:
        print("Error! can't create the database connection.")

connection = sqlite3.connect("skola.db")
cur = connection.cursor()
cur.execute("SELECT * FROM ucenici WHERE razred = 'VI-2'")
ans = cur.fetchall()
n = 0
for i in ans:
    print(i)
    n+=1
print("Broj ucenika u VI-2 razredu je: ", n)

class Razred():
    def __init__(self, id_r, razred, razrednik, broj_uc):
        self.id_r = id_r
        self.razred = razred
        self.razrednik = razrednik
        self.broj_uc = broj_uc

    def __str__(self):
        return "Razred: " + self.razred + " ima " + str(self.broj_uc) + " ucenika, a razrednik je: " + self.razrednik

