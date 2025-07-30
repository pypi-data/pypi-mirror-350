"""
Dolze Templates Package

This package provides templates for Dolze landing pages.
"""

import json
import os
import pkgutil
from typing import Dict, Any, Optional

# Cache for template registry and content
_registry_cache = None
_template_content_cache = {}


def get_template_registry() -> Dict[str, Any]:
    """
    Get the template registry configuration.

    Returns:
        Dict[str, Any]: The template registry configuration.
    """
    global _registry_cache

    if _registry_cache is not None:
        return _registry_cache

    try:
        # Use pkgutil to get the template registry
        data = pkgutil.get_data("dolze_templates", "template-registry.json")
        if data:
            _registry_cache = json.loads(data.decode("utf-8"))
            return _registry_cache
        else:
            raise ValueError("Could not load template registry")
    except Exception as e:
        raise ValueError(f"Failed to load template registry: {e}")


def get_template_content(template_path: str) -> str:
    """
    Get the content of a template file.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The content of the template file.
    """
    global _template_content_cache

    if template_path in _template_content_cache:
        return _template_content_cache[template_path]

    try:
        # Normalize the path
        normalized_path = template_path.replace("templates/", "")

        # Use pkgutil to get the template content
        data = pkgutil.get_data("dolze_templates", f"templates/{normalized_path}")
        if data:
            content = data.decode("utf-8")
            _template_content_cache[template_path] = content
            return content
        else:
            raise ValueError(f"Could not load template: {template_path}")
    except Exception as e:
        raise ValueError(f"Failed to load template: {template_path}, error: {e}")


def check_section_variant_exists(section_name: str, variant: str) -> bool:
    """
    Check if a section variant exists in the package.

    Args:
        section_name (str): The name of the section.
        variant (str): The variant ID (e.g., "v1", "v2").

    Returns:
        bool: True if the variant exists, False otherwise.
    """
    try:
        section_path = f"sections/{section_name}/{variant}.html"
        # Try to get the content, if it succeeds, the variant exists
        data = pkgutil.get_data("dolze_templates", f"templates/{section_path}")
        return data is not None
    except Exception:
        return False


def get_section_variants_from_registry(
    template_id: str, page: str = "index"
) -> Optional[Dict[str, str]]:
    """
    Fetch the section_variants mapping for a given template_id and page from the template registry.

    Args:
        template_id (str): The ID of the template.
        page (str, optional): The page slug (e.g., "index", "shop"). Defaults to "index".

    Returns:
        Optional[Dict[str, str]]: A dictionary mapping section names to variant IDs, or None if not found.
    """
    try:
        registry = get_template_registry()
        template_config = registry.get(template_id)
        if template_config and "section_variants" in template_config:
            # Get variants for the specified page
            page_variants = template_config["section_variants"].get(page)
            if page_variants:
                return page_variants
            # If page not found, return None
            return None
        else:
            return None
    except Exception as e:
        print(f"Error reading section_variants from registry: {e}")
        return None


def get_sample_json() -> Dict[str, Any]:
    """
    Get the sample JSON data.

    Returns:
        Dict[str, Any]: The sample JSON data.
    """
    try:
        # Use pkgutil to get the sample JSON
        data = pkgutil.get_data("dolze_templates", "sample.json")
        if data:
            return json.loads(data.decode("utf-8"))
        else:
            raise ValueError("Could not load sample JSON")
    except Exception as e:
        raise ValueError(f"Failed to load sample JSON: {e}")


__all__ = [
    "get_template_registry",
    "get_template_content",
    "check_section_variant_exists",
    "get_section_variants_from_registry",
    "get_sample_json",
]
