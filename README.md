# 404NotFoundBE

Langkah langkah pemasangan:

pasang .env dengan contoh:

DB_HOST=localhost
DB_NAME=404notfound
DB_USER=root
DB_PASSWORD= #sesuaikan
DB_POOLNAME=404notfound_pool
POOL_SIZE=10

# Untuk konfigurasi Flask & JWT
SECRET_KEY=supersecretkey
JWT_SECRET_KEY=superjwtsecretkey

# Format SQLAlchemy URI dari atas:
DATABASE_URL=mysql+pymysql://root:#sesuaikan#@localhost/404notfound
FRONTEND_URL=http://localhost:5173

Tahap selanjutnya:

1. jalankan perintah rm -r migrations
2. DROP TABLE alembic_version;  # Lewat DB / phpMyAdmin #lakukan jika sudah ada, jika belum gausah ngedrop
3. jalankan perintah flask db init
4. jalankan perintah flask db migrate
5. jalankan perintah flask db upgrade

