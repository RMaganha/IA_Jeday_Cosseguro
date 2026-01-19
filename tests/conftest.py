"""
Configurações e fixtures compartilhadas para todos os testes
"""
import pytest
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def setup_test_env():
    """Configura ambiente de teste"""
    # Define variáveis de ambiente para teste
    os.environ.setdefault('GEMINI_API_KEY', 'test_key_for_mocking')
    os.environ.setdefault('SQL_CONNECTION_STRING', 'test_connection')
    yield
    # Cleanup se necessário


@pytest.fixture
def mock_pdf_bytes():
    """Retorna bytes de um PDF mínimo válido"""
    return b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%EOF'


@pytest.fixture
def sample_apolice_data():
    """Dados de exemplo de uma apólice"""
    return {
        "segurado": "EMPRESA TESTE LTDA",
        "cnpj": "12.345.678/0001-90",
        "numero_apolice_lider": "123456-2024",
        "inicio_vigencia": "01/01/2024",
        "fim_vigencia": "31/12/2024",
        "moeda": "BRL",
        "valor_limite_maximo_garantia": "1000000.00",
        "premio_emitido_ou_liquido": "50000.00",
        "participacao_mitsui_sumitomo": "30",
        "lmi_unico": "Sim",
        "tem_cobertura_cbi": "Não",
        "cosseguro_completo": [
            {
                "nome_raw": "Seguradora Líder",
                "percentual": "70",
                "lider": True
            },
            {
                "nome_raw": "Mitsui Sumitomo",
                "percentual": "30",
                "lider": False
            }
        ]
    }


@pytest.fixture
def sample_locais_data():
    """Dados de exemplo de locais de risco"""
    return {
        "locais_risco": [
            {
                "nro_local_risco": "1",
                "endereco": "Rua das Flores, 123",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01234-567",
                "atividade_principal_risco": "Indústria de eletrônicos",
                "valor_risco_predio": "5000000.00",
                "valor_risco_mmu": "2000000.00",
                "valor_risco_mmp": "1000000.00"
            },
            {
                "nro_local_risco": "2",
                "endereco": "Av. Principal, 456",
                "cidade": "Rio de Janeiro",
                "estado": "RJ",
                "cep": "20000-000",
                "atividade_principal_risco": "Depósito",
                "valor_risco_predio": "3000000.00",
                "valor_risco_mmu": "500000.00",
                "valor_risco_mmp": "2000000.00"
            }
        ]
    }


@pytest.fixture
def sample_coberturas_data():
    """Dados de exemplo de coberturas"""
    return {
        "coberturas_completas": [
            {
                "nome_raw": "Incêndio, Raio e Explosão",
                "lmi": "8000000.00",
                "franquia_raw": "10% dos prejuízos, mínimo R$ 50.000,00",
                "premio": "40000.00"
            },
            {
                "nome_raw": "Vendaval",
                "lmi": "5000000.00",
                "franquia_raw": "15% dos prejuízos, mínimo R$ 100.000,00",
                "premio": "15000.00"
            },
            {
                "nome_raw": "Lucros Cessantes",
                "lmi": "2000000.00",
                "franquia_raw": "30 dias",
                "premio": "10000.00"
            }
        ]
    }


@pytest.fixture
def sample_especificacao_data():
    """Dados de exemplo de especificação"""
    return {
        "especificacao_cosseguro_cedido": {
            "dados_gerais": {
                "codigo_lider": "001",
                "seguradora_lider": "Seguradora Teste",
                "tomador": "EMPRESA TESTE LTDA",
                "cnpj_tomador": "12.345.678/0001-90",
                "corretor": "Corretora XYZ",
                "codigo_susep_corretor": "123456",
                "ramo_seguro": "Incêndio",
                "tipo_documento": "Apólice",
                "apolice": "123456-2024",
                "percentual_sobre_premio_tarifario": "100",
                "percentual_comissao": "10",
                "data_emissao": "01/01/2024",
                "vigencia_inicio": "01/01/2024",
                "vigencia_fim": "31/12/2024",
                "importancia_segurada": "8000000.00",
                "moeda": "BRL"
            },
            "seguradoras_participantes": [
                {
                    "codigo": "001",
                    "nome": "Seguradora Líder",
                    "numero_ordem": "1",
                    "percentual_participacao": "70"
                },
                {
                    "codigo": "002",
                    "nome": "Mitsui Sumitomo",
                    "numero_ordem": "2",
                    "percentual_participacao": "30"
                }
            ],
            "parcelas": [
                {
                    "num_parc": "1",
                    "premio_tarifario": "25000.00",
                    "desconto": "0",
                    "ad_fracionamento": "0",
                    "comissao_cosseguro": "2500.00",
                    "total_liquido": "22500.00"
                },
                {
                    "num_parc": "2",
                    "premio_tarifario": "25000.00",
                    "desconto": "0",
                    "ad_fracionamento": "0",
                    "comissao_cosseguro": "2500.00",
                    "total_liquido": "22500.00"
                }
            ],
            "totais_parcelas": {
                "total_premio_tarifario": "50000.00",
                "total_desconto": "0",
                "total_ad_fracionamento": "0",
                "total_comissao_cosseguro": "5000.00",
                "total_liquido": "45000.00"
            }
        }
    }


@pytest.fixture
def complete_json_output(
    sample_apolice_data,
    sample_locais_data,
    sample_coberturas_data,
    sample_especificacao_data
):
    """JSON completo consolidado para testes"""
    return {
        "dados_gerais_apolice": {
            "metadata": {
                "arquivo": "teste_apolice.pdf",
                "timestamp": "2024-01-01T10:00:00"
            },
            **sample_apolice_data,
            "pais": "Brasil",
            "valor_cobertura_lucros_cessantes": "R$ 2.000.000,00",
            "limite_cobertura_vendaval": "R$ 5.000.000,00",
            "franquia_vendaval": "15% dos prejuízos, mínimo R$ 100.000,00"
        },
        **sample_locais_data,
        **sample_coberturas_data,
        **sample_especificacao_data
    }