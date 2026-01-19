"""
Configurações centralizadas do sistema
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class GeminiConfig:
    """Configurações da API Gemini"""
    API_KEY: str = os.getenv('GEMINI_API_KEY')
    MODEL: str = "gemini-2.5-flash"
    TIMEOUT: int = 600
    TEMPERATURE: float = 0.0
    RESPONSE_MIME_TYPE: str = "application/json"


@dataclass
class DatabaseConfig:
    """Configurações do banco de dados"""
    CONNECTION_STRING: str = os.getenv('SQL_CONNECTION_STRING')
    TIMEOUT: int = 30
    MAX_RETRIES: int = 3


@dataclass
class AppConfig:
    """Configurações gerais da aplicação"""
    JSON_OUTPUT_DIR: str = "json"
    MAX_FILE_SIZE_MB: int = 50
    NUM_SOLIC_TESTE: int = 559616
    PAGE_TITLE: str = "Extrator V20 (Visão Nativa)"
    PAGE_LAYOUT: str = "wide"


# Instâncias globais
gemini_config = GeminiConfig()
db_config = DatabaseConfig()
app_config = AppConfig()


def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    if not gemini_config.API_KEY:
        raise ValueError("GEMINI_API_KEY não configurada. Configure no arquivo .env")
    if not db_config.CONNECTION_STRING:
        raise ValueError("SQL_CONNECTION_STRING não configurada. Configure no arquivo .env")