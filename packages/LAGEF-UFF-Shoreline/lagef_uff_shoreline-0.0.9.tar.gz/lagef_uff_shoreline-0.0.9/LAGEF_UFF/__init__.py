import ee

def autenticar_gee(project: str):
    """
    Autentica e inicializa o Google Earth Engine (GEE) com o projeto fornecido.

    Args:
        project (str): Nome do projeto no GEE.

    Raises:
        Exception: Caso a autenticação falhe.
    """
    try:
        ee.Authenticate()
        ee.Initialize(project=project)
        print(f"Autenticação bem-sucedida com o projeto: {project}")
    except Exception as e:
        raise Exception(f"Erro na autenticação ou inicialização do GEE: {e}")

# Solicita que o usuário insira o nome do projeto no momento da importação
try:
    project_name = input("Insira o nome do seu projeto no Google Earth Engine: ")
    autenticar_gee(project_name)
except Exception as e:
    raise ImportError(f"Erro ao autenticar o Google Earth Engine: {e}")

# Importa as funções da biblioteca
from .LAGEF_UFF_Shoreline import (
    function_lc,
    estatisticas_mare,
    area_linha_de_costa_loop,
    linha_de_costa_loop,
    exportar_resultados,
    geemap
)

