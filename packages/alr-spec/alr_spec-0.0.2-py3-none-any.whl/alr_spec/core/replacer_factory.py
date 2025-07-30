from typing import TYPE_CHECKING

from alr_spec.replacers.base import BaseReplacer
from alr_spec.replacers.sources import Utils

if TYPE_CHECKING:
    from tree_sitter import Node


def get_version_replacer_class(field, value):
    class VersionReplacer(BaseReplacer):
        def __init__(self, content, tree, ctx=None):
            super().__init__(content, tree, ctx)

        def process(self):
            root_node = self.tree.root_node

            def find_replacements(node: "Node"):
                for child in node.children:
                    if child.type == "variable_assignment":
                        res = Utils.parse_variable_assignment(child)
                        if res is not None:
                            var_node, value_node = res
                            var_name = self._node_text(var_node)

                            if var_name == field:
                                if value_node.type in [
                                    "string",
                                    "word",
                                    "number",
                                ]:
                                    self.replaces.append(
                                        {
                                            "node": value_node,
                                            "content": value,
                                        }
                                    )
                                else:
                                    print(value_node.type)

            find_replacements(root_node)
            return self._apply_replacements()

    return VersionReplacer
