import sqlite3
from sqlite3 import Error


class Nastavnici:
    def __init__(self, id_n, ime, prezime, razrednistvo, godina_zaposlenja):
        self.id_n = id_n
        self.ime = ime
        self.prezime = prezime
        self.razrednistvo = razrednistvo
        self.godina_zaposlenja = godina_zaposlenja

    def __str__(self):
        return "Ime: " + self.ime + ", prezime: " + self.prezime + ", razrednistvo: " + self.razrednistvo + ", godina zaposlenja: " + str(self.godina_zaposlenja)

    def Godine_staza(self):
        n = 2023 - self.godina_zaposlenja
        return "Nastavnik " + self.ime + " " + self.prezime + " ima " + str(n) + " staza."

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


def create_nastavnik(conn, nastavnik):
    try:
        sql = ''' INSERT INTO nastavnik (id_n,ime,prezime,razrednistvo, godina_zaposlenja)
                  VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        parametri = (nastavnik.id_n, nastavnik.ime, nastavnik.prezime, nastavnik.razrednistvo, nastavnik.godina_zaposlenja)
        cur.execute(sql, parametri)
        conn.commit()
    except Error as e:
        print(e)


def select_all_nastavnici(conn):
    sql = ''' SELECT * FROM nastavnik;'''
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def delete_nastavnik(conn):
    id_n = [int(input('Unesite id nastavnika kojeg zelite izbrisati: '))]
    cur = conn.cursor()
    izbrisi = ('''DELETE FROM nastavnik where id_n=?''')
    cur.execute(izbrisi,id_n)
    conn.commit()
def godine_staza(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM nastavnik WHERE godina_zaposlenja<2003")
    ans = cur.fetchall()
    for i in ans:
        print(i)
    print("Navedeni nastavnici imaju preko 20 godina staza.")

def update_nastavnik(conn):
    curr=conn.cursor()
    id_n = int(input("Unesite id nastavnika kojem zelite da izmijenite razrednistvo: "))
    razrednistvo = input("Unesite razrednistvo : ")
    sql = "UPDATE nastavnik SET razrednistvo = ? WHERE id_n = ?"
    curr.execute(sql,(razrednistvo,id_n))
    conn.commit()

def razrednici(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM nastavnik WHERE razrednistvo != ''")
    print("Spisak razrednika u skoli: ")
    ans = cur.fetchall()
    for i in ans:
        print(i)

if __name__=='__main__':
    sql_create_nastavnici_table = """CREATE TABLE IF NOT EXISTS nastavnik (
                                    id_n integer PRIMARY KEY,
                                    ime text NOT NULL,
                                    prezime text NOT NULL,
                                    razrednistvo text, 
                                    godina_zaposlenja integer NOT NULL
                                    ); """
    conn = create_connection("skola.db")

    if conn is not None:
        create_table(conn,sql_create_nastavnici_table)

        while True:
            cur = conn.cursor()
            izbor = int(input("Unesite 0 za kraj programa, 1 za unos nastavnika, 2 za brisanje nastavnika, 3 za izmjenu podataka o nastavniku, 4 za ispis svih nastavnika...: "))
            if izbor == 0:
                break
            elif izbor==1:
                id_n = int(input("Unesite id nastavnika: "))
                ime = input("Unesite ime nastavnika: ")
                prezime = input("Unesite prezime nastavnika: ")
                razrednistvo = input("Unesite razrednistvo nastavnika: ")
                godina_zaposlenja = int(input("Unesite godinu zaposlenja nastavnika: "))
                n = Nastavnici(id_n,ime,prezime,razrednistvo, godina_zaposlenja)
                create_nastavnik(conn, n)
            elif izbor==2:
                delete_nastavnik(conn)
            elif izbor==3:
                update_nastavnik(conn)
            elif izbor==4:
                r = select_all_nastavnici(conn)
                for i in r:
                    print(i)
        godine_staza(conn)
        razrednici(conn)
        
    else:
        print("Error! can't create the database connection.")
