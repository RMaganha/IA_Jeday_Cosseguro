"""
Testes unitários para funções de formatação
"""
import pytest
from utils.formatters import formatar_moeda, sanitizar_nome_arquivo, extrair_numero_limpo


class TestFormatarMoeda:
    """Testes para a função formatar_moeda"""
    
    def test_formatar_valor_inteiro(self):
        """Testa formatação de valor inteiro"""
        assert formatar_moeda(1000) == "R$ 1.000,00"
        assert formatar_moeda("1000") == "R$ 1.000,00"
    
    def test_formatar_valor_decimal(self):
        """Testa formatação de valor decimal"""
        assert formatar_moeda(1234.56) == "R$ 1.234,56"
        assert formatar_moeda("1234.56") == "R$ 1.234,56"
    
    def test_formatar_valor_com_virgula(self):
        """Testa formatação de valor com vírgula como separador decimal"""
        assert formatar_moeda("1234,56") == "R$ 1.234,56"
        assert formatar_moeda("1.234,56") == "R$ 1.234,56"
    
    def test_formatar_valor_com_moeda(self):
        """Testa formatação de valor que já contém R$"""
        assert formatar_moeda("R$ 1.234,56") == "R$ 1.234,56"
        assert formatar_moeda("R$1234.56") == "R$ 1.234,56"
    
    def test_valores_invalidos(self):
        """Testa valores inválidos que devem retornar 'Não consta'"""
        assert formatar_moeda(None) == "Não consta"
        assert formatar_moeda("") == "Não consta"
        assert formatar_moeda("Não consta") == "Não consta"
        assert formatar_moeda(0) == "Não consta"
        assert formatar_moeda("0") == "Não consta"
        assert formatar_moeda("null") == "Não consta"
    
    def test_valor_grande(self):
        """Testa formatação de valores grandes"""
        assert formatar_moeda(1000000) == "R$ 1.000.000,00"
        assert formatar_moeda("1000000.50") == "R$ 1.000.000,50"
    
    def test_valor_com_texto(self):
        """Testa extração de valor de string com texto"""
        assert formatar_moeda("Valor: R$ 1.234,56 reais") == "R$ 1.234,56"


class TestSanitizarNomeArquivo:
    """Testes para a função sanitizar_nome_arquivo"""
    
    def test_remover_caracteres_invalidos(self):
        """Testa remoção de caracteres inválidos"""
        assert sanitizar_nome_arquivo("arquivo*.txt") == "arquivo.txt"
        assert sanitizar_nome_arquivo("arquivo:teste?.pdf") == "arquivoteste.pdf"
        assert sanitizar_nome_arquivo('arquivo"<>|.json') == "arquivo.json"
    
    def test_nome_valido(self):
        """Testa que nomes válidos não são alterados"""
        assert sanitizar_nome_arquivo("arquivo_valido.txt") == "arquivo_valido.txt"
        assert sanitizar_nome_arquivo("Arquivo-123.pdf") == "Arquivo-123.pdf"
    
    def test_caminho_com_barra(self):
        """Testa remoção de barras (não permite caminhos)"""
        assert sanitizar_nome_arquivo("pasta/arquivo.txt") == "pastaarquivo.txt"
        assert sanitizar_nome_arquivo("pasta\\arquivo.txt") == "pastaarquivo.txt"


class TestExtrairNumeroLimpo:
    """Testes para a função extrair_numero_limpo"""
    
    def test_extrair_apenas_numeros(self):
        """Testa extração de números de strings"""
        assert extrair_numero_limpo("123") == "123"
        assert extrair_numero_limpo("abc123def") == "123"
        assert extrair_numero_limpo("12.34.56") == "123456"
    
    def test_cnpj_com_formatacao(self):
        """Testa extração de CNPJ formatado"""
        assert extrair_numero_limpo("12.345.678/0001-90") == "12345678000190"
    
    def test_telefone_com_formatacao(self):
        """Testa extração de telefone formatado"""
        assert extrair_numero_limpo("(11) 98765-4321") == "11987654321"
    
    def test_sem_numeros(self):
        """Testa string sem números"""
        assert extrair_numero_limpo("abcdef") == ""
    
    def test_valor_none(self):
        """Testa com valor None (convertido para string)"""
        assert extrair_numero_limpo(None) == ""