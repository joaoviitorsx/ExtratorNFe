import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.service.parseNFe import parseNFe

class ExtratorService:
    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers

    def processarPasta(self, pasta_path: str):
        notas_validas = []
        notas_canceladas = []
        arquivos_com_problema = []

        arquivos_xml = [
            os.path.join(pasta_path, f)
            for f in os.listdir(pasta_path)
            if os.path.isfile(os.path.join(pasta_path, f))
        ]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.processamentoArquivos, arquivo): arquivo for arquivo in arquivos_xml}

            for future in as_completed(futures):
                arquivo = futures[future]
                try:
                    resultado = future.result()

                    if resultado["status"] == "valida":
                        notas_validas.append(resultado["nfe"])

                    elif resultado["status"] == "cancelada":
                        notas_canceladas.append((os.path.basename(arquivo), arquivo)) 

                    else:
                        arquivos_com_problema.append((os.path.basename(arquivo), arquivo))

                except Exception:
                    arquivos_com_problema.append((os.path.basename(arquivo), arquivo))

        return {
            "validas": notas_validas,
            "canceladas": notas_canceladas,
            "erros": arquivos_com_problema
        }

    def processamentoArquivos(self, arquivo_path: str):
        if not arquivo_path.lower().endswith(".xml"):
            return {"status": "erro"}

        nfe = parseNFe(arquivo_path)

        if nfe is None:
            return {"status": "erro"}

        if nfe.status == "autorizada":
            return {"status": "valida", "nfe": nfe}
        elif nfe.status == "cancelada":
            return {"status": "cancelada"}
        else:
            return {"status": "erro"}

    def processarArquivos(self, arquivo_path: str):
        notas_validas = []
        notas_canceladas = []
        arquivos_com_problema = []

        resultado = self.processamentoArquivos(arquivo_path)

        if resultado["status"] == "valida":
            notas_validas.append(resultado["nfe"])
        elif resultado["status"] == "cancelada":
            notas_canceladas.append((os.path.basename(arquivo_path), arquivo_path))
        else:
            arquivos_com_problema.append((os.path.basename(arquivo_path), arquivo_path))

        return {
            "validas": notas_validas,
            "canceladas": notas_canceladas,
            "erros": arquivos_com_problema
        }
