"""Tests for the image downloader."""

from pathlib import Path

from image_downloader.downloader import safe_filename


def test_safe_filename_replaces_invalid_characters() -> None:
    assert safe_filename("Phone/Tablet: 128 GB") == "Phone,Tablet, 128 GB"


def test_safe_filename_removes_redundant_whitespace() -> None:
    assert safe_filename("  Product   Name  ") == "Product Name"


def test_safe_filename_uses_fallback_for_empty_name() -> None:
    assert safe_filename("   ") == "image"
