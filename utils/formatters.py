"""
Funções de formatação de dados
"""
import re
import logging

logger = logging.getLogger(__name__)


def formatar_moeda(valor) -> str:
    """
    Formata um valor para o padrão de moeda brasileira (R$ x.xxx,xx)
    
    Args:
        valor: Valor a ser formatado (pode ser string, int, float)
        
    Returns:
        String formatada no padrão brasileiro ou "Não consta"
    """
    if not valor or valor in ["Não consta", "null", None, "", "0", 0]:
        return "Não consta"
    
    limpo = re.sub(r'[^\d.,]', '', str(valor)).strip()
    
    if not limpo:
        return "Não consta"
    
    try:
        # Detecta se usa vírgula ou ponto como separador decimal
        if ',' in limpo and '.' in limpo:
            # Verifica qual é o separador decimal (o último)
            if limpo.rfind(',') > limpo.rfind('.'):
                limpo = limpo.replace('.', '').replace(',', '.')
            else:
                limpo = limpo.replace(',', '')
        elif ',' in limpo:
            limpo = limpo.replace(',', '.')
        
        float_val = float(limpo)
        return f"R$ {float_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    except (ValueError, TypeError) as e:
        logger.warning(f"Erro ao formatar valor '{valor}': {e}")
        return str(valor)


def sanitizar_nome_arquivo(nome: str) -> str:
    """
    Remove caracteres inválidos de um nome de arquivo
    
    Args:
        nome: Nome do arquivo original
        
    Returns:
        Nome sanitizado
    """
    return re.sub(r'[\\/*?:"<>|]', "", nome)


def extrair_numero_limpo(texto: str) -> str:
    """
    Extrai apenas números de um texto
    
    Args:
        texto: Texto contendo números
        
    Returns:
        String com apenas números
    """
    return re.sub(r'[^\d]', '', str(texto))