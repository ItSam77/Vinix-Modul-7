Berikut adalah dashboard interaktif untuk analisis data Auto MPG dengan visualisasi dinamis dan filter interaktif.

Bagaimana cara menjalankan dashboard ini?

NOTE: Pastikan anda sudah memiliki python dan git di dalam sistem anda.
Untuk mengecek apakah anda memiliki python dan git, anda dapat menjalankan perintah berikut pada terminal:
```bash
python --version
git --version
```
Jika anda tidak memiliki python atau git, anda dapat mengunjungi situs resmi python dan git untuk mengunduhnya.

Python: https://www.python.org/
Git: https://git-scm.com/

1. Clone repository ini ke dalam direktori lokal Anda.
 ```bash	
 git clone https://github.com/ItSam77/Vinix-Modul-7.git
 ```

2. cd ke dalam direktori repository.
 ```bash
 cd Vinix-Modul-7
 ```

3. Buat virtual environment.
Windows:
```bash
python -m venv venv
```

Linux/Mac:
```bash
python3 -m venv venv
```

4. Aktifkan virtual environment.
Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

5. Install dependencies.
 ```bash
 pip install -r requirements.txt
 ```

6. Jalankan dashboard.
 ```bash
 panel serve app.py
 ```

7. Buka browser dan buka URL http://localhost:5006/ untuk melihat dashboard.