"""
Sistema de logging customizado para Streamlit
"""
import logging


class StreamlitHandler(logging.Handler):
    """Handler customizado para exibir logs no Streamlit"""
    
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.log_buffer = ""

    def emit(self, record):
        """Emite uma mensagem de log"""
        msg = self.format(record)
        self.log_buffer += msg + "\n"
        self.widget.code(self.log_buffer)


def setup_logger(name: str, widget) -> logging.Logger:
    """
    Configura e retorna um logger para uso no Streamlit
    
    Args:
        name: Nome do logger
        widget: Widget do Streamlit para exibir os logs
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Remove handlers existentes para evitar duplicação
    if logger.handlers:
        logger.handlers.clear()
    
    # Adiciona o handler customizado
    handler = StreamlitHandler(widget)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger