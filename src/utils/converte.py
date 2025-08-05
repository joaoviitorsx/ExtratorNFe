def conversorTexto(elem, default="-"):
    return elem.text.strip() if elem is not None and elem.text else default

def conversorFloat(elem, default=0.0):
    if elem is None or elem.text is None:
        return default

    text = elem.text.strip()
    if text in ["", "-"]:
        return default

    try:
        return float(text)
    except ValueError:
        return default
