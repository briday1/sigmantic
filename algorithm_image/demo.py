#!/usr/bin/env python3
"""Demo script for the algorithm image generator."""

import json
import os
from generator import AlgorithmImageGenerator


def main():
    """Generate example algorithm flow image."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load example flow
    example_json_path = os.path.join(script_dir, 'example_flow.json')
    with open(example_json_path, 'r') as f:
        flow_dict = json.load(f)
    
    # Create generator
    generator = AlgorithmImageGenerator()
    
    # Generate and save image
    output_path = os.path.join(script_dir, 'output_flow.png')
    generator.generate_and_save(flow_dict, output_path)
    
    print(f"Generated algorithm flow image: {output_path}")
    print(f"Image dimensions: {generator.width}x{generator.height}")


if __name__ == '__main__':
    main()
