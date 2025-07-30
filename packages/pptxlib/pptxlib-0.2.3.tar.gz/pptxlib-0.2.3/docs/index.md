# pptxlib

A Python library for automating Microsoft PowerPoint operations.

## Overview

pptxlib is a high-level Python library that provides a simple and intuitive interface
for automating Microsoft PowerPoint operations. It allows you to create, modify, and
manage PowerPoint presentations programmatically.

## Features

- Create and manage PowerPoint presentations
- Add and modify slides
- Work with shapes, tables, and charts
- Customize text, colors, and formatting
- Automate presentation generation
- Support for Windows platforms

## Quick Start

```python
from pptxlib import App

app = App()
presentation = app.presentations.add()
slide = presentation.slides.add()
shape = slide.shapes.add("Rectangle", 100, 100, 200, 100)
```

## Installation

```bash
pip install pptxlib
```

## Requirements

- Windows operating system
- Microsoft PowerPoint
- Python 3.11 or higher
