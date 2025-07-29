# Watchman HTTP Server

Watchman HTTP Server est un serveur FastAPI qui expose la liste des applications installées ainsi que des informations sur le système.

## Installation

Installez le package via pip :
```sh
pip install watchman_http_server
```

Ou depuis le code source :
```sh
git clone https://github.com/votre-repo/watchman_http_server.git
cd watchman_http_server
pip install -e .
```

## Utilisation

Lancer le serveur avec un port et une clé API spécifiés :
```sh
watchman-http-server runserver --port 8000 --api-key "VOTRE_CLE_API"
```

## Configuration

- `--port` : Définit le port d'écoute du serveur (par défaut : 8001).
- `--api-key` : Spécifie la clé API requise pour accéder aux endpoints.
- `--hour` : L'heure à laquelle démarrer le serveur (0-23).
- `--minute` : La minute à laquelle démarrer le serveur (0-59).
- `--day` : Jour du mois (1-31), * pour chaque jour.
- `--month` : Mois (1-12), * pour chaque mois.
- `--ip` : Adresses IPs pour autorisées pour accéder au serveur.
- `-d` : Exécuter en arrière-plan.

## Endpoints

### `GET /apps`
Retourne la liste des applications installées et les informations du système.

#### Headers requis
```http
WATCHMAN-API-KEY: VOTRE_CLE_API
```

#### Exemple de réponse
```json
{
  "system_info": {
    "hostname": "mon-pc",
    "ip": "192.168.1.10",
    "mac": "A1:B2:C3:D4:E5:F6",
    "architecture": "x86_64",
    "os": "Windows 10"
  },
  "applications": [
    {
      "name": "Google Chrome",
      "version": "99.0.4844.84",
      "vendor": "Google LLC",
      "type": "application"
    }
  ]
}
```

## Déploiement sur un réseau local

Pour rendre le serveur accessible sur un réseau local :
1. Lancer le serveur avec `0.0.0.0` comme hôte :
   ```sh
   watchman-http-server runserver --port 8000 --api-key "VOTRE_CLE_API"
   ```
2. Planifier une tâche pour lancer le serveur en arrière plan avec `0.0.0.0` comme hôte :
     ```sh
   watchman-http-server schedule --port 8000 --api-key "VOTRE_CLE_API" --hour "heure" --minute "minute" --day "day" --month "month" --d
   ```
   
3. Stoper le serveur en cours d'éxécution  en arrière plan:
     ```sh
   watchman-http-server stopserver
   ```
4. Assurez-vous que le port est ouvert dans le pare-feu :
   - **Windows** :
     ```sh
     netsh advfirewall firewall add rule name="Watchman" dir=in action=allow protocol=TCP localport=8000
     ```
   - **Linux** :
     ```sh
     sudo ufw allow 8000/tcp
     ```

## Contributions

Les contributions sont les bienvenues ! Clonez le projet, créez une branche et proposez vos modifications via une pull request.

## Licence

Ce projet est sous licence MIT.
