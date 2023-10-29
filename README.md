# 📕 Bookquet 💐
<!-- (coba coba) Untuk kamu yang belum dapat karangan bunga dari si Doi, Bookquet datang memberikan solusi -->
\~ Di setiap buku, terdapat karangan kata-kata berbunga \~

> "If you don’t like to read, you haven’t found the right book." – **J.K. Rowling**

> Proyek ini dibuat untuk memenuhi tugas Proyek Tengah Semester (PTS) pada mata kuliah Pemrograman Berbasis Platform (CSGE602022) yang diselenggarakan oleh Fakultas Ilmu Komputer, Universitas Indonesia Tahun Ajaran 2023/2024 Semester Gasal.

## 👥 Anggota Kelompok
Kami dari kelompok D-12 yang beranggotakan:
| Nama | NPM | Github | 
| -- | -- | -- |
| Akmal Ramadhan | 2206081534 | Akmal76 |
| Carissa Aida Zahra | 2206082543 | carissadzr
| Edbert Halim | 2206813795 | edbert2397 |
| Farah Aura Rosadi | 2206824773 | FarahAuraR
| William | 2206083432 | sunsetheus |

## 📜 Cerita Aplikasi

Dalam rangka diselenggarakannya Kongres Bahasa Indonesia XII pada bulan Oktober 2023, kelompok D-12 dengan bangga mepersembahkan **Bookquet** - sebuah aplikasi inovatif yang menghadirkan literasi ke dalam pengalaman baru. Lebih dari sekadar perpustakaan pribadi, Bookquet memanjakan pengguna melalui pengalaman yang tak terlupakan dengan fitur penyimpanan buku yang akan dibaca nanti. Selain itu, pengguna dapat memberikan ulasan mengenai buku yang sudah dibaca. Nantinya, aplikasi ini bukan hanya tempat untuk literasi, tetapi juga sebagai sarana untuk mendorong generasi muda Indonesia untuk menjelajahi kekayaan kata-kata. Mari menjelajah dunia literasi bersama Bookquet 💐.

## 📚 Daftar Modul
Berikut ini adalah daftar modul yang akan kami implementasikan beserta pengembang dari setiap modul.
 
| Modul | Penjelasan | Pengembang |
| -- | -- | -- |
| **Authentication & Admin Dashboard** | Pengguna pada aplikasi Django ini dapat melakukan registrasi, *login*, dan *logout*. Admin dapat melihat dashboard mereka dan mengedit Quotes of The Day pada homepage. | Carissa |
| **Dashboard** | Menampilkan informasi pribadi pengguna. | Carissa |
| **Homepage** | Menampilkan halaman utama berupa daftar buku. Pengguna disambut dengan *hero block* dan daftar buku dibawahnya. Pengguna juga bisa menggunakan fitur *filter* dan *search* untuk mencari buku berdasarkan *genre* dan judul. | Akmal |
| **Book Preview**| Menampilkan informasi suatu buku seperti sinopsis, pengarang, ISBN, dan lain-lain. Pengguna dapat memberikan *review*, *rate*, atau memasukkan buku ke dalam daftar baca nanti.  | William |
| **Read Later** | Pengguna dapat menambahkan suatu buku ke dalam daftar baca nanti. Dalam aplikasi Django ini, pengguna dapat melihat daftar buku yang ditambahkan dan dapat menghapus buku tersebut dari daftar baca nanti. | Edbert |
| **Rate & Review Book** | Pengguna juga dapat menambahkan *review* dan *rating* pada suatu buku. Pada aplikasi ini, pengguna dapat melihat daftar buku yang sudah diberi *review* dan *rating* serta dapat mengedit salah satunya. | Farah |

## 🕵️ *Role* atau Peran Pengguna 
### 1. 👨‍💻 User
#### 🔓 User yang Sudah Terautentikasi
- Melakukan pencarian dan *filter* berdasarkan genre
- Membuka halaman *profile* yang berisi data-data user terkait
- Memberikan *review* dan *rating* ke buku yang dipilih
- Menambah dan menghapus daftar buku pada fitur baca nanti

#### 🔒 User yang Belum Terautentikasi
- Melakukan pencarian dan *filter* berdasarkan genre
- Melihat buku pada halaman utama
### 2. 👩‍💻 Admin
- Melakukan register dan login sebagai pembaca
- Menambahkan dan menghapus daftar buku
- Menghapus *review user* pada suatu buku

##  *Dataset* yang Digunakan
*Dataset* yang kami gunakan bersumber dari [Kaggle - GoodReads Best Books](https://www.kaggle.com/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b/data). Alasan pemilihan *dataset* ini dikarenakan tersedianya informasi lengkap buku seperti deskripsi singkat, genre, gambar sampul, dan lain-lain. Kami akan mengambil sebanyak 150 buku dari *dataset* tersebut.
