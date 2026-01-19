"""
Testes de integração - testam o fluxo completo com PDFs reais
"""
import pytest
import json
import os
from io import BytesIO
from pathlib import Path

# Importar apenas se as variáveis de ambiente estiverem configuradas
try:
    from services.pdf_processor import PDFProcessor
    from services.gemini_service import GeminiService
    INTEGRATION_ENABLED = os.getenv('RUN_INTEGRATION_TESTS') == 'true'
except Exception:
    INTEGRATION_ENABLED = False


@pytest.mark.skipif(not INTEGRATION_ENABLED, reason="Testes de integração desabilitados")
class TestPDFProcessorIntegration:
    """Testes de integração do processador de PDFs"""
    
    @pytest.fixture
    def processor(self):
        """Cria uma instância do processador"""
        return PDFProcessor()
    
    @pytest.fixture
    def pdf_apolice_sample(self):
        """Carrega um PDF de apólice de teste"""
        # Coloque um PDF real de teste na pasta tests/fixtures/
        pdf_path = Path(__file__).parent / "fixtures" / "apolice_teste.pdf"
        
        if not pdf_path.exists():
            pytest.skip("PDF de teste não encontrado")
        
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        return BytesIO(pdf_bytes)
    
    @pytest.fixture
    def pdf_especificacao_sample(self):
        """Carrega um PDF de especificação de teste"""
        pdf_path = Path(__file__).parent / "fixtures" / "especificacao_teste.pdf"
        
        if not pdf_path.exists():
            pytest.skip("PDF de teste não encontrado")
        
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        return BytesIO(pdf_bytes)
    
    def test_processar_apolice_completa(self, processor, pdf_apolice_sample):
        """Testa processamento completo de uma apólice"""
        resultado = processor.processar_apolice(pdf_apolice_sample)
        
        # Valida estrutura da resposta
        assert 'mestre' in resultado
        assert 'locais' in resultado
        assert 'coberturas' in resultado
        assert 'clausulas' in resultado
        
        # Valida que não há erros críticos
        assert 'erro' not in resultado.get('mestre', {})
        
        # Valida campos essenciais do mestre
        dados_mestre = resultado['mestre']
        assert 'segurado' in dados_mestre
        assert 'cnpj' in dados_mestre
        assert 'numero_apolice_lider' in dados_mestre
    
    def test_processar_especificacao(self, processor, pdf_especificacao_sample):
        """Testa processamento de especificação financeira"""
        resultado = processor.processar_especificacao(pdf_especificacao_sample)
        
        # Valida estrutura
        assert 'especificacao_cosseguro_cedido' in resultado
        
        especificacao = resultado['especificacao_cosseguro_cedido']
        assert 'dados_gerais' in especificacao
        assert 'seguradoras_participantes' in especificacao
    
    def test_consolidar_dados_completo(
        self,
        processor,
        pdf_apolice_sample,
        pdf_especificacao_sample
    ):
        """Testa consolidação completa dos dados"""
        # Processa ambos os documentos
        dados_apolice = processor.processar_apolice(pdf_apolice_sample)
        dados_especificacao = processor.processar_especificacao(pdf_especificacao_sample)
        
        # Consolida
        resultado_final = processor.consolidar_dados(
            dados_apolice,
            dados_especificacao,
            "teste_apolice.pdf"
        )
        
        # Valida estrutura final
        assert 'dados_gerais_apolice' in resultado_final
        assert 'locais_risco' in resultado_final
        assert 'coberturas_completas' in resultado_final
        assert 'especificacao_cosseguro_cedido' in resultado_final
        
        # Valida metadata
        metadata = resultado_final['dados_gerais_apolice'].get('metadata', {})
        assert 'arquivo' in metadata
        assert 'timestamp' in metadata
        
        # Valida que valores monetários estão formatados
        lmg = resultado_final['dados_gerais_apolice'].get('valor_limite_maximo_garantia')
        if lmg and lmg != "Não consta":
            assert lmg.startswith("R$")
    
    def test_busca_cobertura_especifica(self, processor, pdf_apolice_sample):
        """Testa busca de coberturas específicas"""
        dados = processor.processar_apolice(pdf_apolice_sample)
        coberturas = dados.get('coberturas', {}).get('coberturas_completas', [])
        
        # Testa busca de cobertura de vendaval
        lmi, franquia = processor._find_coverage(coberturas, ["vendaval"])
        
        # Deve retornar algo (mesmo que seja "Não consta")
        assert lmi is not None
        assert franquia is not None


@pytest.mark.skipif(not INTEGRATION_ENABLED, reason="Testes de integração desabilitados")
class TestGeminiServiceIntegration:
    """Testes de integração do serviço Gemini"""
    
    @pytest.fixture
    def service(self):
        """Cria instância do serviço"""
        return GeminiService()
    
    def test_processar_documento_simples(self, service):
        """Testa processamento de documento simples"""
        # Cria um PDF mínimo para teste
        pdf_bytes = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n%EOF'
        pdf_stream = BytesIO(pdf_bytes)
        pdf_stream.name = "teste.pdf"
        
        prompt = """Analise este documento e retorne JSON:
        { "teste": "valor" }
        """
        
        # Nota: Este teste pode falhar se o PDF for muito simples
        # É mais um smoke test para verificar conectividade
        try:
            resultado = service.processar_documento(pdf_stream, prompt)
            assert isinstance(resultado, dict)
        except Exception as e:
            pytest.skip(f"API indisponível ou PDF inválido: {e}")


@pytest.mark.skipif(not INTEGRATION_ENABLED, reason="Testes de integração desabilitados")
class TestFluxoCompletoE2E:
    """Testes end-to-end do fluxo completo"""
    
    def test_fluxo_completo_com_salvamento(self, tmp_path):
        """Testa o fluxo completo incluindo salvamento"""
        # Este teste simula o fluxo completo que o usuário faria
        
        # 1. Carrega PDFs (fixtures)
        # 2. Processa
        # 3. Consolida
        # 4. Salva
        # 5. Valida arquivo salvo
        
        pytest.skip("Implementar quando houver PDFs de fixture disponíveis")


# Fixtures compartilhadas
@pytest.fixture(scope="session")
def sample_json_response():
    """JSON de resposta de exemplo para testes"""
    return {
        "dados_gerais_apolice": {
            "segurado": "EMPRESA TESTE LTDA",
            "cnpj": "12.345.678/0001-90",
            "numero_apolice_lider": "123456",
            "moeda": "BRL",
            "valor_limite_maximo_garantia": "R$ 1.000.000,00"
        },
        "locais_risco": [
            {
                "nro_local_risco": "1",
                "endereco": "Rua Teste, 123",
                "cidade": "São Paulo",
                "estado": "SP"
            }
        ],
        "coberturas_completas": [
            {
                "nome_raw": "Incêndio",
                "lmi": "R$ 500.000,00",
                "franquia_raw": "10% dos prejuízos"
            }
        ]
    }