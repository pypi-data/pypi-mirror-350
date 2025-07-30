"""
Tests for the dolze-templates package.
"""

import unittest
import json
from dolze_templates import (
    get_template_registry,
    get_template_content,
    check_section_variant_exists,
    get_section_variants_from_registry,
    get_sample_json
)

class TestTemplates(unittest.TestCase):
    """Test the dolze-templates package."""

    def test_get_template_registry(self):
        """Test getting the template registry."""
        registry = get_template_registry()
        self.assertIsInstance(registry, dict)
        self.assertIn('brand_product_physical', registry)
        self.assertIn('brand_service_physical', registry)
        self.assertIn('brand_service_digital_saas', registry)

    def test_get_template_content(self):
        """Test getting template content."""
        content = get_template_content('layouts/brand_product_physical.html')
        self.assertIsInstance(content, str)
        self.assertTrue('<!DOCTYPE html>' in content.lower() or '<html' in content.lower())

    def test_check_section_variant_exists(self):
        """Test checking if a section variant exists."""
        self.assertTrue(check_section_variant_exists('navigation', 'v1'))
        self.assertFalse(check_section_variant_exists('nonexistent', 'v1'))

    def test_get_section_variants_from_registry(self):
        """Test getting section variants from the registry."""
        variants = get_section_variants_from_registry('brand_product_physical', 'index')
        self.assertIsInstance(variants, dict)
        self.assertIn('navigation', variants)
        self.assertEqual(variants['navigation'], 'v1')

    def test_get_sample_json(self):
        """Test getting the sample JSON."""
        sample = get_sample_json()
        self.assertIsInstance(sample, dict)
        self.assertIn('settings', sample)
        self.assertIn('sections', sample)

if __name__ == '__main__':
    unittest.main()
