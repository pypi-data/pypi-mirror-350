import os
import subprocess
import platform
import click
from Osdental.Shared.Logger import logger
from Osdental.Shared.Message import Message

SRC_PATH = 'src'
APP_PATH = os.path.join(SRC_PATH, 'Application')
DOMAIN_PATH = os.path.join(SRC_PATH, 'Domain')
INFRA_PATH = os.path.join(SRC_PATH, 'Infrastructure')
GRAPHQL_PATH = os.path.join(INFRA_PATH, 'Graphql')
SCHEMAS_PATH = os.path.join(GRAPHQL_PATH, 'Schemas')

@click.group()
def cli():
    """Comandos personalizados para gestionar el proyecto."""
    pass

@cli.command()
def clean():
    """Borrar todos los __pycache__."""
    if platform.system() == 'Windows':
        subprocess.run('for /d /r . %d in (__pycache__) do @if exist "%d" rd /s/q "%d"', shell=True)
    else:
        subprocess.run("find . -name '__pycache__' -type d -exec rm -rf {} +", shell=True)

    logger.info(Message.PYCACHE_CLEANUP_SUCCESS_MSG)


@cli.command(name='start-app')
@click.argument('app')
def start_app(app: str):
    """Crear un servicio con estructura hexagonal."""
    app = app.capitalize()
    # Definir las rutas donde se deben crear los archivos
    directories = [
        os.path.join(APP_PATH, 'UseCases'),
        os.path.join(APP_PATH, 'Interfaces'),
        os.path.join(DOMAIN_PATH, 'Interfaces'),
        os.path.join(GRAPHQL_PATH, 'Resolvers'),
        os.path.join(SCHEMAS_PATH),
        os.path.join(INFRA_PATH, 'Repositories'),
        os.path.join(SCHEMAS_PATH, app, 'Queries'),
        os.path.join(SCHEMAS_PATH, app, 'Mutations')
    ]
    
    # Crear las carpetas si no existen
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Crear archivos en cada carpeta con contenido inicial
    files = {
        os.path.join(APP_PATH, 'UseCases', f'{app}UseCase.py'): f'class {app}UseCase:\n    pass\n',
        os.path.join(APP_PATH, 'Interfaces', f'{app}UseCaseInput.py'): f'class {app}UseCaseInput:\n    pass\n',
        os.path.join(DOMAIN_PATH, 'Interfaces', f'{app}RepositoryOutput.py'): f'class {app}RepositoryOutput:\n    pass\n',
        os.path.join(GRAPHQL_PATH, 'Resolvers', f'{app}Resolver.py'): f'class {app}Resolver:\n    pass\n',
        os.path.join(SCHEMAS_PATH, app, 'Queries', 'Query.graphql'): 'type Query {\n    _empty: String\n}\n',
        os.path.join(SCHEMAS_PATH, app, 'Mutations', 'Mutation.graphql'): 'type Mutation {\n    _empty: String\n}\n',
        os.path.join(INFRA_PATH, 'Repositories', f'{app}Repository.py'): f'class {app}Repository:\n    pass\n'
    }
    
    # Crear y escribir en los archivos
    for file_path, content in files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(content)

    
    logger.info(Message.HEXAGONAL_SERVICE_CREATED_MSG)


@cli.command()
@click.argument('port')
def start(port:int):
    """Levantar el servidor FastAPI."""
    try:
        subprocess.run(['uvicorn', 'app:app', '--port', str(port), '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'{Message.SERVER_NETWORK_ACCESS_ERROR_MSG}: {e}')


@cli.command()
@click.argument('port')
def serve(port:int):
    """Levantar el servidor FastAPI accesible desde cualquier máquina."""
    try:
        # Levanta el servidor en el puerto 8000 accesible desde cualquier IP
        subprocess.run(['uvicorn', 'app:app', '--host', '0.0.0.0', '--port', str(port), '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'{Message.SERVER_NETWORK_ACCESS_ERROR_MSG}: {e}')


if __name__ == "__main__":
    cli()
