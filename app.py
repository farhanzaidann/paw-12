from flask import Flask, render_template, request, redirect, url_for, session, make_response
from models import KategoriRoti, DaftarRoti, User

app = Flask(__name__)
app.secret_key = "bakery-secret-key-123"

def login_required():
    return 'user_id' in session

def admin_only():
    return session.get("role") == "admin"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    message = ""
    last_username = request.cookies.get('last_username', '')

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.check_login(username, password)
        
        if user:
            session['user_id'] = user['id_user']
            session['username'] = user['username']
            session['role'] = user['role']
            
            resp = make_response(redirect(url_for('index')))
            # Cookie berlaku 1 jam (60*60 detik)
            resp.set_cookie("last_username", username, max_age=60*60*24) 
            return resp
        else:
            message = "Username atau password salah."
            
    return render_template('login.html', message=message, last_username=last_username)

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie("last_username", "", max_age=0)
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Hanya admin yang dapat menambah user baru."
    
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        User.create_user(username, password, role)
        return redirect(url_for('index'))
        
    return render_template('register.html')

# --- MAIN ROUTES ---
@app.route('/')
def index():
    if not login_required():
        return redirect(url_for('login'))
    
    kategori = KategoriRoti.get_all()
    roti = DaftarRoti.get_all()
    last_username = request.cookies.get('last_username')
    
    return render_template(
        "index.html",
        kategori=kategori,
        roti=roti,
        username=session.get('username'),
        role=session.get('role'),
        last_username=last_username
    )

# --- KATEGORI ROUTES (Admin Only) ---
@app.route('/kategori/insert')
def form_insert_kategori():
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    return render_template('insert_kategori.html')

@app.route('/kategori/insert', methods=['POST'])
def insert_kategori():
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    nama = request.form.get("nama_kategori")
    deskripsi = request.form.get("deskripsi")
    KategoriRoti.create(nama, deskripsi)
    return redirect(url_for('index'))

@app.route('/kategori/update/<int:id_kategori>')
def form_update_kategori(id_kategori):
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    data = KategoriRoti.get_by_id(id_kategori)
    return render_template('update_kategori.html', data=data)

@app.route('/kategori/update/<int:id_kategori>', methods=['POST'])
def update_kategori(id_kategori):
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    nama = request.form.get("nama_kategori")
    deskripsi = request.form.get("deskripsi")
    KategoriRoti.update(id_kategori, nama, deskripsi)
    return redirect(url_for('index'))

@app.route('/kategori/delete/<int:id_kategori>')
def delete_kategori(id_kategori):
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    KategoriRoti.delete(id_kategori)
    return redirect(url_for('index'))

# --- ROTI ROUTES (Admin Only) ---
@app.route('/roti/insert')
def form_insert_roti():
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    kategori = KategoriRoti.get_all()
    return render_template('insert_daftar.html', kategori=kategori)

@app.route('/roti/insert', methods=['POST'])
def insert_roti():
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    nama = request.form.get("nama_roti")
    id_kat = request.form.get("id_kategori")
    deskripsi = request.form.get("deskripsi")
    harga = request.form.get("harga")
    stok = request.form.get("stok")
    
    DaftarRoti.create(nama, id_kat, deskripsi, harga, stok)
    return redirect(url_for('index'))

@app.route('/roti/update/<int:id_roti>')
def form_update_roti(id_roti):
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    data = DaftarRoti.get_by_id(id_roti)
    kategori = KategoriRoti.get_all()
    return render_template('update_daftar.html', data=data, kategori=kategori)

@app.route('/roti/update/<int:id_roti>', methods=['POST'])
def update_roti(id_roti):
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    nama = request.form.get("nama_roti")
    id_kat = request.form.get("id_kategori")
    deskripsi = request.form.get("deskripsi")
    harga = request.form.get("harga")
    stok = request.form.get("stok")
    
    DaftarRoti.update(id_roti, nama, id_kat, deskripsi, harga, stok)
    return redirect(url_for('index'))

@app.route('/roti/delete/<int:id_roti>')
def delete_roti(id_roti):
    if not login_required(): return redirect(url_for('login'))
    if not admin_only(): return "Akses ditolak! (Admin Only)"
    
    DaftarRoti.delete(id_roti)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)