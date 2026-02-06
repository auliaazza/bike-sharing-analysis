# Submission Dicoding
## Belajar Fundamental Analisis Data

---

### Tentang Proyek

Repository ini berisi proyek analisis data Bike Sharing Dataset yang saya kerjakan sebagai bagian dari submission proyek analisis data, kelas Belajar Fundamental Analisis Data (Dicoding).
Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit agar data lebih mudah dipahami secara visual.

---

### Deskripsi

Proyek ini bertujuan untuk memahami pola penyewaan sepeda berdasarkan waktu, seperti perbedaan antara hari kerja dan akhir pekan, serta pola peminjaman berdasarkan jam.
Melalui proses analisis ini, data diolah menjadi insight yang dapat membantu memahami kebiasaan pengguna dalam menggunakan layanan bike sharing.

---

### Struktur Direktori

* /data
Berisi dataset Bike Sharing dalam format.csv yang digunakan selama proses analisis.

* /dashboard
Berisi file utama Streamlit (dashboard.py) yang digunakan untuk menampilkan hasil analisis dalam bentuk dashboard interaktif.

* notebook.ipynb
Notebook yang berisi proses eksplorasi data, pembersihan data, analisis, visualisasi, dan penarikan insight.

* requirements.txt
Daftar library Python yang diperlukan untuk menjalankan proyek ini.

---

### Instalasi

1. Clone repository ini ke komputer lokal Anda menggunakan perintah berikut:

   ```shell
   git clone https://github.com/auliaazza/bike-sharing-analysis
   ```

2. Pastikan Anda memiliki lingkungan Python yang sesuai dan pustaka-pustaka yang diperlukan. Anda dapat menginstal pustaka-pustaka tersebut dengan menjalankan perintah berikut:

    ```shell
    pip install streamlit
    pip install -r requirements.txt
    ```

### Penggunaan
1. Masuk ke direktori proyek (Local):

    ```shell
    cd bike-sharing-analysis/dashboard/
    streamlit run dashboard.py
    ```
    Atau bisa dengan kunjungi website ini [Project Data Analytics](https://bike-sharing-analysis-aulia-azzahra.streamlit.app/)

---

### Insight Singkat

Beberapa temuan utama dari analisis ini:

* Pada hari kerja, terdapat dua puncak peminjaman di pagi dan sore hari yang mencerminkan aktivitas berangkat dan pulang kerja.

* Pada akhir pekan, pola peminjaman lebih santai dengan puncak di siang hari, cenderung bersifat rekreatif.

* Faktor cuaca memiliki peran penting dalam memengaruhi jumlah peminjaman sepeda.

---

### Kontribusi

Proyek ini terbuka untuk pengembangan. Silakan lakukan fork dan pull request jika ingin menambahkan fitur, memperbaiki visualisasi, atau mengembangkan analisis lebih lanjut.

---

### Penutup

Proyek ini dibuat sebagai bagian dari proses belajar analisis data dan sebagai portofolio untuk menunjukkan kemampuan dalam mengolah data serta menyajikannya dalam bentuk dashboard interaktif.
