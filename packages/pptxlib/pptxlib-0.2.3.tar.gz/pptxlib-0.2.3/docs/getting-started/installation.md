# Installation

## Prerequisites

Before installing pptxlib, ensure you have the following:

- Windows operating system
- Microsoft PowerPoint installed on your system
- Python 3.11 or higher

## Installation Methods

### Using uv

The recommended way to install pptxlib is using uv:

```bash
uv pip install pptxlib
```

### Using pip

An alternative way to install pptxlib is using pip:

```bash
pip install pptxlib
```

## Verifying Installation

To verify the installation, you can run Python and
check if the package is installed and if PowerPoint is available:

```python exec="1" source="material-block"
from pptxlib import is_powerpoint_available

is_powerpoint_available()
```
