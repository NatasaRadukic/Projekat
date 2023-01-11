import sqlite3
from sqlite3 import Error

class Ocjene():
    def __init__(self, id_o, ime_u, prezime_u, predmet, ocjena):
        self.id_o = id_o
        self.ime_u = ime_u
        self.prezime_u = prezime_u
        self.predmet = predmet
        self.ocjena = ocjena

    def Ispis(self):
        print("Ucenik ", self.ime_u, " ", self.prezime_u, " je dobio ", self.ocjena, " iz predmeta ", self.predmet)

    def Dobra_ocjena(self):
        while self.ocjena<1 or self.ocjena>5:
            print("Niste unijeli dobru ocjenu: ")
            self.ocjena = int(input("Unesite ocjenu ponovo: "))

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

def create_ocjenu(conn, ocjene):
    try:
        sql = """INSERT INTO ocjene (id_o, ime_u, prezime_u, predmet, ocjena)
                VALUES (?, ?, ?, ?, ?)"""
        cur = conn.cursor()
        parametri = (ocjene.id_o, ocjene.ime_u, ocjene.prezime_u, ocjene.predmet, ocjene.ocjena)
        cur.execute(sql, parametri)
        conn.commit()
    except Error as e:
        print(e)

def izmijeni_ocjenu(conn):
    id_o = int(input("Unesite id ocjene koju zelite promijeniti: "))
    ocjena = int(input("Unesite novu ocjenu: "))
    sql = "UPDATE ocjene SET ocjena=? WHERE id_o=?"
    cur = conn.cursor()
    cur.execute(sql, (ocjena, id_o))
    conn.commit()

def izbrisi_ocjenu(conn):
    id_o = [int(input("Unesite id ocjene koju zelite izbrisati: "))]
    sql = "DELETE FROM ocjene WHERE id_o = ?"
    cur = conn.cursor()
    cur.execute(sql, id_o)
    conn.commit()

def izaberi_sve_ocjene(conn):
    sql = "SELECT * FROM ocjene"
    cur = conn.cursor()
    cur.execute(sql)
    ocj = cur.fetchall()
    return ocj



def prosjecna_ocjena(conn):
    ime = input("Unesite ime ucenika kojem zelite izracunati prosjecnu ocjenu: ")
    prezime = input("Unesite prezime ucenika kojem zelite izracunati prosjecnu ocjenu: ")
    predmet = input("Unesite predmet za koji zelite izracunati prosjecnu ocjenu: ")
    sql = "SELECT * FROM ocjene WHERE ime_u = ? and prezime_u = ? and predmet = ?"
    cur = conn.execute(sql, (ime, prezime, predmet))
    ocj = cur.fetchall()
    suma = 0
    n = 0
    for o in ocj:
        suma += o[4]
        n+=1
    if n<3:
        print("Ucenik je neocjenjen iz predmeta: ", predmet)
    else:
        print("Prosjecna ocjena ucenika iz predmeta: ", predmet, " je: ", suma/n)


if __name__ == '__main__':
    sql_create_predmeti_table = """CREATE TABLE IF NOT EXISTS ocjene (
                                    id_o integer PRIMARY KEY,
                                    ime_u text NOT NULL,
                                    prezime_u text NOT NULL,
                                    predmet text NOT NULL,
                                    ocjena integer
                                    )"""
    conn1 = create_connection("skola.db")
    if conn1 is not None:
        create_table(conn1, sql_create_predmeti_table)

        while True:
            cursor = conn1.cursor()
            izbor = int(input("Unesite 0 za kraj programa, 1 za unos nove ocjene, 2 za izmjenu ocjene, 3 za brisanje ocjene, 4 za ispis svih ocjena..: "))
            if izbor == 0:
                break
            elif izbor==1:
                id_o = int(input("Unesite id ocjene: "))
                ime = input("Unesite ime ucenika: ")
                prezime = input("Unesite prezime ucenika: ")
                predmet = input("Unesite naziv predmeta: ")
                ocjena = int(input("Unesite ocjenu ucenika: "))
                o = Ocjene(id_o, ime, prezime, predmet, ocjena)
                o.Dobra_ocjena()
                create_ocjenu(conn1, o)
            elif izbor==2:
                izmijeni_ocjenu(conn1)
            elif izbor == 3:
                izbrisi_ocjenu(conn1)
            elif izbor==4:
                ocj = izaberi_sve_ocjene(conn1)
                for o in ocj:
                    print(o)
        prosjecna_ocjena(conn1)

    else:
        print("Error! can't create the database connection.")