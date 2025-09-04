from pathlib import Path
from django.core.management.utils import get_random_secret_key

ENV_PATH = Path('.env')


def regenerate():
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Gera novos valores
    new_secret_key = get_random_secret_key()

    if ENV_PATH.exists():
        lines = ENV_PATH.read_text().splitlines()
    else:
        lines = []

    updated_lines = []
    found_secret_key = False

    for line in lines:
        if line.startswith('SECRET_KEY='):
            updated_lines.append(f'SECRET_KEY={new_secret_key}')
            found_secret_key = True
        else:
            updated_lines.append(line)

    # Se não existirem ainda, adiciona no final
    if not found_secret_key:
        updated_lines.append(f'SECRET_KEY={new_secret_key}')

    ENV_PATH.write_text('\n'.join(updated_lines) + '\n')
    print('✅ SECRET_KEY regenerado no arquivo .env')


if __name__ == '__main__':
    regenerate()