import re

from alr_spec.replacers.arch_replacer import ArchReplacer
from alr_spec.replacers.base import BaseReplacer


class SourcesReplacer(BaseReplacer):
    SOURCE_PATTERN = r"^source(?:_(x86_64|i686|armv7h|aarch64))?$"

    def process(self):
        root_node = self.tree.root_node

        def find_replacements(node):
            if node.type == "variable_name":
                var_name = self._node_text(node)
                re_match = re.match(self.SOURCE_PATTERN, var_name)

                if re_match:
                    arch = re_match.group(1)
                    self.replaces.append(
                        {
                            "node": node,
                            "content": (
                                f"sources_{ArchReplacer.ARCH_MAPPING[arch]}"
                                if arch
                                else "sources"
                            ),
                        }
                    )

            for child in node.children:
                find_replacements(child)

        find_replacements(root_node)
        return self._apply_replacements()
