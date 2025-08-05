from lxml import etree
from typing import Optional
from src.models.nfeModel import NFeModel, NFeItemModel
from src.utils.converte import conversorTexto, conversorFloat
from src.utils.imposto import extratorICMS, extratorIPI, extratorPIS, extratorCOFINS

def parseNFe(file_path: str) -> Optional[NFeModel]:
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
    except Exception:
        return None

    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}
    status = "autorizada"

    evento_cancel = root.find(".//nfe:procEventoNFe", namespaces=ns)
    if evento_cancel is not None:
        tpEvento = evento_cancel.find(".//nfe:tpEvento", namespaces=ns)
        if tpEvento is not None and tpEvento.text == "110111":
            status = "cancelada"

    prot = root.find(".//nfe:protNFe", namespaces=ns)
    if prot is not None:
        cStat = prot.find(".//nfe:cStat", namespaces=ns)
        if cStat is not None and cStat.text not in ["100", "150"]:
            status = "rejeitada"

    inf_nfe = root.find(".//nfe:infNFe", namespaces=ns)
    if inf_nfe is None:
        return None

    chave = inf_nfe.get("Id", "-").replace("NFe", "")

    ide = inf_nfe.find("nfe:ide", namespaces=ns)
    numero = conversorTexto(ide.find("nfe:nNF", namespaces=ns))
    serie = conversorTexto(ide.find("nfe:serie", namespaces=ns))
    data_emissao = conversorTexto(ide.find("nfe:dhEmi", namespaces=ns))
    data_saida = conversorTexto(ide.find("nfe:dhSaiEnt", namespaces=ns))

    emit = inf_nfe.find("nfe:emit", namespaces=ns)
    emitente_nome = conversorTexto(emit.find("nfe:xNome", namespaces=ns))
    emitente_cnpj = conversorTexto(emit.find("nfe:CNPJ", namespaces=ns))
    emitente_ie = conversorTexto(emit.find("nfe:IE", namespaces=ns))

    dest = inf_nfe.find("nfe:dest", namespaces=ns)
    destinatario_nome = conversorTexto(dest.find("nfe:xNome", namespaces=ns))
    destinatario_cnpj = conversorTexto(dest.find("nfe:CNPJ", namespaces=ns))
    destinatario_ie = conversorTexto(dest.find("nfe:IE", namespaces=ns))

    itens = []
    for det in inf_nfe.findall("nfe:det", namespaces=ns):
        nItem = det.get("nItem", "-")

        prod = det.find("nfe:prod", namespaces=ns)
        imposto = det.find("nfe:imposto", namespaces=ns)

        cProd = conversorTexto(prod.find("nfe:cProd", namespaces=ns))
        cEAN = conversorTexto(prod.find("nfe:cEAN", namespaces=ns))
        xProd = conversorTexto(prod.find("nfe:xProd", namespaces=ns))
        NCM = conversorTexto(prod.find("nfe:NCM", namespaces=ns))
        CFOP = conversorTexto(prod.find("nfe:CFOP", namespaces=ns))

        qCom = conversorFloat(prod.find("nfe:qCom", namespaces=ns))
        vUnCom = conversorFloat(prod.find("nfe:vUnCom", namespaces=ns))
        vProd = conversorFloat(prod.find("nfe:vProd", namespaces=ns))
        vFrete = conversorFloat(prod.find("nfe:vFrete", namespaces=ns))
        vSeg = conversorFloat(prod.find("nfe:vSeg", namespaces=ns))
        vDesc = conversorFloat(prod.find("nfe:vDesc", namespaces=ns))
        vOutro = conversorFloat(prod.find("nfe:vOutro", namespaces=ns))
        cEANTrib = conversorTexto(prod.find("nfe:cEANTrib", namespaces=ns))
        uTrib = conversorTexto(prod.find("nfe:uTrib", namespaces=ns))
        qTrib = conversorFloat(prod.find("nfe:qTrib", namespaces=ns))
        vUnTrib = conversorFloat(prod.find("nfe:vUnTrib", namespaces=ns))
        indTot = conversorTexto(prod.find("nfe:indTot", namespaces=ns))

        icms_data = extratorICMS(imposto, ns)
        ipi_data = extratorIPI(imposto, ns)
        pis_data = extratorPIS(imposto, ns)
        cofins_data = extratorCOFINS(imposto, ns)

        item = NFeItemModel(
            nItem=nItem,
            cProd=cProd,
            cEAN=cEAN,
            xProd=xProd,
            NCM=NCM,
            CFOP=CFOP,
            qCom=qCom,
            vUnCom=vUnCom,
            vProd=vProd,
            vFrete=vFrete,
            vSeg=vSeg,
            vDesc=vDesc,
            vOutro=vOutro,
            cEANTrib=cEANTrib,
            uTrib=uTrib,
            qTrib=qTrib,
            vUnTrib=vUnTrib,
            indTot=indTot,
            icms=icms_data,
            ipi=ipi_data,
            pis=pis_data,
            cofins=cofins_data
        )
        itens.append(item)

    totais = {}
    total_tag = inf_nfe.find("nfe:total/nfe:ICMSTot", namespaces=ns)
    if total_tag is not None:
        for child in total_tag.iterchildren():
            totais[child.tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")] = conversorTexto(child)

    inf_adic_tag = inf_nfe.find("nfe:infAdic", namespaces=ns)
    inf_adic = conversorTexto(inf_adic_tag.find("nfe:infCpl", namespaces=ns)) if inf_adic_tag is not None else None

    return NFeModel(
        chave=chave,
        numero=numero,
        serie=serie,
        data_emissao=data_emissao,
        data_saida=data_saida,
        emitente_nome=emitente_nome,
        emitente_cnpj=emitente_cnpj,
        emitente_ie=emitente_ie,
        destinatario_nome=destinatario_nome,
        destinatario_cnpj=destinatario_cnpj,
        destinatario_ie=destinatario_ie,
        itens=itens,
        totais=totais,
        informacoes_adicionais=inf_adic,
        status=status
    )
