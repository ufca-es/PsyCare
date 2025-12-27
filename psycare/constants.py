import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = os.path.join(BASE_DIR, 'config')

FORMAL_JSON = os.path.join(CONFIG_DIR, 'respostas_formal.json')
AMIGAVEL_JSON = os.path.join(CONFIG_DIR, 'respostas_amigavel.json')
DIRETO_JSON = os.path.join(CONFIG_DIR, 'respostas_direto.json')
APRENDIZADO_JSON = os.path.join(CONFIG_DIR, 'aprendizado.json')