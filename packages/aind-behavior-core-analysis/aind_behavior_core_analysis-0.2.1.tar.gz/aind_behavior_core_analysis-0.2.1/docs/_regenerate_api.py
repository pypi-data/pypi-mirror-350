#!/usr/bin/env uv run
"""
Script to regenerate the API documentation structure in mkdocs.yml
based on the current state of the library.
"""

import logging
from pathlib import Path

import yaml

# Constants
ROOT_DIR = Path(__file__).parent.parent
PACKAGE_NAME = "aind_behavior_core_analysis"
SRC_DIR = ROOT_DIR / "src" / f"{PACKAGE_NAME}"
DOCS_DIR = ROOT_DIR / "docs"
API_DIR = DOCS_DIR / "api"
MKDOCS_YML = ROOT_DIR / "mkdocs.yml"
API_LABEL = "API Reference"

# Leaving this manual for now.
DOCUMENTED_MODULES = ["contract", "qc"]

log = logging.getLogger("mkdocs")


def on_pre_build(config):
    main()


def find_modules(base_dir, module_name):
    """Find all Python modules in the given directory."""
    modules = []
    dir_path = base_dir / module_name

    if not dir_path.is_dir():
        return modules

    if (dir_path / "__init__.py").exists():
        modules.append(("core", f"{module_name}"))

    for item in dir_path.iterdir():
        if item.is_file() and item.suffix == ".py" and not item.name.startswith("_"):
            modules.append((item.stem, f"{module_name}.{item.stem}"))

    modules.sort(key=lambda x: x[0])

    return modules


def generate_api_structure():
    """Generate the API documentation structure."""
    api_structure = {}

    for module_name in DOCUMENTED_MODULES:
        module_structure = []
        modules = find_modules(SRC_DIR, module_name)

        for name, import_path in modules:
            md_file = f"api/{module_name}/{name}.md"

            (API_DIR / module_name).mkdir(parents=True, exist_ok=True)

            with open(DOCS_DIR / md_file, "w") as f:
                f.write(f"# {import_path}\n\n")
                f.write(f"::: {PACKAGE_NAME}.{import_path}\n")

            module_structure.append({name: md_file})

        api_structure[module_name] = module_structure

    return api_structure


def update_mkdocs_yml(api_structure):
    """Rewrite the mkdocs.yml overriding the API Reference section only!."""
    with open(MKDOCS_YML, "r") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav")
    for entry in nav:
        if isinstance(entry, dict) and API_LABEL in entry:
            api_ref = ["api/index.md"]
            for module_name, module_content in api_structure.items():
                api_ref.append({module_name.capitalize(): module_content})
            entry[API_LABEL] = api_ref

    with open(MKDOCS_YML, "w+") as f:
        yaml.dump(config, f, sort_keys=False, default_flow_style=False)


def main():
    """Main function."""
    log.info("Regenerating API documentation...")

    # Generate API structure
    api_structure = generate_api_structure()

    # Update mkdocs.yml
    update_mkdocs_yml(api_structure)

    log.info("API documentation regenerated successfully.")


if __name__ == "__main__":
    main()
