# Algorithm Image Generator

This module generates visual representations of algorithm flows from JSON descriptions.

## Features

- Generate algorithm flow diagrams from JSON descriptions
- Support for input, process, and output node types
- Automatic layout and positioning
- Customizable colors and dimensions
- Annotations support for additional information
- Arrow-based connections between nodes

## Usage

### Basic Example

```python
from algorithm_image import AlgorithmImageGenerator
import json

# Load flow description
with open('example_flow.json', 'r') as f:
    flow_dict = json.load(f)

# Create generator and generate image
generator = AlgorithmImageGenerator()
img = generator.from_dict(flow_dict)
generator.save(img, 'output.png')
```

### JSON Schema

The input JSON should follow this schema:

```json
{
  "title": "Algorithm Name",
  "nodes": [
    {
      "id": "unique_id",
      "label": "Display Label",
      "type": "input|process|output",
      "annotations": ["Optional", "Annotations"]
    }
  ],
  "edges": [
    {
      "from": "source_node_id",
      "to": "target_node_id",
      "label": "Optional edge label"
    }
  ]
}
```

### Node Types

- **input**: Light blue background, represents input data or signals
- **process**: White background, represents processing steps
- **output**: Light green background, represents output results

### Running the Demo

```bash
cd algorithm_image
python3 demo.py
```

This will generate `output_flow.png` based on `example_flow.json`.

## Customization

You can customize the image dimensions and background color:

```python
generator = AlgorithmImageGenerator(
    width=1920,
    height=1080,
    bg_color=(255, 255, 255)  # White background
)
```

## Dependencies

- PIL/Pillow: For image generation and manipulation
- Python 3.6+

## Example Output

The module generates images similar to the reference Open Graph image style with:
- 2400x1260 pixel resolution (default)
- Warm beige background color
- Clean, professional appearance
- Clear node and edge visualization
