import logging

from androguard.core.apk import APK
from androguard.core.axml import AXMLPrinter

from apklisparser.build_icon import build_icon


class APK(APK):
    def extract_icon(self, filename, max_dpi=65536):
        """
        Extract application icon in `filename` location
        :param filename:
        :return:
        """
        icon = self.get_app_icon()
        if icon.endswith(".xml"):
            icon_element = AXMLPrinter(self.get_file(icon)).get_xml_obj()
            if icon_element.tag in ('adaptative-icon', 'adaptive-icon'):
                parts = []
                try:
                    bg = self.get_part(icon_element, 'background')
                    if bg is not None and len(bg.values()) > 0:
                        parts.append(list(bg.values())[0].replace("android:", ""))
                except:
                    pass

                try:
                    fg = self.get_part(icon_element, 'foreground')
                    if fg is not None and len(fg.values()) > 0:
                        parts.append(list(fg.values())[0].replace("android:", ""))
                except:
                    pass
            else:
                parts = [list(icon_element.attrib.values())[0]]

            parts = [
                self._resolve_icon_resource(p[1:], max_dpi) if p.startswith("@") else p
                for p in parts
            ]
        else:
            parts = [icon]

        parts = [p for p in parts if p]  # Filtramos partes inválidas
        parts = [(p, None if p.startswith("#") else self.get_file(p)) for p in parts]

        icon = build_icon(self, parts)
        icon.save(filename)

    def get_part(self, tree, key):
        element = tree.find(key)
        if element and len(element.values()) == 0:
            element = element.find('inset')

        return element

    def _resolve_icon_resource(self, res, max_dpi):
        res_id = int(res, 16)
        res_parser = self.get_android_resources()
        candidates = res_parser.get_resolved_res_configs(res_id)

        res = None
        current_dpi = -1

        try:
            for config, file_name in candidates:
                dpi = config.get_density()
                if current_dpi < dpi <= max_dpi:
                    res = file_name
                    current_dpi = dpi
        except Exception as e:
            logging.error("Exception selecting application res: %s" % e)
        return res