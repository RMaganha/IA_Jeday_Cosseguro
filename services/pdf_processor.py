"""
Serviço de processamento de PDFs de apólices
"""
import logging
from io import BytesIO
from typing import Dict, Any, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.gemini_service import GeminiService
from config.prompts import (
    PROMPT_MESTRE_APOLICE,
    PROMPT_LOCAIS_V4_1,
    PROMPT_COBERTURAS_V3_GENERICO,
    PROMPT_LMI_UNICO_CBI,
    PROMPT_ESPECIFICACAO_FINANCEIRA_VISUAL
)
from utils.formatters import formatar_moeda

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Processador de PDFs de apólices e especificações"""
    
    def __init__(self):
        """Inicializa o processador"""
        self.gemini_service = GeminiService()
    
    def processar_apolice(self, arquivo_apolice) -> Dict[str, Any]:
        """
        Processa o arquivo de apólice extraindo todas as informações
        
        Args:
            arquivo_apolice: BytesIO com o PDF da apólice
            
        Returns:
            Dicionário com dados consolidados da apólice
        """
        logger.info("Iniciando processamento paralelo da apólice...")
        
        # Processamento paralelo dos diferentes aspectos da apólice
        arquivo_apolice.seek(0)
        apolice_bytes = arquivo_apolice.read()
        tarefas = {
            'mestre': (BytesIO(apolice_bytes), PROMPT_MESTRE_APOLICE),
            'locais': (BytesIO(apolice_bytes), PROMPT_LOCAIS_V4_1),
            'coberturas': (BytesIO(apolice_bytes), PROMPT_COBERTURAS_V3_GENERICO),
            'clausulas': (BytesIO(apolice_bytes), PROMPT_LMI_UNICO_CBI)
        }
        
        resultados = self._processar_paralelo(tarefas)
        
        return resultados
    
    def processar_especificacao(self, arquivo_especificacao) -> Dict[str, Any]:
        """
        Processa o arquivo de especificação financeira
        
        Args:
            arquivo_especificacao: BytesIO com o PDF da especificação
            
        Returns:
            Dicionário com dados da especificação
        """
        logger.info("Processando especificação financeira...")
        
        resultado = self.gemini_service.processar_documento(
            arquivo_especificacao,
            PROMPT_ESPECIFICACAO_FINANCEIRA_VISUAL
        )
        
        return resultado
    
    def _processar_paralelo(self, tarefas: Dict[str, Tuple]) -> Dict[str, Any]:
        """
        Processa múltiplas tarefas em paralelo
        
        Args:
            tarefas: Dicionário com nome_tarefa: (arquivo, prompt)
            
        Returns:
            Dicionário com os resultados de cada tarefa
        """
        resultados = {}
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submete todas as tarefas
            futures = {
                executor.submit(
                    GeminiService().processar_documento,
                    arquivo,
                    prompt
                ): nome
                for nome, (arquivo, prompt) in tarefas.items()
            }
            
            # Coleta os resultados conforme completam
            for future in as_completed(futures):
                nome_tarefa = futures[future]
                try:
                    resultado = future.result()
                    resultados[nome_tarefa] = resultado
                    logger.info(f"Tarefa '{nome_tarefa}' concluída")
                except Exception as e:
                    logger.error(f"Erro na tarefa '{nome_tarefa}': {e}")
                    resultados[nome_tarefa] = {"erro": str(e)}
        
        return resultados
    
    def consolidar_dados(
        self,
        dados_apolice: Dict[str, Any],
        dados_especificacao: Dict[str, Any],
        nome_arquivo_apolice: str
    ) -> Dict[str, Any]:
        """
        Consolida todos os dados extraídos em um único JSON estruturado
        
        Args:
            dados_apolice: Dados extraídos da apólice
            dados_especificacao: Dados extraídos da especificação
            nome_arquivo_apolice: Nome do arquivo da apólice
            
        Returns:
            JSON consolidado e formatado
        """
        import datetime
        
        logger.info("Consolidando dados...")
        
        # Extrai dados das diferentes seções
        j_mestre = dados_apolice.get('mestre', {})
        j_locais = dados_apolice.get('locais', {})
        j_cob = dados_apolice.get('coberturas', {})
        j_clausulas = dados_apolice.get('clausulas', {})
        
        # Busca coberturas específicas
        coberturas = j_cob.get("coberturas_completas", [])
        lmi_lc, _ = self._find_coverage(coberturas, ["lucros cessantes"])
        lmi_vend, fra_vend = self._find_coverage(coberturas, ["vendaval"])
        lmi_alag, fra_alag = self._find_coverage(coberturas, ["alagamento"])
        lmi_terr, fra_terr = self._find_coverage(coberturas, ["terremoto"])
        
        # Formata locais de risco
        locais_fmt = self._formatar_locais(j_locais.get("locais_risco", []))
        
        # Formata dados financeiros
        fin_data = self._formatar_especificacao(
            dados_especificacao.get("especificacao_cosseguro_cedido", {})
        )
        
        # Monta JSON final
        final_json = {
            "dados_gerais_apolice": {
                "metadata": {
                    "arquivo": nome_arquivo_apolice,
                    "timestamp": str(datetime.datetime.now())
                },
                "segurado": j_mestre.get("segurado"),
                "cnpj": j_mestre.get("cnpj"),
                "inicio_vigencia": j_mestre.get("inicio_vigencia"),
                "fim_vigencia": j_mestre.get("fim_vigencia"),
                "numero_apolice_lider": j_mestre.get("numero_apolice_lider"),
                "moeda": j_mestre.get("moeda"),
                "valor_limite_maximo_garantia": formatar_moeda(
                    j_mestre.get("valor_limite_maximo_garantia")
                ),
                "premio_emitido_ou_liquido": formatar_moeda(
                    j_mestre.get("premio_emitido_ou_liquido")
                ),
                "participacao_mitsui_sumitomo": j_mestre.get("participacao_mitsui_sumitomo"),
                "lmi_unico": j_mestre.get("lmi_unico"),
                "tem_cobertura_cbi": j_mestre.get("tem_cobertura_cbi"),
                "pais": "Brasil",
                "valor_cobertura_lucros_cessantes": lmi_lc,
                "limite_cobertura_vendaval": lmi_vend,
                "franquia_vendaval": fra_vend,
                "limite_cobertura_alagamento": lmi_alag,
                "franquia_alagamento": fra_alag,
                "limite_cobertura_terremoto": lmi_terr,
                "franquia_terremoto": fra_terr,
                "cosseguro_completo": j_mestre.get("cosseguro_completo", [])
            },
            "locais_risco": locais_fmt,
            "coberturas_completas": coberturas,
            "especificacao_cosseguro_cedido": fin_data
        }
        
        return final_json
    
    def _find_coverage(
        self,
        coverage_list: List[Dict],
        keywords: List[str]
    ) -> Tuple[str, str]:
        """
        Busca uma cobertura específica na lista baseado em palavras-chave
        
        Args:
            coverage_list: Lista de coberturas
            keywords: Palavras-chave para busca
            
        Returns:
            Tupla (LMI formatado, Franquia)
        """
        lmi, franquia = "Não consta", "Não consta"
        
        for c in coverage_list:
            nome_raw = c.get("nome_raw", "").lower()
            if all(k.lower() in nome_raw for k in keywords):
                lmi = formatar_moeda(c.get("lmi"))
                franquia = c.get("franquia_raw", "Não consta")
                break
        
        return lmi, franquia
    
    def _formatar_locais(self, locais: List[Dict]) -> List[Dict]:
        """Formata valores monetários dos locais de risco"""
        locais_fmt = []
        
        for loc in locais:
            loc["valor_risco_predio"] = formatar_moeda(loc.get("valor_risco_predio"))
            loc["valor_risco_mmu"] = formatar_moeda(loc.get("valor_risco_mmu"))
            loc["valor_risco_mmp"] = formatar_moeda(loc.get("valor_risco_mmp"))
            locais_fmt.append(loc)
        
        return locais_fmt
    
    def _formatar_especificacao(self, fin_data: Dict) -> Dict:
        """Formata valores monetários da especificação"""
        if "dados_gerais" in fin_data:
            fin_data["dados_gerais"]["importancia_segurada"] = formatar_moeda(
                fin_data["dados_gerais"].get("importancia_segurada")
            )
        
        # Formata ramos
        ramos_fmt = []
        for r in fin_data.get("outros_ramos", []):
            r["is"] = formatar_moeda(r.get("is"))
            ramos_fmt.append(r)
        fin_data["outros_ramos"] = ramos_fmt
        
        # Formata parcelas
        parc_fmt = []
        for p in fin_data.get("parcelas", []):
            for k in ["premio_tarifario", "desconto", "ad_fracionamento", 
                      "comissao_cosseguro", "total_liquido"]:
                p[k] = formatar_moeda(p.get(k))
            parc_fmt.append(p)
        fin_data["parcelas"] = parc_fmt
        
        # Formata totais
        if "totais_parcelas" in fin_data:
            t = fin_data["totais_parcelas"]
            for k in t:
                t[k] = formatar_moeda(t.get(k))
        
        return fin_data
