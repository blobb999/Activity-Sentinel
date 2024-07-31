Activity Sentinel

![Activity Sentinel](https://github.com/user-attachments/assets/1136ebd0-e171-4cc7-b4e6-1032e2f41888)![Activity Sentinel-config](https://github.com/user-attachments/assets/667ac42b-c59e-4ed4-8d94-dc6aa740aed6)

Activity Sentinel ist ein leistungsfähiges Überwachungs- und Verwaltungstool, das verschiedene Systemaktivitäten überwacht und darauf basierend Skripte ausführt. Es wurde speziell entwickelt, um Multimedia-Entertainment-Systeme unter Windows zu verwalten, auf die gelegentlich auch remote zugegriffen wird.
Funktionen

    Audio-Aktivitätsüberwachung: Erkennt und überwacht Audioaktivitäten.
    Maus- und Tastaturüberwachung: Überwacht Mausbewegungen und Tastaturanschläge, um Benutzeraktivität zu erkennen.
    Bildschirmaktivitätsüberwachung: Überwacht die GPU-Auslastung, um die Bildschirmaktivität zu bestimmen.
    Skriptausführung: Führt benutzerdefinierte Skripte basierend auf festgelegten Aktivitäts- und Inaktivitätsbedingungen aus.
    Anpassbare Schwellenwerte: Benutzer können Schwellenwerte für die Dauer der Audioaktivität und die GPU-Auslastung festlegen.
    Konfigurierbare Inaktivitätszeit: Definieren Sie die Zeitspanne, nach der ein Inaktivitätsskript ausgeführt wird.
    Checkboxen für flexible Einstellungen: Wählen Sie aus, welche Aktivitäten überwacht werden sollen und steuern Sie die Reaktionen des Systems entsprechend.
    Grafische Benutzeroberfläche (GUI): Einfache und intuitive Bedienung durch eine benutzerfreundliche Oberfläche.

Zweck und Anwendungsgebiete

Activity Sentinel ist besonders geeignet für:

    Multimedia-Entertainment-Systeme: Optimieren Sie die Energieverwaltung und führen Sie spezifische Skripte basierend auf der Aktivität von Audio, Maus, Tastatur und Bildschirm aus.
    Remote-Access-Systeme: Stellen Sie sicher, dass Ihr System inaktiv bleibt oder sich nach einer bestimmten Zeitspanne abschaltet, wenn es nicht genutzt wird, um Energie zu sparen.
    Automatisierung von Aufgaben: Führen Sie automatisch Wartungsskripte, Backups oder andere Aufgaben aus, wenn keine Benutzeraktivität festgestellt wird.

Nutzungsmöglichkeiten der Checkboxen

Die Checkboxen bieten eine Vielzahl von Anwendungsmöglichkeiten und Vorteilen:

    Flexibilität und Anpassungsfähigkeit: Die Checkboxen ermöglichen es Benutzern, die Überwachung und Reaktionen des Systems flexibel an ihre individuellen Bedürfnisse und spezifischen Anwendungsfälle anzupassen.
    Energieeinsparung und Ressourcenschonung: Durch die gezielte Überwachung und das Deaktivieren bestimmter Aktivitäten können Energie und Systemressourcen effizienter genutzt werden.
    Erhöhung der Systemsicherheit: Stellen Sie sicher, dass das System bei Inaktivität sicher bleibt, indem Sie Sicherheitsmaßnahmen wie das Sperren des Bildschirms aktivieren.
    Optimierung der Systemleistung: Passen Sie die Überwachungsfunktionen an, um die Systemleistung zu optimieren und unnötige Belastungen zu vermeiden.
    Remote-Verwaltung: Überwachen und steuern Sie Remote-Aktivitäten effizient, um sicherzustellen, dass das System bei Nichtnutzung in den Ruhezustand versetzt wird.
    Benutzerfreundlichkeit und Komfort: Erhöhen Sie die Benutzerfreundlichkeit durch intuitive Bedienung und schnelle Anpassungsmöglichkeiten.
    Szenario-basierte Einstellungen: Erstellen Sie unterschiedliche Profile oder Szenarien für verschiedene Nutzungskontexte wie Arbeit, Unterhaltung oder Präsentationen.
    Automatisierung von Routineaufgaben: Nutzen Sie die Kombination von Überwachungsfunktionen und Skriptausführung zur Automatisierung von Routineaufgaben.

Installation

    Voraussetzungen: Stellen Sie sicher, dass Python 3.x und die erforderlichen Pakete installiert sind. Installieren Sie die benötigten Pakete mit:

    bash

pip install -r requirements.txt

Ausführung: Führen Sie das Skript Activity Sentinel.py aus, um die Anwendung zu starten:

bash

python "Activity Sentinel.py"

Erstellung einer ausführbaren Datei (optional): Um die Anwendung ohne Python-Installation auszuführen, können Sie PyInstaller verwenden, um eine ausführbare Datei zu erstellen:

bash

    pyinstaller --noconsole --onefile "Activity Sentinel.py"

    Die ausführbare Datei finden Sie im dist-Verzeichnis.

Konfiguration

    Audioaktivität: Stellen Sie die Dauer ein, nach der Audioaktivität erkannt werden soll.
    GPU-Schwellenwert: Legen Sie den Schwellenwert für die GPU-Auslastung fest, um Bildschirmaktivität zu erkennen.
    Inaktivitätszeit: Geben Sie die Zeitspanne ein, nach der bei Inaktivität ein Skript ausgeführt werden soll.
    Skriptauswahl: Wählen Sie benutzerdefinierte Skripte für Aktivitäts- und Inaktivitätsbedingungen aus.
    Checkboxen:
        Audio bei Inaktivität berücksichtigen: Aktivieren Sie diese Option, um Audioaktivität bei der Bestimmung der Systeminaktivität zu berücksichtigen.
        Maus bei Inaktivität berücksichtigen: Aktivieren Sie diese Option, um Mausaktivität bei der Bestimmung der Systeminaktivität zu berücksichtigen.
        Tastatur bei Inaktivität berücksichtigen: Aktivieren Sie diese Option, um Tastaturaktivität bei der Bestimmung der Systeminaktivität zu berücksichtigen.
        Bildschirm bei Inaktivität berücksichtigen: Aktivieren Sie diese Option, um Bildschirmaktivität bei der Bestimmung der Systeminaktivität zu berücksichtigen.
        Audio bei Aktivität berücksichtigen: Aktivieren Sie diese Option, um Audioaktivität bei der Bestimmung der Systemaktivität zu berücksichtigen.
        Maus bei Aktivität berücksichtigen: Aktivieren Sie diese Option, um Mausaktivität bei der Bestimmung der Systemaktivität zu berücksichtigen.
        Tastatur bei Aktivität berücksichtigen: Aktivieren Sie diese Option, um Tastaturaktivität bei der Bestimmung der Systemaktivität zu berücksichtigen.
        Bildschirm bei Aktivität berücksichtigen: Aktivieren Sie diese Option, um Bildschirmaktivität bei der Bestimmung der Systemaktivität zu berücksichtigen.

Verwendung

    Überwachungs- und Konfigurationseinstellungen: Passen Sie die Einstellungen im Überwachungs- und Konfigurations-Tab an Ihre Bedürfnisse an.
    Skriptauswahl: Wählen Sie die Skripte aus, die bei Aktivität oder Inaktivität ausgeführt werden sollen.
    Starten: Die Anwendung überwacht nun die Systemaktivitäten und führt die ausgewählten Skripte basierend auf den festgelegten Bedingungen aus.

Lizenz:

Dieses Projekt steht unter der MIT-Lizenz. Es ist lizenzfrei und für jedermann zur Verwendung und Weiterentwicklung freigegeben.

Beiträge:

Beiträge sind willkommen! Wenn Sie Ideen, Fehlerberichte oder Verbesserungen haben, öffnen Sie bitte ein Issue oder senden Sie einen Pull-Request.

Haftungsausschluss:

Dieses Tool wird ohne jegliche Garantie bereitgestellt. Die Nutzung erfolgt auf eigene Gefahr.