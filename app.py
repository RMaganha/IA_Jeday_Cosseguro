"""
Aplicação principal - Extrator de Apólices V20 (Visão Nativa)
"""
import streamlit as st
import json
import os
import traceback
import logging

from config.settings import app_config, validate_config
from services.database_service import DatabaseService
from services.pdf_processor import PDFProcessor
from ui.components import exibir_telas_json
from utils.logger import setup_logger
from utils.formatters import sanitizar_nome_arquivo


def main():
    """Função principal da aplicação"""
    
    # Configuração da página
    st.set_page_config(
        page_title=app_config.PAGE_TITLE,
        layout=app_config.PAGE_LAYOUT
    )
    
    st.title(f"📄 {app_config.PAGE_TITLE}")
    
    # Valida configurações
    try:
        validate_config()
    except ValueError as e:
        st.error(f"❌ Erro de configuração: {e}")
        st.info("Configure as variáveis de ambiente GEMINI_API_KEY e SQL_CONNECTION_STRING no arquivo .env")
        st.stop()
    
    # Interface
    num_solic_input = st.text_input(
        "Número da solicitação:",
        value=str(app_config.NUM_SOLIC_TESTE)
    )
    
    # Área de logs
    with st.expander("Logs de Processamento", expanded=True):
        log_placeholder = st.empty()
    
    # Configura logger
    logger = setup_logger("extrator", log_placeholder)
    
    # Informações
    st.info(
        f"💡 Modo automático: Os anexos serão carregados da base de dados "
        f"para a solicitação {num_solic_input}"
    )
    
    # Botão de processamento
    if st.button("🚀 Processar Apólice", type="primary"):
        processar_apolice(num_solic_input, logger)


def processar_apolice(num_solic: str, logger: logging.Logger):
    """
    Processa uma apólice completa
    
    Args:
        num_solic: Número da solicitação
        logger: Logger configurado
    """
    status = st.status("Processando...", expanded=True)
    
    try:
        # Valida número da solicitação
        try:
            num_solic_int = int(num_solic)
        except ValueError:
            st.error("❌ Número de solicitação inválido")
            return
        
        # Inicializa serviços
        logger.info("Inicializando serviços...")
        db_service = DatabaseService()
        processor = PDFProcessor()
        
        # Carrega anexos do banco
        status.write("📥 Carregando anexos do banco de dados...")
        f_apolice, f_especificacao = db_service.carregar_anexos(num_solic_int)
        
        if not f_apolice or not f_especificacao:
            status.update(
                label="❌ Erro: Anexos não encontrados",
                state="error"
            )
            st.error(
                "Não foi possível localizar os anexos (Apólice e Especificação) "
                "no banco de dados para a solicitação informada."
            )
            return
        
        logger.info(f"✅ Anexos carregados: {f_apolice.name}, {f_especificacao.name}")
        
        # Processa apólice
        status.write("🔍 Extraindo dados da apólice...")
        dados_apolice = processor.processar_apolice(f_apolice)
        
        # Verifica erros no processamento da apólice
        if any('erro' in v or 'erro_agente' in v for v in dados_apolice.values()):
            logger.warning("⚠️ Alguns dados da apólice podem estar incompletos")
        
        # Processa especificação
        status.write("💰 Extraindo dados da especificação financeira...")
        dados_especificacao = processor.processar_especificacao(f_especificacao)
        
        # Consolida dados
        status.write("📊 Consolidando dados...")
        final_json = processor.consolidar_dados(
            dados_apolice,
            dados_especificacao,
            f_apolice.name
        )
        
        # Salva JSON
        status.write("💾 Salvando resultado...")
        caminho_arquivo = salvar_json(final_json, logger)
        
        # Sucesso
        status.update(label="✅ Processamento concluído!", state="complete")
        
        st.success(f"🎉 Arquivo salvo com sucesso: `{caminho_arquivo}`")
        
        # Exibe JSON bruto
        with st.expander("📋 Visualizar JSON Completo"):
            st.json(final_json)
        
        # Exibe interface organizada
        st.markdown("---")
        st.subheader("📑 Dados Extraídos")
        exibir_telas_json(final_json)
        
    except Exception as e:
        status.update(label="❌ Erro no processamento", state="error")
        logger.error(f"Erro: {str(e)}")
        st.error(f"❌ Erro no processamento: {str(e)}")
        
        with st.expander("🔍 Detalhes do Erro"):
            st.code(traceback.format_exc())


def salvar_json(final_json: dict, logger: logging.Logger) -> str:
    """
    Salva o JSON em arquivo
    
    Args:
        final_json: Dicionário com dados processados
        logger: Logger configurado
        
    Returns:
        Caminho do arquivo salvo
    """
    # Cria diretório se não existir
    os.makedirs(app_config.JSON_OUTPUT_DIR, exist_ok=True)
    
    # Extrai informações para nome do arquivo
    dados_apolice = final_json.get("dados_gerais_apolice", {})
    seguradora = dados_apolice.get("metadata", {}).get("arquivo", "DESCONHECIDA")
    
    # Tenta extrair nome da seguradora do arquivo
    if "dados_gerais_apolice" in final_json:
        seguradora_nome = "SEGURADORA"
        apolice_numero = dados_apolice.get("numero_apolice_lider", "000")
    else:
        seguradora_nome = "SEGURADORA"
        apolice_numero = "000"
    
    # Monta nome do arquivo
    nome_arquivo = sanitizar_nome_arquivo(f"{seguradora_nome}-{apolice_numero}.json")
    caminho_completo = os.path.join(app_config.JSON_OUTPUT_DIR, nome_arquivo)
    
    # Salva
    with open(caminho_completo, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ JSON salvo em: {caminho_completo}")
    
    return caminho_completo


if __name__ == "__main__":
    main()