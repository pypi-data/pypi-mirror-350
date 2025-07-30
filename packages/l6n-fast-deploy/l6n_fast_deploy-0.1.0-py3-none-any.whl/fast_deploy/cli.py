import subprocess

from rich.console import Console
from typer import Argument, Option, Typer, prompt

console = Console()
app = Typer()


def check_docker_installed():
    """Verifica se o Docker está instalado no sistema.

    Raises:
        SystemExit: Encerra o programa com código 1 se o Docker não estiver instalado
    """
    try:
        subprocess.run(
            ['docker', '--version'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        console.print(
            '[bold red]Docker não está instalado. Por favor, instale o Docker para usar esta aplicação.'
        )
        raise SystemExit(1)


@app.command()
def deploy(
    image_name: str = Argument('fastdeploy', help='Nome da imagem Docker'),
    port: int = Argument(8000, help='Porta para expor a API'),
    verbose: bool = Option(
        False, '--verbose', help='Flag para exibir logs do container'
    ),
):
    """Constrói e executa um container Docker para disponibilizar a API.

    Esta função verifica se o Docker está instalado, constrói uma imagem Docker
    a partir do diretório atual e executa um container para expor a API na
    porta especificada.

    Parameters:
        image_name (str): Nome da imagem Docker a ser construída. Padrão é 'fastdeploy'
        port (int): Porta para expor a API do container. Padrão é 8000
        verbose (bool): Flag que, se definida, exibe os logs de construção e execução
         do container. Padrão é False

    Raises:
        SystemExit: Encerra o programa se o Docker não estiver instalado
    """
    check_docker_installed()
    console.print('Buildando Docker container...')
    build_command = ['docker', 'build', '-t', image_name, '.']
    if verbose:
        subprocess.run(build_command, check=True)
    else:
        subprocess.run(
            build_command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    console.print('Startando Docker container.')
    if verbose:
        run_command = ['docker', 'run', '-p', f'{port}:8000', image_name]
    else:
        run_command = ['docker', 'run', '-d', '-p', f'{port}:8000', image_name]
    subprocess.run(run_command, check=True)


if __name__ == '__main__':
    app()
