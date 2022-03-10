Konfiguracja Raspberry Pi:

 Raspberry Pi 4b 2GB

Czujnik ruchu HC-SR501:

 - zasilanie 5V - PIN 2 PWR
 - sygnał - GPIO 18 (PIN 12)
 - masa - PIN 14


Buzzer (bez generatora):

 - "+" - GPIO 4 (PIN 7)
 - "-" - PIN 9

Lokalizacja folderu:
 /home/

Uruchamianie skryptu ze startem urządzenia:
 na końcu pliku 

 /etc/rc.local

 dopisać:

 sudo python /home/czujnik/move2.py & > /home/pi/Desktop/startlog.txt 2>&1
 exit 0

 plik startlog.txt opcjonalny
