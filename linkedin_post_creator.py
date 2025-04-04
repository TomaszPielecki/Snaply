# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Rejestracja fontów z obsługą polskich znaków
def register_fonts():
    # Rejestracja fontów DejaVu (obsługują polskie znaki)
    font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    # Sprawdzenie, czy fonty już istnieją, jeśli nie - użyj domyślnych lub pobierz
    dejavu_regular = os.path.join(font_dir, 'DejaVuSans.ttf')
    dejavu_bold = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
    
    # Jeśli pliki fontów nie istnieją, informujemy użytkownika
    if not os.path.exists(dejavu_regular) or not os.path.exists(dejavu_bold):
        print("Proszę umieścić fonty DejaVu w katalogu 'fonts'.")
        print("Można je pobrać ze strony: https://dejavu-fonts.github.io/")
        print("Używam domyślnych fontów, polskie znaki mogą nie być poprawnie wyświetlane.")
        return False
    
    # Rejestracja fontów
    pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_regular))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_bold))
    return True

def create_project_pdf():
    # Próba rejestracji niestandardowych fontów z obsługą polskich znaków
    fonts_registered = register_fonts()
    
    doc = SimpleDocTemplate(
        "Snaply_Project_Description.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        encoding='utf-8'  # Ustawienie kodowania UTF-8 dla dokumentu
    )
    
    # Container for elements
    elements = []
    
    # Document Styles
    styles = getSampleStyleSheet()
    
    # Ustaw fonty z obsługą polskich znaków jeśli są dostępne
    font_name = 'DejaVuSans' if fonts_registered else 'Helvetica'
    font_name_bold = 'DejaVuSans-Bold' if fonts_registered else 'Helvetica-Bold'
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontName=font_name_bold,
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontName=font_name_bold,
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Modyfikacja stylu normalnego tekstu, aby używał fontu z polskimi znakami
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName=font_name_bold,
        fontSize=14
    )
    
    # Add title and subtitle
    elements.append(Paragraph("Projekt Snaply", title_style))
    elements.append(Paragraph("Narzędzie do Zaawansowanego Przechwytywania Ekranu", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Introduction
    intro_text = """
    Snaply to zaawansowane narzędzie do wykonywania zrzutów ekranu, które stworzyłem, aby umożliwić 
    łatwe przechwytywanie zawartości zarówno z urządzeń mobilnych, jak i desktopowych. Aplikacja 
    oferuje szereg funkcji usprawniających pracę programistów, testerów i specjalistów UX/UI.
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 12))
    
    # Content sections
    section_titles = [
        "O Projekcie Snaply",
        "Rozwiązane Problemy",
        "Technologie Wykorzystane w Projekcie",
        "Kluczowe Funkcjonalności",
        "Wyniki i Efekty",
        "Wnioski i Plany Rozwojowe"
    ]
    
    section_content = [
        """Snaply powstał jako odpowiedź na potrzebę efektywnego dokumentowania interfejsów 
        użytkownika podczas procesu rozwoju oprogramowania. Narzędzie umożliwia automatyczne 
        wykonywanie zrzutów ekranu na różnych urządzeniach, w różnych rozdzielczościach 
        i stanach interfejsu. Jest to nieoceniona pomoc zarówno w fazie projektowej, jak i 
        testowej każdego projektu cyfrowego.""",
        
        """1. Czasochłonny proces ręcznego tworzenia zrzutów ekranu
        2. Trudność w przechwytywaniu spójnych zrzutów na różnych urządzeniach
        3. Problemy z dokumentowaniem dynamicznych elementów interfejsu
        4. Brak narzędzia łączącego przechwytywanie z analizą wizualną
        5. Potrzeba szybkiego wykrywania zmian w interfejsie między wersjami""",
        
        """• Python jako główny język programowania
        • Selenium WebDriver do automatyzacji przeglądarek
        • Appium do testowania aplikacji mobilnych
        • OpenCV do analizy obrazu i wykrywania różnic
        • Flask do stworzenia interfejsu webowego
        • SQLite do przechowywania metadanych zrzutów
        • Docker do zapewnienia spójnego środowiska wykonawczego""",
        
        """• Równoczesne wykonywanie zrzutów ekranu na wielu urządzeniach
        • Automatyczne wykrywanie zmian wizualnych między wersjami
        • Przechwytywanie pełnej strony z przewijaniem
        • Izolowanie określonych elementów interfejsu
        • Harmonogramowanie sesji przechwytywania
        • Eksport rezultatów w różnych formatach (PNG, PDF, HTML)
        • Integracja z systemami CI/CD""",
        
        """Wdrożenie Snaply przyniosło wymierne korzyści:
        
        • Redukcja czasu poświęconego na dokumentację o 75%
        • Wcześniejsze wykrywanie błędów wizualnych w interfejsie
        • Usprawnienie procesu akceptacji zmian przez klientów
        • Lepszy wgląd w spójność UI na różnych urządzeniach
        • Automatyzacja raportowania różnic wizualnych
        • Przyspieszenie procesu testowania regresyjnego""",
        
        """Stworzenie Snaply było fascynującym wyzwaniem technicznym, które połączyło 
        moje umiejętności w zakresie automatyzacji i przetwarzania obrazu. Projekt jest 
        stale rozwijany, a w planach są:
        
        1. Wdrożenie sztucznej inteligencji do wykrywania istotnych zmian
        2. Rozszerzenie obsługi na urządzenia IoT i SmartTV
        3. Dodanie funkcji nagrywania interakcji użytkownika
        4. Stworzenie rozszerzenia do popularnych środowisk IDE
        5. Implementacja chmurowej wersji usługi"""
    ]
    
    # Add sections to document
    for i in range(len(section_titles)):
        elements.append(Paragraph(section_titles[i], heading_style))
        elements.append(Paragraph(section_content[i], normal_style))
        elements.append(Spacer(1, 12))
    
    # Use cases section
    elements.append(Paragraph("Przykłady Zastosowań", heading_style))
    
    use_cases = """
    Snaply znajduje zastosowanie w wielu scenariuszach zawodowych:
    
    • Testowanie regresyjne interfejsów - automatyczne wykrywanie nieplanowanych zmian
    • Dokumentacja produktu - tworzenie zrzutów do instrukcji i materiałów marketingowych
    • Kontrola jakości - weryfikacja spójności wizualnej na różnych urządzeniach
    • Rozwój responsywnych stron - testowanie wyglądu przy różnych rozdzielczościach
    • Współpraca z klientem - łatwe dokumentowanie błędów i propozycji zmian
    • Archiwizacja wersji produktu - śledzenie ewolucji interfejsu w czasie
    """
    
    elements.append(Paragraph(use_cases, normal_style))
    elements.append(Spacer(1, 12))
    
    # Personal skills developed
    elements.append(Paragraph("Umiejętności Rozwinięte Podczas Projektu", heading_style))
    
    skills_data = [
        ["Umiejętność", "Zastosowanie w projekcie"],
        ["Automatyzacja testów", "Tworzenie skryptów do automatycznego przechwytywania ekranu"],
        ["Przetwarzanie obrazu", "Analiza i porównywanie zrzutów ekranu"],
        ["Frontend/Backend", "Budowa interfejsu użytkownika i silnika aplikacji"],
        ["DevOps", "Konteneryzacja i ciągła integracja narzędzia"],
        ["UX Design", "Projektowanie intuicyjnego interfejsu użytkownika"]
    ]
    
    # Update table style to use custom fonts
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), font_name_bold),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    # Create the table
    skills_table = Table(skills_data, colWidths=[2.5*inch, 3.5*inch])
    skills_table.setStyle(table_style)
    
    elements.append(skills_table)
    elements.append(Spacer(1, 20))
    
    # Conclusion
    conclusion = """
    Projekt Snaply pokazuje, jak automatyzacja może znacząco usprawnić proces rozwoju 
    oprogramowania i kontroli jakości. Narzędzie to pozwala zaoszczędzić czas, obniżyć 
    koszty i podnieść jakość produktów cyfrowych dzięki precyzyjnemu i systematycznemu 
    podejściu do dokumentacji wizualnej.
    
    Jestem dumny, że stworzyłem rozwiązanie, które rozwiązuje realne problemy deweloperów 
    i zespołów QA. Snaply reprezentuje moje podejście do inżynierii oprogramowania: 
    identyfikacja potrzeby, opracowanie efektywnego rozwiązania i ciągłe doskonalenie.
    """
    elements.append(Paragraph("Podsumowanie", heading_style))
    elements.append(Paragraph(conclusion, normal_style))
    
    # Build the PDF
    doc.build(elements)
    print("PDF z opisem projektu został pomyślnie utworzony!")
    
    # Informacja dla użytkownika
    if not fonts_registered:
        print("\nUWAGA: Nie znaleziono fontów z obsługą polskich znaków.")
        print("Aby poprawnie wyświetlać polskie znaki, utwórz katalog 'fonts' i umieść w nim fonty DejaVu.")

if __name__ == "__main__":
    create_project_pdf()
