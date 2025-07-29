import os
import sys
import click
import subprocess
import logging
import uvicorn
import psutil
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import set_key, load_dotenv

from watchman_http_server.main import create_env_file


class WatchmanCLI(click.Group):
    def resolve_command(self, ctx, args):
        if not args and not ctx.protected_args:
            args = ['default']
        return super(WatchmanCLI, self).resolve_command(ctx, args)


@click.command(cls=WatchmanCLI)
def cli():
    pass


@cli.command(name='runserver')
@click.option('--port', default=8001, help="Port sur lequel démarrer le serveur (par défaut : 8001)", type=int,
              required=True)
@click.option('--api-key', help="Clé API pour accéder au serveur.", type=str, required=True)
@click.option('--ip', help="Adresses IPs pour autorisées pour accéder au serveur.", type=str, required=False)
@click.option('-d', '--detach', is_flag=True, help="Exécuter en arrière-plan.")
def runserver(port, api_key, ip, detach):
    # Vérifier si la clé API est fournie en ligne de commande
    if api_key:
        print(f'api_key : {api_key}')
        click.echo("creation de .env")
        create_env_file(api_key)  # Créer ou mettre à jour le fichier .env avec la clé fournie
    else:
        click.echo("Erreur : la clé API doit être fournie.")
        sys.exit(1)


    dotenv_path = os.path.join(os.path.dirname(__file__), "config", ".env")
    load_dotenv(dotenv_path)

    # Liste des IPs existantes
    existing_ips = os.getenv("ALLOWED_IPS", "").split(",")

    # Ajouter ou mettre à jour la liste des IPs dans le .env
    if ip:
        set_key(dotenv_path, "ENABLE_IP_FILTERING", "true")

        # Séparer les IPs passées et les nettoyer
        ip_list = [addr.strip() for addr in ip.split(",") if addr.strip()]

        # Ajouter les nouvelles IPs non présentes dans la liste existante
        for new_ip in ip_list:
            if new_ip not in existing_ips:
                existing_ips.append(new_ip)

        # Sauvegarder la liste des IPs mises à jour dans le .env
        set_key(dotenv_path, "ALLOWED_IPS", ",".join(existing_ips))
        print(f"✅ IPs autorisées : {existing_ips}")
    else:
        set_key(dotenv_path, "ENABLE_IP_FILTERING", "false")
        print("❌ Aucun IP autorisé.")

    if detach:
        log_file = os.path.expanduser("~/watchman_http_server.log")
        with open(log_file, "w") as f:
            subprocess.Popen(
                ["python", "-m", "uvicorn", "watchman_http_server.main:app", "--host", "0.0.0.0", "--port", str(port)],
                stdout=f, stderr=f, close_fds=True
            )
        print(f"✅ Serveur lancé en arrière-plan (logs: {log_file})")
    else:
        logging.info(f"Starting Watchman HTTP Server on port {port}...")
        uvicorn.run("watchman_http_server.main:app", host="0.0.0.0", port=port, log_level="info")


@cli.command(name="stopserver")
def stopserver():
    """Arrêter le serveur Watchman HTTP tournant en arrière-plan."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if proc.info['cmdline'] and "uvicorn" in " ".join(proc.info['cmdline']):
            print(f"🔴 Arrêt du serveur (PID: {proc.info['pid']})")
            os.kill(proc.info['pid'], 9)  # Signal 9 = kill immédiat
            break
    else:
        print("⚠️ Aucun serveur Watchman HTTP trouvé en cours d'exécution.")


# Assurez-vous que vous avez une configuration de logging correcte
logging.basicConfig(level=logging.INFO)


@cli.command(name='schedule')
@click.option('--hour', type=int, required=True, help="L'heure à laquelle démarrer le serveur (0-23).")
@click.option('--minute', type=int, required=True, help="La minute à laquelle démarrer le serveur (0-59).")
@click.option('--day', type=int, required=False, default="*", help="Jour du mois (1-31), * pour chaque jour.")
@click.option('--month', type=int, required=False, default="*", help="Mois (1-12), * pour chaque mois.")
@click.option('--port', default=8001, help="Port sur lequel démarrer le serveur (par défaut : 8001)", type=int)
@click.option('--api-key', type=str, required=True, help="Clé API pour accéder au serveur.")
@click.option('-d', 'detach', is_flag=True, help="Exécuter en arrière-plan.")
def schedule_task(hour, minute, day, month, port, api_key, detach):
    """Planifier une tâche pour démarrer le serveur à un moment précis"""

    # Configurer l'environnement
    create_env_file(api_key)

    # Configurer le planificateur
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=hour, minute=minute, day=day, month=month)

    def runserver_on_schedule():
        log_file = os.path.expanduser("~/watchman_http_server.log")
        logging.info(f"🔄 Tâche exécutée à {hour}:{minute} (journée: {day}, mois: {month})")

        try:
            with open(log_file, "w") as f:
                subprocess.Popen(
                    ["python", "-m", "uvicorn", "watchman_http_server.commands:app", "--host", "0.0.0.0", "--port",
                     str(port)],
                    stdout=f, stderr=f, close_fds=True
                )
            logging.info(f"✅ Serveur démarré (logs: {log_file})")
        except Exception as e:
            logging.error(f"❌ Erreur lors du démarrage du serveur: {e}")

    scheduler.add_job(runserver_on_schedule, trigger=trigger, name="runserver_on_schedule")

    if detach:
        log_file = os.path.expanduser("~/watchman_http_server.log")
        logging.info("🛠 Démarrage du planificateur en arrière-plan...")

        subprocess.Popen(
            ["watchman-http-server", "schedule",
             "--hour", str(hour), "--minute", str(minute),
             "--day", str(day), "--month", str(month),
             "--port", str(port), "--api-key", api_key],
            stdout=open(log_file, "w"),
            stderr=subprocess.STDOUT,
            close_fds=True
        )

        logging.info(f"✅ Serveur planifié en arrière-plan (logs: {log_file})")
    else:
        logging.info("🟢 Planificateur en cours d'exécution...")
        scheduler.start()
        logging.info(f"✅ Tâche planifiée pour {hour}:{minute} (Journée: {day}, Mois: {month})")

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            logging.info("🛑 Planificateur arrêté.")
