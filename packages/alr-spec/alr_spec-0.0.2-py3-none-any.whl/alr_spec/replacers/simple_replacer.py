from alr_spec.replacers.base import BaseReplacer


class SimpleReplacer(BaseReplacer):
    SIMPLE_REPLACEMENTS = {
        "pkgname": "name",
        "pkgver": "version",
        "pkgrel": "release",
        "pkgdesc": "desc",
        "url": "homepage",
        "arch": "architectures",
        "depends": "deps",
        "optdepends": "opt_deps",
    }

    def process(self):
        root_node = self.tree.root_node

        def find_replacements(node):
            if node.type == "variable_name":
                var_name = self._node_text(node)
                if var_name in self.SIMPLE_REPLACEMENTS:
                    self.replaces.append(
                        {
                            "node": node,
                            "content": self.SIMPLE_REPLACEMENTS[var_name],
                        }
                    )
            for child in node.children:
                find_replacements(child)

        find_replacements(root_node)
        return self._apply_replacements()
