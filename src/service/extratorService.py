import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.service.parseNFe import parseNFe

class ExtratorService:
    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers

    def processarPasta(self, pasta_path: str, progresso_callback=None):
        notas_validas = []
        notas_canceladas = []
        arquivos_com_problema = []

        arquivos_xml = []
        for root, _, files in os.walk(pasta_path):
            for f in files:
                if f.lower().endswith(".xml"):
                    arquivos_xml.append(os.path.join(root, f))

        total_arquivos = len(arquivos_xml)
        processados = 0

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

                processados += 1
                if progresso_callback:
                    progresso_callback(processados, total_arquivos)

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
