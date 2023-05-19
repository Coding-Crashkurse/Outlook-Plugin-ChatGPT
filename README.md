# Dokumentation des Exchange Email und Calendar ChatGPT Plugins

Dieses Plugin ermöglicht es dir, über die ChatGPT Schnittstelle E-Mails zu senden, Kalendereinträge zu erstellen und die neuesten E-Mails in deinem Posteingang abzurufen.

## Voraussetzungen

Um dieses Plugin zu nutzen, benötigst du einen Outlook-Account. Die Anmeldedaten für diesen Account (E-Mail und Passwort) müssen in einer `.env`-Datei gespeichert werden, die im Hauptverzeichnis deines Projekts liegt. Die Variablen in dieser Datei sollten `EMAIL` und `PASSWORD` heißen.

```env
EMAIL=deine-email@beispiel.com
PASSWORD=deinPasswort
```

## Endpunkte

### POST /email/

Mit diesem Endpunkt kannst du eine E-Mail senden. Du musst ein JSON-Objekt mit den folgenden Eigenschaften im Request Body bereitstellen:

- `subject`: Der Betreff der E-Mail.
- `body`: Der Inhalt der E-Mail.
- `email_address`: Die E-Mail-Adresse des Empfängers.

### POST /calendar/

Mit diesem Endpunkt kannst du einen Kalendereintrag erstellen. Du musst ein JSON-Objekt mit den folgenden Eigenschaften im Request Body bereitstellen:

- `subject`: Der Betreff des Kalendereintrags.
- `body`: Weitere Details zum Kalendereintrag.
- `location`: Der Ort des Kalendereintrags.
- `start_time`: Der Startzeitpunkt des Kalendereintrags.
- `end_time`: Der Endzeitpunkt des Kalendereintrags.
- `attendees`: Eine Liste von E-Mail-Adressen der Teilnehmer.

### GET /latest_email/

Mit diesem Endpunkt kannst du die neuesten 10 E-Mails in deinem Posteingang abrufen. Der Endpunkt gibt eine Liste von E-Mail-Objekten zurück, wobei jedes Objekt die folgenden Eigenschaften hat:

- `subject`: Der Betreff der E-Mail.
- `body`: Der Inhalt der E-Mail.
- `author`: Die E-Mail-Adresse des Autors.
- `name`: Der Name des Autors.
