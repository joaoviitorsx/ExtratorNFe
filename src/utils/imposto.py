from src.utils.converte import conversorTexto

def extratorICMS(imposto, ns):
    icms_data = {}
    icms_tag = imposto.find("nfe:ICMS", namespaces=ns) if imposto is not None else None
    if icms_tag is not None:
        for icms_tipo in icms_tag:
            for elem in icms_tipo.iterchildren():
                icms_data[elem.tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")] = conversorTexto(elem)
    return icms_data

def extratorIPI(imposto, ns):
    ipi_data = {}
    ipi_tag = imposto.find("nfe:IPI", namespaces=ns) if imposto is not None else None
    if ipi_tag is not None:
        for ipi_tipo in ipi_tag:
            for elem in ipi_tipo.iterchildren():
                ipi_data[elem.tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")] = conversorTexto(elem)
    return ipi_data

def extratorPIS(imposto, ns):
    pis_data = {}
    pis_tag = imposto.find("nfe:PIS", namespaces=ns) if imposto is not None else None
    if pis_tag is not None:
        for pis_tipo in pis_tag:
            for elem in pis_tipo.iterchildren():
                pis_data[elem.tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")] = conversorTexto(elem)
    return pis_data

def extratorCOFINS(imposto, ns):
    cofins_data = {}
    cofins_tag = imposto.find("nfe:COFINS", namespaces=ns) if imposto is not None else None
    if cofins_tag is not None:
        for cofins_tipo in cofins_tag:
            for elem in cofins_tipo.iterchildren():
                cofins_data[elem.tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")] = conversorTexto(elem)
    return cofins_data