"""
Testes unitários para funções de validação
"""
import pytest
from utils.validators import (
    validar_resposta_json,
    validar_cnpj,
    validar_data_formato,
    validar_arquivo_pdf,
    ValidationError
)


class TestValidarRespostaJson:
    """Testes para validação de resposta JSON"""
    
    def test_json_valido(self):
        """Testa validação de JSON válido"""
        dados = {"campo1": "valor1", "campo2": "valor2"}
        campos = ["campo1", "campo2"]
        assert validar_resposta_json(dados, campos) is True
    
    def test_campo_obrigatorio_ausente(self):
        """Testa detecção de campo obrigatório ausente"""
        dados = {"campo1": "valor1"}
        campos = ["campo1", "campo2"]
        
        with pytest.raises(ValidationError) as exc_info:
            validar_resposta_json(dados, campos)
        
        assert "campo2" in str(exc_info.value)
    
    def test_campo_com_valor_none(self):
        """Testa detecção de campo com valor None"""
        dados = {"campo1": "valor1", "campo2": None}
        campos = ["campo1", "campo2"]
        
        with pytest.raises(ValidationError):
            validar_resposta_json(dados, campos)
    
    def test_resposta_nao_e_dict(self):
        """Testa quando resposta não é um dicionário"""
        with pytest.raises(ValidationError) as exc_info:
            validar_resposta_json(["lista"], ["campo"])
        
        assert "dicionário" in str(exc_info.value)
    
    def test_sem_campos_obrigatorios(self):
        """Testa quando não há campos obrigatórios"""
        dados = {"campo1": "valor1"}
        assert validar_resposta_json(dados, []) is True


class TestValidarCnpj:
    """Testes para validação de CNPJ"""
    
    def test_cnpj_valido_formatado(self):
        """Testa CNPJ formatado válido"""
        assert validar_cnpj("12.345.678/0001-90") is True
    
    def test_cnpj_valido_sem_formatacao(self):
        """Testa CNPJ sem formatação válido"""
        assert validar_cnpj("12345678000190") is True
    
    def test_cnpj_invalido_poucos_digitos(self):
        """Testa CNPJ com menos de 14 dígitos"""
        assert validar_cnpj("123456780001") is False
    
    def test_cnpj_invalido_muitos_digitos(self):
        """Testa CNPJ com mais de 14 dígitos"""
        assert validar_cnpj("123456780001901") is False
    
    def test_cnpj_vazio(self):
        """Testa CNPJ vazio"""
        assert validar_cnpj("") is False
        assert validar_cnpj(None) is False
    
    def test_cnpj_com_letras(self):
        """Testa CNPJ com letras (deve ignorar)"""
        assert validar_cnpj("12.345.678/0001-9A") is False


class TestValidarDataFormato:
    """Testes para validação de formato de data"""
    
    def test_data_formato_brasileiro(self):
        """Testa formato brasileiro DD/MM/YYYY"""
        assert validar_data_formato("31/12/2023") is True
        assert validar_data_formato("01/01/2024") is True
    
    def test_data_formato_traco(self):
        """Testa formato com traço DD-MM-YYYY"""
        assert validar_data_formato("31-12-2023") is True
    
    def test_data_formato_iso(self):
        """Testa formato ISO YYYY-MM-DD"""
        assert validar_data_formato("2023-12-31") is True
    
    def test_data_invalida(self):
        """Testa formatos de data inválidos"""
        # Nota: A validação atual é apenas de formato, não de valores válidos
        # Para validar se o mês é 1-12, seria necessário parsing completo
        assert validar_data_formato("2023/12/31") is False  # Formato YYYY/MM/DD não é aceito
        assert validar_data_formato("31.12.2023") is False  # Formato com ponto não é aceito
    
    def test_data_vazia(self):
        """Testa data vazia ou 'Não consta'"""
        assert validar_data_formato("") is False
        assert validar_data_formato(None) is False
        assert validar_data_formato("Não consta") is False
    
    def test_data_texto(self):
        """Testa texto que não é data"""
        assert validar_data_formato("texto qualquer") is False


class TestValidarArquivoPdf:
    """Testes para validação de arquivo PDF"""
    
    def test_pdf_valido(self):
        """Testa PDF válido"""
        pdf_bytes = b'%PDF-1.4\n%EOF'
        assert validar_arquivo_pdf(pdf_bytes) is True
    
    def test_pdf_vazio(self):
        """Testa arquivo vazio"""
        with pytest.raises(ValidationError) as exc_info:
            validar_arquivo_pdf(b'')
        
        assert "vazio" in str(exc_info.value)
    
    def test_arquivo_nao_pdf(self):
        """Testa arquivo que não é PDF"""
        with pytest.raises(ValidationError) as exc_info:
            validar_arquivo_pdf(b'texto comum')
        
        assert "não é um PDF válido" in str(exc_info.value)
    
    def test_pdf_excede_tamanho(self):
        """Testa PDF que excede tamanho máximo"""
        # Cria um arquivo de 51MB
        pdf_bytes = b'%PDF-1.4\n' + b'x' * (51 * 1024 * 1024)
        
        with pytest.raises(ValidationError) as exc_info:
            validar_arquivo_pdf(pdf_bytes, max_size_mb=50)
        
        assert "excede tamanho máximo" in str(exc_info.value)
    
    def test_pdf_tamanho_limite(self):
        """Testa PDF no limite do tamanho"""
        # Cria um arquivo de exatamente 1MB
        pdf_bytes = b'%PDF-1.4\n' + b'x' * (1 * 1024 * 1024 - 10)
        assert validar_arquivo_pdf(pdf_bytes, max_size_mb=1) is True