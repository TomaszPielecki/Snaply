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
