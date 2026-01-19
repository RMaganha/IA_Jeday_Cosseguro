"""
Componentes de interface do Streamlit
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any


def exibir_telas_json(final_json: Dict[str, Any]):
    """
    Exibe o JSON processado em múltiplas abas organizadas
    
    Args:
        final_json: Dicionário com todos os dados processados
    """
    dados_apolice = final_json.get("dados_gerais_apolice", {})
    locais_risco = final_json.get("locais_risco", [])
    coberturas = final_json.get("coberturas_completas", [])
    especificacao = final_json.get("especificacao_cosseguro_cedido", {})

    tab_apolice, tab_locais, tab_coberturas, tab_espec = st.tabs(
        ["Apólice", "Local de Risco", "Coberturas", "Especificação"]
    )

    # ---- ABA APÓLICE ----
    with tab_apolice:
        _exibir_aba_apolice(dados_apolice)

    # ---- ABA LOCAIS DE RISCO ----
    with tab_locais:
        _exibir_aba_locais(locais_risco)

    # ---- ABA COBERTURAS ----
    with tab_coberturas:
        _exibir_aba_coberturas(coberturas)

    # ---- ABA ESPECIFICAÇÃO ----
    with tab_espec:
        _exibir_aba_especificacao(especificacao)


def _exibir_aba_apolice(dados_apolice: Dict[str, Any]):
    """Exibe a aba de dados da apólice"""
    st.subheader("Dados Gerais da Apólice")
    c1, c2 = st.columns(2)

    with c1:
        st.text_input("Segurado", value=dados_apolice.get("segurado", ""), 
                     key="apolice_segurado")
        st.text_input("CNPJ", value=dados_apolice.get("cnpj", ""), 
                     key="apolice_cnpj")
        st.text_input("Início Vigência", value=dados_apolice.get("inicio_vigencia", ""), 
                     key="apolice_inicio")
        st.text_input("LMG", value=dados_apolice.get("valor_limite_maximo_garantia", ""), 
                     key="apolice_lmg")
        st.text_input("Cobertura LC", value=dados_apolice.get("valor_cobertura_lucros_cessantes", ""), 
                     key="apolice_lc")

    with c2:
        st.text_input("Número Apólice Líder", value=dados_apolice.get("numero_apolice_lider", ""), 
                     key="apolice_numero")
        st.text_input("Fim Vigência", value=dados_apolice.get("fim_vigencia", ""), 
                     key="apolice_fim")
        st.text_input("Moeda", value=dados_apolice.get("moeda", ""), 
                     key="apolice_moeda")
        st.text_input("Prêmio Emitido/Líquido", value=dados_apolice.get("premio_emitido_ou_liquido", ""), 
                     key="apolice_premio")
        st.text_input("Participação Mitsui", value=str(dados_apolice.get("participacao_mitsui_sumitomo", "")), 
                     key="apolice_part_mitsui")

    c3, c4 = st.columns(2)
    with c3:
        st.text_input("LMI Único", value=dados_apolice.get("lmi_unico", ""), 
                     key="apolice_lmi_unico")
        st.text_input("Tem Cobertura CBI", value=dados_apolice.get("tem_cobertura_cbi", ""), 
                     key="apolice_cbi")
        st.text_input("País", value=dados_apolice.get("pais", ""), 
                     key="apolice_pais")
    
    with c4:
        st.text_input("Limite Vendaval", value=dados_apolice.get("limite_cobertura_vendaval", ""), 
                     key="apolice_lim_vendaval")
        st.text_input("Franquia Vendaval", value=dados_apolice.get("franquia_vendaval", ""), 
                     key="apolice_fra_vendaval")
        st.text_input("Limite Alagamento", value=dados_apolice.get("limite_cobertura_alagamento", ""), 
                     key="apolice_lim_alagamento")
        st.text_input("Franquia Alagamento", value=dados_apolice.get("franquia_alagamento", ""), 
                     key="apolice_fra_alagamento")
        st.text_input("Limite Terremoto", value=dados_apolice.get("limite_cobertura_terremoto", ""), 
                     key="apolice_lim_terremoto")
        st.text_input("Franquia Terremoto", value=dados_apolice.get("franquia_terremoto", ""), 
                     key="apolice_fra_terremoto")

    st.markdown("**Cosseguro Completo**")
    if dados_apolice.get("cosseguro_completo"):
        st.table(dados_apolice.get("cosseguro_completo", []))
    else:
        st.info("Nenhum cosseguro registrado")


def _exibir_aba_locais(locais_risco: list):
    """Exibe a aba de locais de risco"""
    st.subheader("Locais de Risco")
    
    if not locais_risco:
        st.info("Nenhum local de risco encontrado no JSON.")
        return
    
    for idx, loc in enumerate(locais_risco):
        with st.expander(f"Local {loc.get('nro_local_risco', idx + 1)}", 
                        expanded=(idx == 0)):
            c1, c2 = st.columns(2)
            
            with c1:
                st.text_input("Nº Local", value=loc.get("nro_local_risco", ""), 
                            key=f"loc_{idx}_nro")
                st.text_input("Endereço", value=loc.get("endereco", ""), 
                            key=f"loc_{idx}_end")
                st.text_input("Cidade", value=loc.get("cidade", ""), 
                            key=f"loc_{idx}_cid")
                st.text_input("CEP", value=loc.get("cep", ""), 
                            key=f"loc_{idx}_cep")
            
            with c2:
                st.text_input("Estado", value=loc.get("estado", ""), 
                            key=f"loc_{idx}_uf")
                st.text_area("Atividade Principal", value=loc.get("atividade_principal_risco", ""), 
                           key=f"loc_{idx}_ativ")
                st.text_input("Valor Risco Prédio", value=loc.get("valor_risco_predio", ""), 
                            key=f"loc_{idx}_predio")
                st.text_input("Valor Risco MMU", value=loc.get("valor_risco_mmu", ""), 
                            key=f"loc_{idx}_mmu")
                st.text_input("Valor Risco MMP", value=loc.get("valor_risco_mmp", ""), 
                            key=f"loc_{idx}_mmp")


def _exibir_aba_coberturas(coberturas: list):
    """Exibe a aba de coberturas"""
    st.subheader("Coberturas")
    
    if not coberturas:
        st.info("Nenhuma cobertura encontrada no JSON.")
        return
    
    df_cob = pd.DataFrame(coberturas).copy()
    
    # CSS para melhor visualização
    css = """
        <style>
        .tabela-coberturas {
            width: 100%;
            table-layout: fixed;
            font-size: 12px;
        }
        .tabela-coberturas th, .tabela-coberturas td {
            font-size: 14px;
            padding: 8px;
            border: 1px solid #ddd;
        }
        .tabela-coberturas th {
            background-color: #f0f2f6;
            font-weight: bold;
        }
        .tabela-coberturas th:nth-child(1),
        .tabela-coberturas td:nth-child(1),
        .tabela-coberturas th:nth-child(3),
        .tabela-coberturas td:nth-child(3) {
            max-width: 260px;
            white-space: normal;
            word-wrap: break-word;
        }
        </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(
        df_cob.to_html(index=False, classes="tabela-coberturas"),
        unsafe_allow_html=True,
    )


def _exibir_aba_especificacao(especificacao: Dict[str, Any]):
    """Exibe a aba de especificação"""
    st.subheader("Dados Gerais da Especificação")
    
    dados_gerais = especificacao.get("dados_gerais", {})
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.text_input("Código Líder", value=dados_gerais.get("codigo_lider", ""), 
                     key="esp_cod_lider")
        st.text_input("Seguradora Líder", value=dados_gerais.get("seguradora_lider", ""), 
                     key="esp_seg_lider")
        st.text_input("Tomador", value=dados_gerais.get("tomador", ""), 
                     key="esp_tomador")
        st.text_input("CNPJ Tomador", value=dados_gerais.get("cnpj_tomador", ""), 
                     key="esp_cnpj_tomador")
        st.text_input("Corretor", value=dados_gerais.get("corretor", ""), 
                     key="esp_corretor")
        st.text_input("Código SUSEP Corretor", value=dados_gerais.get("codigo_susep_corretor", ""), 
                     key="esp_susep_corretor")
        st.text_input("Ramo Seguro", value=dados_gerais.get("ramo_seguro", ""), 
                     key="esp_ramo")
    
    with c2:
        st.text_input("Tipo Documento", value=dados_gerais.get("tipo_documento", ""), 
                     key="esp_tipo_doc")
        st.text_input("Apólice", value=dados_gerais.get("apolice", ""), 
                     key="esp_apolice")
        st.text_input("Percentual sobre Prêmio Tarifário", 
                     value=dados_gerais.get("percentual_sobre_premio_tarifario", ""), 
                     key="esp_pct_premio")
        st.text_input("Percentual Comissão", value=dados_gerais.get("percentual_comissao", ""), 
                     key="esp_pct_comissao")
        st.text_input("Data Emissão", value=dados_gerais.get("data_emissao", ""), 
                     key="esp_data_emissao")
        st.text_input("Vigência Início", value=dados_gerais.get("vigencia_inicio", ""), 
                     key="esp_vig_ini")
        st.text_input("Vigência Fim", value=dados_gerais.get("vigencia_fim", ""), 
                     key="esp_vig_fim")
        st.text_input("Importância Segurada", value=dados_gerais.get("importancia_segurada", ""), 
                     key="esp_is")

    st.markdown("**Seguradoras Participantes**")
    participantes = especificacao.get("seguradoras_participantes", [])
    if participantes:
        st.table(participantes)
    else:
        st.info("Nenhuma seguradora participante")

    st.markdown("**Outros Ramos**")
    ramos = especificacao.get("outros_ramos", [])
    if ramos:
        st.table(ramos)
    else:
        st.info("Nenhum outro ramo registrado")

    st.markdown("**Parcelas**")
    parcelas = especificacao.get("parcelas", [])
    if parcelas:
        st.table(parcelas)
    else:
        st.info("Nenhuma parcela registrada")

    st.markdown("**Totais das Parcelas**")
    totais = especificacao.get("totais_parcelas", {})
    if totais:
        st.table([totais])
    else:
        st.info("Nenhum total calculado")