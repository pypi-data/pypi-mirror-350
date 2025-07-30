import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tree_sitter import Node

from alr_spec.replacers.arch_replacer import ArchReplacer
from alr_spec.replacers.base import BaseReplacer


class StringValue(str):
    def __init__(self, node: "Node"):
        self.node = node

    def get_text_value(self) -> str:
        value = self.node.text.decode("utf-8")
        return value[1:-1]

    def get_quote(self) -> str:
        value = self.node.text.decode("utf-8")
        return value[0]

    def __repr__(self):
        return self.node.text.decode("utf-8")

    def __str__(self):
        return self.__repr__()


class Utils:
    def parse_variable_assignment(
        node: "Node",
    ) -> tuple["Node", "Node"] | None:
        var_node = node.child_by_field_name("name")
        value_node = node.child_by_field_name("value")

        if not (var_node and value_node):
            return None

        return (var_node, value_node)

    def get_string_values_from_array(node: "Node"):
        arr = []
        for item in node.children:
            if (
                item.type == "string"
                or item.type == "raw_string"
                or item.type == "concatenation"
            ):
                arr.append(StringValue(item))

        return arr


CHECKSUMS_REPLACEMENTS = {
    "b2sums": "blake2b-512",
    "sha512sums": "sha512",
    "sha384sums": "sha384",
    "sha256sums": "sha256",
    "sha224sums": "sha224",
    "sha1sums": "sha1",
    "md5sums": "md5",
}

SOURCE_PATTERN = r"^source(?:_(x86_64|i686|armv7h|aarch64))?$"
CHECKSUMS_PATTERN = (
    r"^(b2sums|sha512sums|sha384sums|sha256sums|sha224sums|sha1sums|md5sums)"
    r"(?:_(x86_64|i686|armv7h|aarch64))?$"
)


class SourcesReplacer(BaseReplacer):
    def process(self):
        root_node = self.tree.root_node

        self.local_files = []
        self.prepare_func_body = None

        self.nodes_to_remove = []

        sources = dict()
        checksums = dict()

        def execute(node: "Node"):
            if node.type == "function_definition":
                func_name = self._node_text(node.child_by_field_name("name"))
                if func_name != "prepare":
                    return
                self.prepare_func_body = node
                return

            if node.type == "variable_assignment":
                var_node = node.child_by_field_name("name")
                value_node = node.child_by_field_name("value")
                if not (var_node and value_node):
                    return

                var_name = self._node_text(var_node)

                re_match = re.match(SOURCE_PATTERN, var_name)
                if re_match:
                    self.nodes_to_remove.append(node)

                    arch = re_match.group(1)
                    sources[arch if arch else "-"] = (
                        Utils.get_string_values_from_array(value_node)
                    )

                re_match = re.match(CHECKSUMS_PATTERN, var_name)
                if re_match:
                    self.nodes_to_remove.append(node)

                    checksum = CHECKSUMS_REPLACEMENTS[re_match.group(1)]
                    arch = re_match.group(2)

                    checksums[arch if arch else "-"] = [
                        f"'{checksum}:{v.get_text_value()}'"
                        for v in Utils.get_string_values_from_array(value_node)
                    ]

        def traverse(node: "Node"):
            execute(node)
            for child in node.children:
                traverse(child)

        traverse(root_node)

        content = ""

        for node in self.nodes_to_remove:
            self.replaces.append({"node": node, "content": ""})

        for arch, files in sources.items():
            source_files = []
            checksums_str = []

            for i, file in enumerate(files):
                file_name = file.get_text_value()
                if "://" in file_name:
                    source_files.append(file)
                    checksums_str.append(checksums[arch][i])
                else:
                    self.local_files.append(file)

            content += self.source_to_str(arch, source_files) + "\n"
            content += self.checksums_to_str(arch, checksums_str) + "\n"

        if len(self.local_files) > 0:
            copy_commands = "\n    ".join(
                f'cp "${{scriptdir}}/{file.get_text_value()}" "${{srcdir}}"'
                for file in self.local_files
            )

            prepare_func_content = f"""
    {copy_commands}
"""
            if self.prepare_func_body is not None:
                text = self._node_text(self.prepare_func_body)
                closing_brace_index = text.rfind("}")
                text = (
                    text[:closing_brace_index]
                    + prepare_func_content
                    + text[closing_brace_index:]
                )
                self.replaces.append(
                    {
                        "node": self.prepare_func_body,
                        "content": text,
                    }
                )
            else:
                text = self._node_text(root_node)
                content += f"""
prepare() {{
{prepare_func_content}}}
"""

        self.appends.append(
            {
                "node": root_node,
                "content": content,
            }
        )

        return self._apply_replacements()

    def source_to_str(self, arch, files):
        return f"""
{f"sources_{ArchReplacer.ARCH_MAPPING[arch]}" if arch != '-' else "sources"}=(
  {'\n  '.join([s.__str__() for s in files])}
)"""

    def checksums_to_str(self, arch, files):
        var_name = (
            f"checksums_{ArchReplacer.ARCH_MAPPING[arch]}"
            if arch != "-"
            else "checksums"
        )

        return f"""
{var_name}=(
  {'\n  '.join([s.__str__() for s in files])}
)"""
