import environ

env = environ.Env()

env.read_env()

WATCHMAN_API_KEY = env('WATCHMAN_API_KEY', default=None)

ALLOWED_IPS_RAW = env('ALLOWED_IPS', default="")
ALLOWED_IPS = [
    ip.strip().strip("'").strip('"')
    for ip in ALLOWED_IPS_RAW.split(",")
    if ip.strip()
]

