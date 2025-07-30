# FastDeploy
[![Read the Docs](https://readthedocs.org/projects/fast-deploy/badge/?version=latest)](https://fast-deploy.readthedocs.io/pt-br/latest)
[![codecov](https://codecov.io/gh/laranapoli/fast-deploy/graph/badge.svg?token=O5NJOZWTE9)](https://codecov.io/gh/laranapoli/fast-deploy)
![CI](https://github.com/laranapoli/fast-deploy/actions/workflows/ci-pipeline.yaml/badge.svg)

FastDeploy é uma ferramenta CLI que simplifica o deploy de modelos de machine learning como APIs REST em containers Docker.

## Instalação
Clone o repositório e execute:
```bash
pipx install fast-deploy
```

## Pré-requisitos

Antes de executar a aplicação, verifique se você possui os seguintes pré-requisitos instalados:

- **Docker**: Certifique-se de que o Docker está instalado e em funcionamento em sua máquina. Você pode verificar isso executando o seguinte comando no terminal:

    ```bash
    docker --version
    ```

    Se o Docker não estiver instalado, você pode seguir as instruções de instalação na [documentação oficial do Docker](https://docs.docker.com/engine/install/)

## Comando Principal
 
### deploy

Inicia em um container Docker uma API com as rotas para fazer o upload de seu modelo e para obter seus resultados.

**Uso**:
```bash
deploy [image_name] [port] [--verbose]
```
- image_name: Nome da imagem Docker (default: 'fastdeploy')
- port: Porta da API (default: 8000)
- --verbose: Exibe logs detalhados (e conecta container ao terminal)

> [!IMPORTANT]  
> Atualmente a única implementação de carregamento de modelos é para classificadores treinados com Scikit-Learn!