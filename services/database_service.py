"""
Serviço de acesso ao banco de dados
"""
import pyodbc
import base64
import logging
from io import BytesIO
from typing import Tuple, Optional
from config.settings import db_config

logger = logging.getLogger(__name__)


class DatabaseService:
    """Serviço para operações no banco de dados"""
    
    def __init__(self, connection_string: str = None):
        """
        Inicializa o serviço de banco de dados
        
        Args:
            connection_string: String de conexão SQL (opcional)
        """
        self.connection_string = connection_string or db_config.CONNECTION_STRING
        
    def _executar_com_retry(self, query: str, params: tuple, max_retries: int = 3):
        """
        Executa uma query com retry em caso de falha
        
        Args:
            query: SQL query
            params: Parâmetros da query
            max_retries: Número máximo de tentativas
            
        Returns:
            Resultado da query
        """
        ultima_excecao = None
        
        for tentativa in range(max_retries):
            try:
                with pyodbc.connect(self.connection_string, timeout=db_config.TIMEOUT) as conn:
                    with conn.cursor() as cur:
                        cur.execute(query, params)
                        return cur.fetchall()
            except pyodbc.Error as e:
                ultima_excecao = e
                logger.warning(f"Tentativa {tentativa + 1}/{max_retries} falhou: {e}")
                if tentativa < max_retries - 1:
                    continue
        
        raise ultima_excecao
    
    def carregar_anexos(
        self,
        num_solic: int
    ) -> Tuple[Optional[BytesIO], Optional[BytesIO]]:
        """
        Busca na base os anexos da solicitação e devolve dois arquivos em memória
        
        Args:
            num_solic: Número da solicitação
            
        Returns:
            Tupla (arquivo_apolice, arquivo_especificacao) como BytesIO
        """
        query = """
        SELECT anexo.num_solic,
               anexo.num_hist_solic,
               anexo.num_seq,
               anexo.nom_arquivo,
               anexo.arq_anexo_base64
        FROM DBCIT_SSC_MTS..tb_solic_cotacao_anexo anexo
        WHERE anexo.num_solic = ?
          AND (
                anexo.nom_arquivo LIKE '%AP%LICE%.pdf'
                OR anexo.nom_arquivo LIKE '%FRONT%'
                OR anexo.nom_arquivo LIKE '%ESPEC%'
          )
          AND anexo.num_hist_solic = (
                SELECT MAX(t.num_hist_solic)
                FROM DBCIT_SSC_MTS..tb_solic_cotacao_anexo t
                WHERE t.num_solic = anexo.num_solic
          )
        ORDER BY anexo.num_solic, anexo.num_seq ASC;
        """
        
        logger.info(f"Consultando anexos no banco para num_solic={num_solic}...")
        
        f_apolice = None
        f_especificacao = None
        
        try:
            rows = self._executar_com_retry(query, (num_solic,))
            logger.info(f"{len(rows)} anexos retornados da base.")
            
            for row in rows:
                nome = (getattr(row, "nom_arquivo", "") or "").upper()
                b64_data = getattr(row, "arq_anexo_base64", None)
                
                if not b64_data:
                    continue
                
                try:
                    pdf_bytes = base64.b64decode(b64_data)
                except Exception as e:
                    logger.error(f"Falha ao decodificar base64 de {nome}: {e}")
                    continue
                
                bio = BytesIO(pdf_bytes)
                bio.name = nome or "anexo.pdf"
                
                # Classifica o tipo de anexo
                if "ESPEC" in nome and f_especificacao is None:
                    f_especificacao = bio
                    logger.info(f"Especificação encontrada: {nome}")
                elif (("AP" in nome and "LICE" in nome and nome.endswith(".PDF")) 
                      or "FRONT" in nome) and f_apolice is None:
                    f_apolice = bio
                    logger.info(f"Apólice encontrada: {nome}")
            
            return f_apolice, f_especificacao
            
        except pyodbc.Error as e:
            logger.error(f"Erro ao consultar banco de dados: {e}")
            raise