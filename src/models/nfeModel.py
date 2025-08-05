from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class NFeItemModel:
    nItem: str
    cProd: str
    cEAN: str
    xProd: str
    NCM: str
    CFOP: str
    qCom: float
    vUnCom: float
    vProd: float
    vFrete: float
    vSeg: float
    vDesc: float
    vOutro: float
    cEANTrib: str
    uTrib: str
    qTrib: float
    vUnTrib: float
    indTot: str
    icms: Dict[str, Optional[str]] = field(default_factory=dict)
    ipi: Dict[str, Optional[str]] = field(default_factory=dict)
    pis: Dict[str, Optional[str]] = field(default_factory=dict)
    cofins: Dict[str, Optional[str]] = field(default_factory=dict)


@dataclass
class NFeModel:
    chave: str
    numero: str
    serie: str
    data_emissao: str
    data_saida: str

    # fornecedor
    emitente_nome: str
    emitente_cnpj: str
    emitente_ie: str

    # cliente
    destinatario_nome: str
    destinatario_cnpj: str
    destinatario_ie: str

    # itens
    itens: List[NFeItemModel]

    # Totais gerais
    totais: Dict[str, Optional[str]] = field(default_factory=dict)

    # adicionais
    informacoes_adicionais: Optional[str] = None

    # NOVO campo
    status: str = "autorizada"