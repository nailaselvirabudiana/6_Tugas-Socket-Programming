# II2120-Jaringan-Komputer-UDP-Socket-Programming

Aplikasi ini terdiri dari dua file utama: server.py untuk menjalankan server yang menerima dan mem-broadcast pesan, serta client.py yang memungkinkan pengguna untuk terhubung ke server dan mengirim atau menerima pesan.

Persyaratan
Python 3.x
Jaringan lokal (LAN) atau konfigurasi jaringan yang memungkinkan klien dan server untuk saling berkomunikasi menggunakan UDP.
Cara Penggunaan
1. Server
Langkah-Langkah Menjalankan Server
Buka terminal.
Jalankan file server.py
python server.py
Server akan mulai mendengarkan pesan dari klien pada alamat IP dan port yang ditentukan di dalam script.

Fungsi Utama
Menerima Pesan: Server akan menerima pesan dari setiap klien yang terhubung.
Broadcast Pesan: Pesan yang diterima dari klien akan dicatat dan disiarkan ke semua klien lain yang aktif.
Log dan Hapus Klien: Jika klien mengirimkan pesan "exit", server akan mencatat pemutusan dan menghapus klien dari daftar.
Log jika Pengiriman Gagal: Server akan mencatat pemutusan koneksi jika terjadi kegagalan saat mengirim pesan ke klien.

2. Client
Langkah-Langkah Menjalankan Klien
Buka terminal.

Jalankan file client.py 
python client.py
Klien akan meminta alamat IP dan nomor port dari server untuk melakukan koneksi.

Setelah terhubung, klien dapat mengirim pesan yang akan disiarkan ke klien lain yang terhubung ke server yang sama.

Jika klien mengirim pesan "exit", klien akan memutuskan koneksi dari server.

Fungsi Utama
Kirim dan Terima Pesan: Klien dapat mengirim pesan ke server, yang kemudian akan menyiarkan pesan tersebut ke klien lain.
Keluar dari Chat: Klien dapat keluar dari chat dengan mengirim pesan "exit". Server akan mencatat pemutusan dan menghapus klien dari daftar aktif.
Struktur Kode
server.py: Mengatur fungsi server untuk menerima dan menyiarkan pesan serta menangani pemutusan koneksi.
client.py: Mengatur koneksi klien ke server, mengirim pesan, dan menampilkan pesan yang diterima.
Catatan Tambahan
Pastikan untuk menjalankan server.py terlebih dahulu sebelum menjalankan client.py.
Aplikasi ini menggunakan protokol UDP, yang berarti tidak ada jaminan pengiriman atau urutan pesan yang tepat. Hal ini sesuai untuk chatroom sederhana tetapi mungkin tidak cocok untuk aplikasi yang membutuhkan reliabilitas tinggi.
