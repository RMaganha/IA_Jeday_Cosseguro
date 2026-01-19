"""
Funções de validação de dados
"""
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass


def validar_resposta_json(
    json_data: Dict[str, Any],
    campos_obrigatorios: List[str],
    nome_secao: str = "Resposta"
) -> bool:
    """
    Valida se todos os campos obrigatórios estão presentes no JSON
    
    Args:
        json_data: Dicionário JSON a ser validado
        campos_obrigatorios: Lista de campos que devem estar presentes
        nome_secao: Nome da seção para mensagens de erro
        
    Returns:
        True se válido
        
    Raises:
        ValidationError: Se algum campo obrigatório estiver ausente
    """
    if not isinstance(json_data, dict):
        raise ValidationError(f"{nome_secao}: Resposta deve ser um dicionário")
    
    campos_ausentes = []
    for campo in campos_obrigatorios:
        if campo not in json_data or json_data[campo] is None:
            campos_ausentes.append(campo)
    
    if campos_ausentes:
        msg = f"{nome_secao}: Campos obrigatórios ausentes: {', '.join(campos_ausentes)}"
        logger.warning(msg)
        raise ValidationError(msg)
    
    return True


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida formato básico de CNPJ (não valida dígitos verificadores)
    
    Args:
        cnpj: String contendo o CNPJ
        
    Returns:
        True se o formato é válido
    """
    if not cnpj:
        return False
    
    # Remove caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, cnpj))
    
    # CNPJ deve ter 14 dígitos
    return len(numeros) == 14


def validar_data_formato(data: str) -> bool:
    """
    Valida se a data está em um formato reconhecível
    
    Args:
        data: String contendo a data
        
    Returns:
        True se o formato parece válido
    """
    if not data or data == "Não consta":
        return False
    
    # Aceita formatos: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    import re
    padroes = [
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2}-\d{2}-\d{4}',
        r'\d{4}-\d{2}-\d{2}'
    ]
    
    return any(re.match(padrao, data) for padrao in padroes)


def validar_arquivo_pdf(file_bytes: bytes, max_size_mb: int = 50) -> bool:
    """
    Valida se o arquivo é um PDF válido e não excede o tamanho máximo
    
    Args:
        file_bytes: Bytes do arquivo
        max_size_mb: Tamanho máximo em MB
        
    Returns:
        True se válido
        
    Raises:
        ValidationError: Se o arquivo for inválido
    """
    if not file_bytes:
        raise ValidationError("Arquivo vazio")
    
    # Verifica tamanho
    tamanho_mb = len(file_bytes) / (1024 * 1024)
    if tamanho_mb > max_size_mb:
        raise ValidationError(f"Arquivo excede tamanho máximo de {max_size_mb}MB")
    
    # Verifica magic number do PDF
    if not file_bytes.startswith(b'%PDF'):
        raise ValidationError("Arquivo não é um PDF válido")
    
    return True