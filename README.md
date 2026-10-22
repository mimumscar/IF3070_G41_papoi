# IF3070_G41_papoi

Repositori ini berisi implementasi dan visualisasi algoritma Genetic Algorithm,
Hill Climbing, dan Simulated Annealing untuk menyelesaikan masalah penempatan kendaraan pada geladak kapal kargo.

## Struktur Repository

- `src/` : source code
- `docs/` : laporan
- `output/` : hasil run algoritma

## Cara Setup & Menjalankan

1. Pastikan Python 3 dan pip sudah terinstall.
2. Install Flask:

```bash
pip install flask
```

3. Masuk ke folder `src/`:

```bash
cd src
```

4. Jalankan aplikasi:

```bash
python app.py
```

5. Buka alamat berikut pada browser:

```bash
http://127.0.0.1:5000/
```

Halaman utama digunakan untuk menjalankan Hill Climbing. Halaman Genetic
Algorithm dapat diakses melalui `/ga`, sedangkan halaman Simulated Annealing
dapat diakses melalui `/sa`.

## Pembagian Tugas

| Nama | NIM | Kontribusi |
|---|---|---|
| Amanda Trishya Aulia | 18224020 | Genetic Algorithm |
| Mineva Azzahra | 18224029 | Hill Climbing |
| Adriel Nathanael Simatupang | 18224109 | Simulated Annealing |