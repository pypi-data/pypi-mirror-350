import uuid


def generate_api_key():
    """Génère une clé API unique."""
    return str(uuid.uuid4())


if __name__ == "__main__":
    api_key = generate_api_key()
    print(f"Votre clé API générée est : {api_key}")
