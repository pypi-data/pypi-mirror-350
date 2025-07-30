from alr_spec.replacers.base import BaseReplacer


class ArchReplacer(BaseReplacer):
    ARCH_MAPPING = {
        "i686": "386",
        "x86_64": "amd64",
        "armv7h": "arm",
        "aarch64": "arm64",
    }

    def process(self):
        root_node = self.tree.root_node

        def find_replacements(node):
            if node.type == "variable_assignment":
                var_node = node.child_by_field_name("name")
                value_node = node.child_by_field_name("value")

                if var_node and value_node:
                    var_name = self._node_text(var_node)
                    if var_name == "architectures":
                        for item in value_node.children:
                            if item.type == "raw_string":
                                element_text = self._node_text(item)
                                if (
                                    element_text.startswith("'")
                                    and element_text.endswith("'")
                                ) or (
                                    element_text.startswith('"')
                                    and element_text.endswith('"')
                                ):
                                    quote_char = element_text[0]
                                    arch = element_text[1:-1]
                                else:
                                    arch = element_text

                                new_arch = self.ARCH_MAPPING.get(arch, arch)
                                new_element_text = (
                                    f"{quote_char}{new_arch}{quote_char}"
                                )

                                self.replaces.append(
                                    {
                                        "node": item,
                                        "content": new_element_text,
                                    }
                                )

            for child in node.children:
                find_replacements(child)

        find_replacements(root_node)
        return self._apply_replacements()
