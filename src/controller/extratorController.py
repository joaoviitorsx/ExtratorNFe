from src.service.extratorService import ExtratorService
from src.service.exportarService import ExportarService

class ExtratorController:
    def __init__(self):
        self.extrator_service = ExtratorService()
        self.export_service = ExportarService()
        self._resultado_processado = None

    def processarPasta(self, pasta_xml: str, progresso_callback=None) -> dict:
        try:
            self._resultado_processado = self.extrator_service.processarPasta(pasta_xml)

            total_arquivos = (
                len(self._resultado_processado.get("validas", [])) +
                len(self._resultado_processado.get("canceladas", [])) +
                len(self._resultado_processado.get("erros", []))
            )

            arquivos_erro = self._resultado_processado.get("erros", [])
            arquivos_cancelados = self._resultado_processado.get("canceladas", [])
            qtd_validos = len(self._resultado_processado.get("validas", []))
            qtd_cancelados = len(arquivos_cancelados)
            qtd_erros = len(arquivos_erro)

            return {
                "status": "sucesso",
                "mensagem": "Arquivos XML processados com sucesso.",
                "total": total_arquivos,
                "validos": qtd_validos,
                "cancelados": qtd_cancelados,
                "erros": qtd_erros,
                "lista_erros": arquivos_erro,
                "lista_cancelados": arquivos_cancelados
            }

        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro ao processar pasta: {str(e)}",
                "total": 0,
                "validos": 0,
                "cancelados": 0,
                "erros": 0,
                "lista_erros": [],
                "lista_cancelados": []
            }

    def exportarPlanilha(self, caminho_saida: str):
        try:
            if not self._resultado_processado:
                return {"status": "erro", "mensagem": "Nenhum processamento encontrado. Execute o processamento primeiro."}

            notas_validas = self._resultado_processado.get("validas", [])

            if not notas_validas:
                return {"status": "erro", "mensagem": "Nenhuma NF-e válida para exportar."}

            caminho_final = self.export_service.gerarPlanilha(self._resultado_processado, caminho_saida)

            total_arquivos = (
                len(self._resultado_processado.get("validas", [])) +
                len(self._resultado_processado.get("canceladas", [])) +
                len(self._resultado_processado.get("erros", []))
            )

            arquivos_erro = self._resultado_processado.get("erros", [])
            arquivos_cancelados = self._resultado_processado.get("canceladas", [])
            qtd_validos = len(self._resultado_processado.get("validas", []))
            qtd_cancelados = len(arquivos_cancelados)
            qtd_erros = len(arquivos_erro)

            return {
                "status": "sucesso",
                "mensagem": f"Planilha salva em: {caminho_final}",
                "arquivo": caminho_final,
                "total": total_arquivos,
                "validos": qtd_validos,
                "cancelados": qtd_cancelados,
                "erros": qtd_erros,
                "lista_erros": arquivos_erro,
                "lista_cancelados": arquivos_cancelados
            }

        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro ao exportar a planilha: {str(e)}"}