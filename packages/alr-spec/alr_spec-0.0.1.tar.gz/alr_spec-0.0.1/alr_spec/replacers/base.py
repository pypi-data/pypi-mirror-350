from typing import TYPE_CHECKING

from typing_extensions import List, TypedDict

if TYPE_CHECKING:
    from tree_sitter import Node, Tree


class Replaces(TypedDict):
    node: "Node"
    content: str


class Appends(TypedDict):
    node: "Node"
    content: str


class BaseReplacer:
    def __init__(self, content, tree: "Tree", ctx: dict | None = None):
        self.content = content
        self.tree = tree
        self.replaces: List[Replaces] = []
        self.appends: List[Appends] = []
        self.ctx = ctx

    def _node_text(self, node: "Node"):
        """Helper function to get the text of a node."""
        return self.content[node.start_byte : node.end_byte].decode("utf-8")

    def _apply_replacements(self):
        """Apply the replacements to the content and edit the tree."""
        new_content = bytearray(self.content)
        for replace_info in sorted(
            self.replaces,
            key=lambda x: (x["node"].start_byte, x["node"].end_byte),
            reverse=True,
        ):
            start, end = (
                replace_info["node"].start_byte,
                replace_info["node"].end_byte,
            )
            replacement = replace_info["content"].encode("utf-8")
            new_content[start:end] = replacement

            self.tree.edit(
                start_byte=start,
                old_end_byte=end,
                new_end_byte=start + len(replacement),
                start_point=replace_info["node"].start_point,
                old_end_point=replace_info["node"].end_point,
                new_end_point=(
                    replace_info["node"].start_point[0],
                    replace_info["node"].start_point[1] + len(replacement),
                ),
            )

        for append_info in sorted(
            self.appends,
            key=lambda x: x["node"].end_byte,
            reverse=True,
        ):
            insertion_point = append_info["node"].end_byte
            append_content = append_info["content"].encode("utf-8")
            new_content[insertion_point:insertion_point] = append_content

            self.tree.edit(
                start_byte=insertion_point,
                old_end_byte=insertion_point,
                new_end_byte=insertion_point + len(append_content),
                start_point=append_info["node"].end_point,
                old_end_point=append_info["node"].end_point,
                new_end_point=(
                    append_info["node"].end_point[0],
                    append_info["node"].end_point[1] + len(append_content),
                ),
            )

        return new_content

    def process(self):
        raise NotImplementedError("Subclasses should implement this method.")
