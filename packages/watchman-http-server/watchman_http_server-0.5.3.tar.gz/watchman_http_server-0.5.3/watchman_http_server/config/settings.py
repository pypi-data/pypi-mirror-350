import environ

env = environ.Env()

env.read_env()

WATCHMAN_API_KEY = env('WATCHMAN_API_KEY', default=None)
