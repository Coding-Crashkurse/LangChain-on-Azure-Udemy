1. Storage Account erstellen
   1.1. Container mit Namen "data" erstellen

2. Azure Database for PostgreSQL flexible server erstellen
   2.1. User und passwort einrichten
   2.2. PGVector Extension aktivieren
   2.3. vectordb database hinzufügen

3. Container Registry erstellen
   3.1. Admin User aktivieren

4. App Services App erstellen
   4.1 App erstellen - Zeigen, dass App nicht erreichbar
   4.2 Environment Variablen zeigen -> WEBSITE_PORT hinzufügen für Access

5. Uploadservice bauen und hochladen
   5.1 Im src folder environment anpassen mit URL des backend services

Erklären, dass wir nun Verbindung haben zu

6. Function erstellen
   6.1 Environment Variablen anlegen

func new --template "EventGridTrigger"
func azure functionapp publish indexingfunctionudemy

7. Frontend App übernehmen
   7.1. Im src folder environment anpassen mit URL des backend services
   7.2. Bauen und in Registry schieben

8. IPs einschränken
