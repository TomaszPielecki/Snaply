# Snaply - Narzędzie do zarządzania zrzutami ekranów stron WWW

![Snaply Logo](https://via.placeholder.com/150/0077FF/FFFFFF?text=Snaply)

## 📋 Opis

Snaply to kompleksowa aplikacja webowa przeznaczona do automatyzacji procesu tworzenia, zarządzania i analizowania zrzutów ekranów stron internetowych. Aplikacja umożliwia wykonywanie zrzutów ekranów witryn w widoku mobilnym i desktopowym, katalogowanie ich według domen i dat oraz zaawansowane filtrowanie.

## ✨ Główne funkcje

- **Automatyczne zrzuty ekranu** - wykonywanie zrzutów ekranu stron WWW w formatach desktop i mobile
- **Przeglądanie podstron** - automatyczne wyszukiwanie i przechwytywanie wszystkich podstron witryny
- **Zarządzanie domenami** - dodawanie, edycja i usuwanie domen
- **Galeria zrzutów** - łatwe przeglądanie i filtrowanie wykonanych zrzutów ekranu
- **System użytkowników** - rejestracja i logowanie z podziałem na role (administrator/użytkownik)
- **Logi systemowe** - śledzenie wszystkich operacji w aplikacji
- **Asynchroniczne zadania** - wykonywanie zrzutów ekranu jako zadania w tle
- **Obsługa wyskakujących okienek** - automatyczne zamykanie okienek z cookies i polityką prywatności przed wykonaniem zrzutu ekranu

## 🛠️ Technologie

### Backend
- **Python 3.8+**
- **Flask** - mikro-framework do tworzenia aplikacji webowych
- **Selenium** - biblioteka do automatyzacji przeglądarek internetowych
- **Pillow** - biblioteka do przetwarzania obrazów
- **Flask-WTF** - integracja Flask z WTForms do obsługi formularzy
- **WebDriver Manager** - zarządzanie sterownikami przeglądarek
- **Psutil** - monitoring procesów systemowych

### Frontend
- **HTML5 / CSS3**
- **Bootstrap 5** - framework CSS do szybkiego tworzenia responsywnych interfejsów
- **JavaScript** - interakcje po stronie klienta
- **Font Awesome** - zestaw ikon
- **Flask Jinja2** - silnik szablonów

### Przechowywanie danych
- **Pliki JSON** - przechowywanie konfiguracji i danych użytkowników
- **System plików** - przechowywanie zrzutów ekranu w zorganizowanej strukturze katalogów

## 🚀 Instalacja i uruchomienie

### Wymagania wstępne
- Python 3.8+
- Google Chrome (dla WebDrivera Selenium)
- Pip (zarządca pakietów Python)

### Instalacja
1. Sklonuj repozytorium:
```bash
git clone https://github.com/username/snaply.git
cd snaply
```

2. Utwórz i aktywuj wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate  # Na Windowsie: venv\Scripts\activate
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skonfiguruj zmienne środowiskowe:
```bash
# Utwórz plik .env i dodaj
SECRET_KEY=twoj_tajny_klucz
```

5. Uruchom aplikację:
```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:5000`

## 📂 Struktura projektu
```
snaply/
├── app.py                 # Główny plik aplikacji
├── config.py              # Konfiguracja aplikacji
├── requirements.txt       # Zależności Pythona
├── .env                   # Zmienne środowiskowe (nie wersjonowane)
├── .gitignore             # Pliki ignorowane przez Git
├── screenshots/           # Katalog przechowujący zrzuty ekranu
│   ├── domain1.com/
│   │   ├── desktop/
│   │   └── mobile/
│   └── domain2.com/
│       ├── desktop/
│       └── mobile/
├── static/                # Statyczne pliki (CSS, JS, obrazy)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/             # Szablony HTML (Jinja2)
│   ├── base.html
│   ├── dashboard/
│   ├── domains/
│   └── screenshots/
├── models/                # Modele danych
│   ├── __init__.py
│   ├── domain.py
│   ├── screenshot.py
│   └── user.py
├── controllers/           # Kontrolery / widoki
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── domains.py
│   └── screenshots.py
├── utils/                 # Narzędzia pomocnicze
│   ├── __init__.py
│   ├── browser.py         # Obsługa przeglądarki przez Selenium
│   ├── screenshot.py      # Logika wykonywania zrzutów
│   └── file_manager.py    # Zarządzanie plikami
├── tasks/                 # Zadania asynchroniczne
│   ├── __init__.py
│   └── scheduler.py
└── tests/                 # Testy jednostkowe i integracyjne
    ├── __init__.py
    ├── test_browser.py
    ├── test_screenshots.py
    └── test_domains.py
```

## 👥 Współpraca

Zachęcamy do współpracy przy projekcie! Aby to zrobić:

1. Utwórz fork repozytorium
2. Stwórz swoją gałąź funkcji (`git checkout -b feature/AmazingFeature`)
3. Zatwierdź zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Wypchnij do gałęzi (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📝 Licencja

Projekt jest dostępny na licencji MIT. Pełny tekst licencji znajduje się w pliku [LICENSE](LICENSE).

```
MIT License

Copyright (c) 2023 Snaply

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Podziękowania

- Zespół Selenium za świetne narzędzie do automatyzacji przeglądarek
- Społeczność Flask za doskonały framework
- Wszystkim kontrybutorów, którzy pomogali w rozwoju projektu
