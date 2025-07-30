import os
from typing import Any, Dict, List

import yaml

from .reference import create_file_references


def assemble_payload(
    components: List[Dict[str, Any]],
    base_dir: str,
) -> str:
    """
    - If a component has a 'text' key, emit that text verbatim.
    - Otherwise it must have 'name' and 'files':
        optional 'prefix' (above the attachment) and 'suffix' (below).
      Files and directories are expanded via create_file_references().
    - if 'wrap' key is present:
        * wrap == "md" → wrap the inner content in a markdown code fence
        * wrap == other string → wrap inner content in <wrap>…</wrap>
    """
    parts: List[str] = []

    for comp in components:
        wrap_mode = comp.get("wrap")  # may be None, "md", or any tag name

        # 1) text‐only
        if "text" in comp:
            text = comp["text"].rstrip()
            if wrap_mode:
                if wrap_mode.lower() == "md":
                    text = "```\n" + text + "\n```"
                else:
                    text = f"<{wrap_mode}>\n{text}\n</{wrap_mode}>"
            parts.append(text)
            continue

        # 2) file component
        name = comp.get("name")
        files = comp.get("files")
        if not name or not files:
            raise ValueError(
                f"Component must have either 'text' or both 'name' & 'files': {comp}"
            )

        prefix = comp.get("prefix", "").rstrip()
        suffix = comp.get("suffix", "").lstrip()

        # collect FileReference objects (recursing into directories)
        all_refs = []
        for rel in files:
            rel_expanded = os.path.expanduser(rel)
            full = (
                rel_expanded
                if os.path.isabs(rel_expanded)
                else os.path.join(base_dir, rel_expanded)
            )
            if not os.path.exists(full):
                raise FileNotFoundError(f"Component '{name}' path not found: {full}")
            refs = create_file_references(
                [full], ignore_paths=None, format="md", label="relative"
            )["refs"]
            all_refs.extend(refs)

        attachment_lines = [f'<attachment label="{name}">']
        for idx, ref in enumerate(all_refs):
            attachment_lines.append(ref.output)
            if idx < len(all_refs) - 1:
                attachment_lines.append("")
        attachment_lines.append("</attachment>")
        inner = "\n".join(attachment_lines)

        if wrap_mode:
            if wrap_mode.lower() == "md":
                inner = "```\n" + inner + "\n```"
            else:
                inner = f"<{wrap_mode}>\n{inner}\n</{wrap_mode}>"

        block_lines: List[str] = []
        if prefix:
            block_lines.append(prefix)
        block_lines.append(inner)
        if suffix:
            block_lines.append(suffix)

        parts.append("\n".join(block_lines))

    return "\n\n".join(parts)


def render_from_yaml(
    manifest_path: str,
) -> str:
    """
    Load YAML with top-level:
      config:
        root:  # optional, expands ~
      components:
        - text: ...
        - name: ...; prefix/suffix?; files: [...]
        - wrap:  # optional
    """
    with open(manifest_path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if not isinstance(data, dict):
        raise ValueError("Manifest must be a mapping with 'config' and 'components'")

    cfg = data.get("config", {})
    if "root" in cfg:
        raw = cfg["root"] or "~"
        base_dir = os.path.expanduser(raw)
    else:
        base_dir = os.path.dirname(os.path.abspath(manifest_path))

    comps = data.get("components")
    if not isinstance(comps, list):
        raise ValueError("'components' must be a list")

    return assemble_payload(comps, base_dir)
