# -*- coding: utf-8 -*-
import os
import urllib.request
import zipfile
import shutil

def download_dejavu_fonts():
    """
    Pobiera i instaluje fonty DejaVu z obsługą polskich znaków.
    """
    print("Rozpoczynam pobieranie fontów DejaVu...")
    
    # Utworzenie katalogu na fonty
    font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    # URL do pobrania fontów DejaVu
    dejavu_url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
    zip_path = os.path.join(font_dir, "dejavu-fonts.zip")
    
    try:
        # Pobranie pliku zip z fontami
        print("Pobieram fonty z:", dejavu_url)
        urllib.request.urlretrieve(dejavu_url, zip_path)
        
        # Rozpakowanie fontów
        print("Rozpakowuję fonty...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(font_dir)
        
        # Przeniesienie potrzebnych fontów do głównego katalogu fontów
        extracted_dir = os.path.join(font_dir, "dejavu-fonts-ttf-2.37", "ttf")
        for font_file in ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]:
            src_path = os.path.join(extracted_dir, font_file)
            dst_path = os.path.join(font_dir, font_file)
            shutil.copy2(src_path, dst_path)
        
        # Usunięcie zbędnych plików
        os.remove(zip_path)
        shutil.rmtree(os.path.join(font_dir, "dejavu-fonts-ttf-2.37"))
        
        print("Fonty zostały pomyślnie zainstalowane!")
        print("Teraz możesz uruchomić program linkedin_post_creator.py aby utworzyć PDF z polskimi znakami.")
        return True
    
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania fontów: {str(e)}")
        print("Proszę pobrać fonty DejaVu ręcznie ze strony https://dejavu-fonts.github.io/")
        print("i umieścić pliki .ttf w katalogu 'fonts'.")
        return False

if __name__ == "__main__":
    download_dejavu_fonts()
