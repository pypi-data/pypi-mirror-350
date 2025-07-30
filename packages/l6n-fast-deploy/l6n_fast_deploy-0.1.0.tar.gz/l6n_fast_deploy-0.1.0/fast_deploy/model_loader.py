from abc import ABC, abstractmethod
from typing import Any


class ModelLoader(ABC):
    @abstractmethod
    def load_model(self, model_path: str) -> Any:
        """Carrega um modelo a partir de um arquivo.

        Parameters:
            model_path: Caminho para o arquivo de objeto serializado

        Returns:
            O modelo carregado
        """
        pass
