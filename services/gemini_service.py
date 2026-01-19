"""
Serviço de integração com a API Gemini
"""
import json
import re
import logging
from typing import Dict, Any
import google.generativeai as genai
from config.settings import gemini_config
from utils.validators import validar_arquivo_pdf, ValidationError

logger = logging.getLogger(__name__)


class GeminiService:
    """Serviço para interação com a API Gemini"""
    
    def __init__(self):
        """Inicializa o serviço Gemini"""
        try:
            genai.configure(api_key=gemini_config.API_KEY)
            self.model = genai.GenerativeModel(
                gemini_config.MODEL,
                generation_config=genai.types.GenerationConfig(
                    temperature=gemini_config.TEMPERATURE,
                    response_mime_type=gemini_config.RESPONSE_MIME_TYPE
                )
            )
        except Exception as e:
            logger.error(f"Erro ao configurar API Gemini: {e}")
            raise
    
    def processar_documento(
        self,
        file_stream,
        prompt: str,
        mime_type: str = "application/pdf"
    ) -> Dict[str, Any]:
        """
        Processa um documento usando a API Gemini
        
        Args:
            file_stream: Stream do arquivo (BytesIO)
            prompt: Prompt para o modelo
            mime_type: Tipo MIME do arquivo
            
        Returns:
            Dicionário com os dados extraídos
            
        Raises:
            ValidationError: Se o arquivo for inválido
            Exception: Para outros erros da API
        """
        try:
            # Rebobina e lê o arquivo
            file_stream.seek(0)
            file_bytes = file_stream.read()
            
            # Valida o arquivo
            validar_arquivo_pdf(file_bytes)
            
            # Cria o objeto "Part" para envio nativo
            document_part = {
                "mime_type": mime_type,
                "data": file_bytes
            }
            
            logger.info(f"Enviando documento ({len(file_bytes)} bytes) para processamento...")
            
            # Envia para a API
            response = self.model.generate_content(
                [prompt, document_part],
                request_options={'timeout': gemini_config.TIMEOUT}
            )
            
            # Limpa e parseia a resposta
            clean_response = self._limpar_resposta(response.text)
            json_data = json.loads(clean_response)
            
            logger.info("Documento processado com sucesso")
            return json_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON da resposta: {e}")
            logger.error(f"Resposta recebida: {response.text[:500]}")
            return {"erro_agente": f"Resposta inválida: {str(e)}"}
        
        except ValidationError as e:
            logger.error(f"Erro de validação: {e}")
            return {"erro_agente": str(e)}
        
        except Exception as e:
            logger.error(f"Erro ao processar documento: {e}")
            return {"erro_agente": str(e)}
    
    def _limpar_resposta(self, texto: str) -> str:
        """
        Remove marcações de código da resposta
        
        Args:
            texto: Texto bruto da resposta
            
        Returns:
            Texto limpo
        """
        # Remove blocos de código markdown
        clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip())
        return clean.strip()