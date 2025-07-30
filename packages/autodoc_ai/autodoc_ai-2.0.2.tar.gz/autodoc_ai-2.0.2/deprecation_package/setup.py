"""Deprecation package for autodoc-ai."""
import sys
from setuptools import setup

# Show deprecation notice during installation
print("\n" + "="*60)
print("DEPRECATION NOTICE")
print("="*60)
print("The 'autodoc-ai' package has been renamed to 'autodoc_ai'.")
print("\nPlease uninstall this package and install the new one:")
print("  pip uninstall autodoc-ai")
print("  pip install autodoc_ai")
print("="*60 + "\n")

setup(
    name="autodoc-ai",
    version="1.0.5",
    description="DEPRECATED - Please install autodoc_ai instead",
    long_description="""# DEPRECATED PACKAGE

This package has been renamed from `autodoc-ai` to `autodoc_ai`.

## Please use the new package:

```bash
pip uninstall autodoc-ai
pip install autodoc_ai
```

The new package is available at:
- PyPI: https://pypi.org/project/autodoc_ai/
- GitHub: https://github.com/auraz/autodoc_ai

All functionality remains the same, just with an underscore instead of a hyphen.
""",
    long_description_content_type="text/markdown",
    author="Oleksandr Kryklia",
    author_email="kryklia@gmail.com",
    url="https://github.com/auraz/autodoc_ai",
    py_modules=[],
    install_requires=["autodoc_ai>=2.0.0"],  # Automatically install the new package
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 7 - Inactive",
        "Programming Language :: Python :: 3",
    ],
)