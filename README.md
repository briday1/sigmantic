# Sigmantic

Signal processing and algorithm visualization toolkit.

## Modules

### algorithm_image

A module for generating visual representations of algorithm flows from JSON descriptions.

**Features:**
- Generate algorithm flow diagrams as PNG images
- JSON-based flow description format
- Support for input, process, and output node types
- Automatic layout and positioning
- Customizable dimensions and colors

**Quick Start:**
```python
from algorithm_image import AlgorithmImageGenerator
import json

# Load algorithm flow description
with open('algorithm_image/example_flow.json', 'r') as f:
    flow = json.load(f)

# Generate image
generator = AlgorithmImageGenerator()
img = generator.from_dict(flow)
generator.save(img, 'output.png')
```

See [algorithm_image/README.md](algorithm_image/README.md) for detailed documentation.

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.6+
- numpy
- scipy
- sympy
- matplotlib
- plantuml
- Pillow (for algorithm_image module)
