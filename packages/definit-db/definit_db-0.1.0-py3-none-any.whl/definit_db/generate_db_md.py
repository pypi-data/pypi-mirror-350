import importlib
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from definit_db.definition.definition import Definition
from definit_db.definition.field import Field

FIELDS = [Field.MATHEMATICS, Field.COMPUTER_SCIENCE]
BASE_SRC = os.path.dirname(__file__)
DATA_PY = os.path.join(BASE_SRC, "data", "field")
DATA_MD = os.path.join(BASE_SRC, "data_md", "field")


def get_field_index(field: Field):
    module = importlib.import_module(f"definit_db_py.data.field.{field}.index")
    return getattr(module, "field_index")


def definition_to_md(defn: Definition) -> str:
    return f"# {defn.key.name}\n\n{defn.content}\n"


def get_md_path(defn: Definition, field: Field) -> str:
    mod = type(defn).__module__
    rel_mod = mod.split("definit_db_py.data.field.", 1)[-1]
    prefix = f"{field}."

    if rel_mod.startswith(prefix):
        rel_mod = rel_mod[len(prefix) :]

    rel_mod = rel_mod.replace(".", os.sep)

    if rel_mod.endswith("__init__"):
        rel_mod = rel_mod[: -len("__init__")]

    md_dir = os.path.join(DATA_MD, field, os.path.dirname(rel_mod))
    os.makedirs(md_dir, exist_ok=True)
    md_path = os.path.join(md_dir, f"{defn.key.name}.md")
    return md_path


def write_index_md(field: Field, field_index: list[Definition]) -> None:
    lines: list[str] = []

    for defn in field_index:
        mod = type(defn).__module__
        rel_mod = mod.split("definit_db_py.data.field.", 1)[-1]
        prefix = f"{field}."

        if rel_mod.startswith(prefix):
            rel_mod = rel_mod[len(prefix) :]

        rel_mod = rel_mod.replace(".", "/")

        if rel_mod.endswith("__init__"):
            rel_mod = rel_mod[: -len("__init__")]

        if rel_mod.startswith("definitions/"):
            rel_mod = rel_mod[len("definitions/") :]

        rel_path = rel_mod.strip("/")
        lines.append(f"- [{defn.key.name}]({rel_path})")

    md_dir = os.path.join(DATA_MD, field)
    os.makedirs(md_dir, exist_ok=True)
    md_path = os.path.join(md_dir, "index.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    for field in FIELDS:
        field_index = get_field_index(field)
        for defn in field_index:
            if not isinstance(defn, Definition):
                continue
            md_path = get_md_path(defn, field)
            md_content = definition_to_md(defn)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
        write_index_md(field, field_index)


if __name__ == "__main__":
    main()
