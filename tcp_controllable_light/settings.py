from polog import config, file_writer
from pathlib import Path
from dotenv import dotenv_values
import os

ROOT_DIR = Path(__file__).resolve(strict=True).parent
ENVIRONMENT = os.getenv('ENVIRONMENT', "production")
env = {
    **dotenv_values(f"{ROOT_DIR}/.envs/.{ENVIRONMENT}/.env"),
    **os.environ,
}

# Insert settings
# -----------------------------------------------------------------------------
TCP_LIGHT_SERVER_HOST = env.get('TCP_LIGHT_SERVER_HOST', '127.0.0.1')
TCP_LIGHT_SERVER_PORT = int(env.get('TCP_LIGHT_SERVER_PORT', 9999))

# Stream encoding, for more variants look at https://docs.python.org/3/library/codecs.html#standard-encodings
PROTO_ENCODING = env.get('TCP_LIGHT_PROTO_ENCODING', 'utf-8')

# Package size, by default it is 1K, but can be up to 64K
PROTO_PACKAGE_SIZE = int(env.get('TCP_LIGHT_PROTO_PACKAGE_SIZE', 1024))

# Configuration for logger
# -----------------------------------------------------------------------------
config.add_handlers(file_writer(env.get('LOG_FILE', f'{ROOT_DIR}/.logs')))
