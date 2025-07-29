from androguard.core.axml import AXMLPrinter

from .vd2png import Vd2PngConverter
from PIL import Image
from io import BytesIO


def layer_from_color(color):
    alpha = 255
    if len(color) > 6:  # ARGB
        color = color[1:]
        alpha = int(color[:2], 16)
        color = "#" + color[2:]  # RGB

    image = Image.new("RGB", (512, 512), color)
    image.putalpha(alpha)
    return image


def _axml2png(axml, apk):
    icon_element = AXMLPrinter(axml).get_xml_obj()
    if icon_element.tag == 'layer-list':
        parts = []
        for item in icon_element.findall(".//item"):
            parts.append(list(item.values())[0])
        parts = [
            apk._resolve_icon_resource(p[1:], 65536) if p.startswith("@") else p
            for p in parts
        ]
        parts = [p for p in parts if p]
        parts = [(p, None if p.startswith("#") else apk.get_file(p)) for p in parts]
        img = build_icon(apk, parts)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr
    else:
        out = BytesIO()
        converter = Vd2PngConverter(apk)
        converter.vd2png(BytesIO(AXMLPrinter(axml).get_xml()), out, 10)
        return out


def build_icon(apk, parts):
    layers = [
        layer_from_color(name)
        if name.startswith("#")
        else Image.open(
            _axml2png(content, apk)
            if name.endswith(".xml")
            else BytesIO(content)
        )
        for name, content in parts
    ]

    if len(layers) == 1:
        icon = layers[0]
    else:
        layers = [l.convert("RGBA") for l in layers]
        min_size = min(layers, key=lambda x: x.size).size
        layers = [l if l.size == min_size else l.resize(min_size) for l in layers]
        icon = Image.alpha_composite(*layers)
    return icon
