import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
import logging

# Ustawienia loggera
logging.basicConfig(filename='C:\\Users\\leszek.stanislawski\\Downloads\\Kodilla\\Python\\NumPy\\lokata.txt',
                    level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Parametry
cena_mieszkania_obecna = 120000  # w zł
wzrost_cen_mieszkan_rocznie = 0.05
okres_lat = 5
okres_miesiecy = okres_lat * 12
stopa_procentowa = 0.12 / 12  # Nominalna stopa procentowa z kapitalizacją miesięczną

# Obliczenia przyszłej ceny mieszkania
miesieczny_wzrost = 1 + wzrost_cen_mieszkan_rocznie / 12
przyszla_cena_mieszkania = cena_mieszkania_obecna * (miesieczny_wzrost ** okres_miesiecy)

# Obliczenia wpłaty miesięcznej do banku
raty = npf.pmt(stopa_procentowa, okres_miesiecy, 0, przyszla_cena_mieszkania, when='end')
wpłata_miesieczna_do_banku = -raty  # wartość ujemna

# Tworzenie wykresu zmiany ceny mieszkania i wartości lokaty w czasie
czas = np.arange(1, okres_miesiecy + 1)
cena_mieszkania = cena_mieszkania_obecna * (miesieczny_wzrost ** czas)
wartosc_lokaty = npf.fv(stopa_procentowa, czas, -wpłata_miesieczna_do_banku, 0, when='end')

# Zapisywanie składki ratalnej, uzbieranej kwoty na lokacie i zysku netto za pomocą logging
deponowana_kwota = wpłata_miesieczna_do_banku  # Składka ratalna równa wpłacie miesięcznej do banku
uzbierana_kwota = 0  # inicjalizacja
for i in range(okres_miesiecy):
    uzbierana_kwota += deponowana_kwota
    zysk_netto = wartosc_lokaty[i] - uzbierana_kwota
    logging.info(f"{i + 1} -> Miesiąc: {i + 1}, Składka ratalna: {deponowana_kwota:.2f} zł, "
                 f"Uzbierana kwota na lokacie: {wartosc_lokaty[i]:.2f} zł, Zysk netto: {zysk_netto:.2f} zł")

print(f"Przyszła cena mieszkania za {okres_lat} lat: {przyszla_cena_mieszkania:.2f} zł")
print(f"Wpłata miesięczna do banku: {wpłata_miesieczna_do_banku:.2f} zł")

# Wykres
plt.figure(figsize=(10, 6))
plt.plot(czas, cena_mieszkania, label='Cena mieszkania')
plt.plot(czas, wartosc_lokaty, label='Wartość lokaty')
plt.title('Zmiana ceny mieszkania i wartości lokaty w czasie')
plt.xlabel('Czas (miesiące)')
plt.ylabel('Wartość (zł)')
plt.legend()
plt.grid(True)
plt.show()
