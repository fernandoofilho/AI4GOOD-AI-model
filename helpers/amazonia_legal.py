class AmazoniaLegal:
    BASE_PATH = '../dados/{sigla}'
    
    estados = {
        "ACRE": "AC",
        "AMAZONAS": "AM",
        "AMAPA": "AP",
        "MATO_GROSSO": "MT",
        "PARA": "PA",
        "RONDONIA": "RO",
        "RORAIMA": "RR",
        "TOCANTINS": "TO",
    }
    
    @classmethod
    def get_paths(cls):
        """
        Retorna os caminhos completos das pastas baseados nas siglas dos estados.
        """
        return [cls.BASE_PATH.format(sigla=sigla) for sigla in cls.estados.values()]
