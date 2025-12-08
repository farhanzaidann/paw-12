import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='bakery',
            cursorclass=pymysql.cursors.DictCursor
        )

    def query(self, sql, params=None):
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
        return cursor

    def fetchall(self, sql, params=None):
        cursor = self.query(sql, params)
        return cursor.fetchall()

    def fetchone(self, sql, params=None):
        cursor = self.query(sql, params)
        return cursor.fetchone()

db = Database()

class KategoriRoti:

    @staticmethod
    def create(nama_kategori, deskripsi):
        sql = "INSERT INTO kategori_roti (nama_kategori, deskripsi) VALUES (%s, %s)"
        db.query(sql, (nama_kategori, deskripsi))
        return True

    @staticmethod
    def get_all():
        sql = "SELECT * FROM kategori_roti"
        return db.fetchall(sql)

    @staticmethod
    def get_by_id(id_kategori):
        sql = "SELECT * FROM kategori_roti WHERE id_kategori = %s"
        return db.fetchone(sql, (id_kategori,))

    @staticmethod
    def update(id_kategori, nama_kategori, deskripsi):
        sql = "UPDATE kategori_roti SET nama_kategori = %s, deskripsi = %s WHERE id_kategori = %s"
        db.query(sql, (nama_kategori, deskripsi, id_kategori))
        return True

    @staticmethod
    def delete(id_kategori):
        sql = "DELETE FROM kategori_roti WHERE id_kategori = %s"
        db.query(sql, (id_kategori,))
        return True

class DaftarRoti:

    @staticmethod
    def create(nama_roti, id_kategori, deskripsi, harga, stok):
        sql = """
        INSERT INTO daftar_roti (nama_roti, id_kategori, deskripsi, harga, stok)
        VALUES (%s, %s, %s, %s, %s)
        """
        db.query(sql, (nama_roti, id_kategori, deskripsi, harga, stok))
        return True

    @staticmethod
    def get_all():
        sql = """
        SELECT r.*, k.nama_kategori
        FROM daftar_roti r
        JOIN kategori_roti k ON r.id_kategori = k.id_kategori
        """
        return db.fetchall(sql)

    @staticmethod
    def get_by_id(id_roti):
        sql = "SELECT * FROM daftar_roti WHERE id_roti = %s"
        return db.fetchone(sql, (id_roti,))

    @staticmethod
    def get_by_kategori(id_kategori):
        sql = "SELECT * FROM daftar_roti WHERE id_kategori = %s"
        return db.fetchall(sql, (id_kategori,))

    @staticmethod
    def update(id_roti, nama_roti, id_kategori, deskripsi, harga, stok):
        sql = """
        UPDATE daftar_roti
        SET nama_roti = %s, id_kategori = %s, deskripsi = %s, harga = %s, stok = %s
        WHERE id_roti = %s
        """
        db.query(sql, (nama_roti, id_kategori, deskripsi, harga, stok, id_roti))
        return True

    @staticmethod
    def delete(id_roti):
        sql = "DELETE FROM daftar_roti WHERE id_roti = %s"
        db.query(sql, (id_roti,))
        return True

class User:
    @staticmethod
    def create_user(username, password, role):
        sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        db.query(sql, (username, password, role))
        return True
        
    @staticmethod
    def check_login(username, password):
        sql = "SELECT * FROM users WHERE username = %s"
        user = db.fetchone(sql, (username,))
        if user and user["password"] == password:
            return user
        return None
    
class User:
    @staticmethod
    def create_user(username, password, role):
        hashed = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        db.query(sql, (username, hashed, role))
        return True

    @staticmethod
    def check_login(username, password):
        sql = "SELECT * FROM users WHERE username = %s"
        user = db.fetchone(sql, (username,))
        if user and check_password_hash(user['password'], password):
            return user
        return None