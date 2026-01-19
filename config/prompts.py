"""
Prompts para a API Gemini
"""

PROMPT_MESTRE_APOLICE = """
Analise este documento visualmente. Extraia os dados da apólice.
Retorne JSON. Se não achar, use "Não consta".

{
  "document_type": "Tipo do documento",
  "seguradora_canon": "Nome da Seguradora (AIG, MAPFRE, ETC)",
  "segurado": "Nome Segurado",
  "cnpj": "CNPJ",
  "numero_apolice_lider": "Número Apólice",
  "inicio_vigencia": "Data Inicio",
  "fim_vigencia": "Data Fim",
  "moeda": "Moeda",
  "valor_limite_maximo_garantia": "Valor LMG (Bruto)",
  "premio_emitido_ou_liquido": "Valor Prêmio (Bruto)",
  "participacao_mitsui_sumitomo": "% Mitsui",
  "lmi_unico": "Sim/Não",
  "tem_cobertura_cbi": "Sim/Não",
  "cosseguro_completo": [ { "nome_raw": "Nome", "percentual": "%", "lider": true/false } ]
}
"""

PROMPT_LOCAIS_V4_1 = """
Analise visualmente a tabela "Identificação do Bem Segurado" ou a lista de locais.
Extraia os valores EXATAMENTE como estão na imagem.

Retorne JSON:
{
  "locais_risco": [
    {
      "nro_local_risco": "Nº",
      "endereco": "Endereço Completo",
      "cidade": "Cidade",
      "estado": "UF",
      "cep": "CEP",
      "atividade_principal_risco": "Atividade",
      "valor_risco_predio": "Valor Edifícios (Coluna Específica)",
      "valor_risco_mmu": "Valor Máquinas/Móveis (Coluna Específica)",
      "valor_risco_mmp": "Valor Mercadorias (Coluna Específica)"
    }
  ]
}
"""

PROMPT_COBERTURAS_V3_GENERICO = """
Analise visualmente a tabela de Coberturas. Extraia TODAS as linhas (LMI, Franquia, Prêmio).
Retorne JSON:
{
  "coberturas_completas": [
    { "nome_raw": "Nome", "lmi": "Valor LMI", "franquia_raw": "Texto Franquia", "premio": "Valor Premio" }
  ]
}
"""

PROMPT_LMI_UNICO_CBI = """
Analise o documento e retorne JSON:
{ "lmi_unico": "Sim/Não", "tem_cobertura_cbi": "Sim/Não" }
"""

PROMPT_ESPECIFICACAO_FINANCEIRA_VISUAL = """
Você é um especialista contábil. Analise VISUALMENTE este documento de "Especificação de Cosseguro".
Ignore a formatação de texto quebrado e olhe para as TABELAS.

1. **LÍDER vs PARTICIPANTES:**
   - Identifique visualmente a tabela no topo (Líder) e a tabela abaixo (Cosseguradoras).
   - Extraia o "Nº Ordem" da Mitsui exatamente como está na imagem.
   - O array `seguradoras_participantes` DEVE ter a Líder E a Mitsui.

2. **RAMOS (Tabela Complexa):**
   - Localize a área "Outros Ramos".
   - Mesmo que os campos pareçam vazios, extraia a estrutura.
   - Se houver valores (Código, I.S., Comissão) preenchidos ao lado de Ramo 2, Ramo 3, etc., capture-os.

3. **PARCELAS:**
   - Localize a tabela de vencimentos.
   - Se os números estiverem grudados visualmente, separe-os logicamente (1, 2, 3...).

Retorne JSON:
{
  "especificacao_cosseguro_cedido": {
    "dados_gerais": {
        "codigo_lider": "Cód", "seguradora_lider": "Nome", "tomador": "Nome", "cnpj_tomador": "CNPJ",
        "corretor": "Nome", "codigo_susep_corretor": "Cód SUSEP", "ramo_seguro": "Ramo",
        "tipo_documento": "Tipo", "apolice": "Num Apólice", "doc_complementar": "Num",
        "endosso_cancelamento": "Texto", "num_ordem_doc_cancelado": "Texto", "codigo_operacao": "Cód",
        "percentual_sobre_premio_tarifario": "%", "percentual_comissao": "%",
        "data_emissao": "Data", "vigencia_inicio": "Data", "vigencia_fim": "Data",
        "sorteio": "Texto", "qtd_prestacao": "Qtd", "importancia_segurada": "Valor",
        "moeda": "Texto", "taxa_moeda": "Valor", "data_base": "Data", "percentual_desconto": "%"
    },
    "seguradoras_participantes": [
       { "codigo": "Cód", "nome": "Nome", "numero_ordem": "Num Ordem", "percentual_participacao": "%" }
    ],
    "outros_ramos": [
       { "ramo": "Nome", "codigo": "Cód", "is": "Valor", "percentual_sobre_premio": "%", "percentual_comissao": "%" }
    ],
    "parcelas": [
       { "num_parc": "1", "premio_tarifario": "Valor", "desconto": "Valor", "ad_fracionamento": "Valor", "comissao_cosseguro": "Valor", "total_liquido": "Valor" }
    ],
    "totais_parcelas": {
       "total_premio_tarifario": "Valor", "total_desconto": "Valor", "total_ad_fracionamento": "Valor", "total_comissao_cosseguro": "Valor", "total_liquido": "Valor"
    }
  }
}
"""