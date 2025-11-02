#!/usr/bin/env python3
"""Validation script for the algorithm image generator."""

import json
import os
import sys
import tempfile
from generator import AlgorithmImageGenerator
from PIL import Image


def test_basic_generation():
    """Test basic image generation."""
    flow_dict = {
        "title": "Test Flow",
        "nodes": [
            {"id": "n1", "label": "Node 1", "type": "input"},
            {"id": "n2", "label": "Node 2", "type": "output"}
        ],
        "edges": [
            {"from": "n1", "to": "n2"}
        ]
    }
    
    generator = AlgorithmImageGenerator()
    img = generator.from_dict(flow_dict)
    
    assert img is not None, "Image generation failed"
    assert img.size == (2400, 1260), f"Unexpected image size: {img.size}"
    assert img.mode == 'RGB', f"Unexpected image mode: {img.mode}"
    
    print("✓ Basic generation test passed")


def test_json_loading():
    """Test loading from JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    example_json_path = os.path.join(script_dir, 'example_flow.json')
    
    with open(example_json_path, 'r') as f:
        flow_dict = json.load(f)
    
    generator = AlgorithmImageGenerator()
    img = generator.from_dict(flow_dict)
    
    assert img is not None, "Image generation from JSON failed"
    print("✓ JSON loading test passed")


def test_custom_dimensions():
    """Test custom image dimensions."""
    flow_dict = {
        "title": "Custom Size",
        "nodes": [{"id": "n1", "label": "Node", "type": "process"}],
        "edges": []
    }
    
    generator = AlgorithmImageGenerator(width=1920, height=1080, bg_color=(255, 255, 255))
    img = generator.from_dict(flow_dict)
    
    assert img.size == (1920, 1080), f"Custom dimensions not applied: {img.size}"
    print("✓ Custom dimensions test passed")


def test_node_types():
    """Test different node types."""
    flow_dict = {
        "title": "Node Types Test",
        "nodes": [
            {"id": "n1", "label": "Input", "type": "input"},
            {"id": "n2", "label": "Process", "type": "process"},
            {"id": "n3", "label": "Output", "type": "output"}
        ],
        "edges": [
            {"from": "n1", "to": "n2"},
            {"from": "n2", "to": "n3"}
        ]
    }
    
    generator = AlgorithmImageGenerator()
    img = generator.from_dict(flow_dict)
    
    assert img is not None, "Node types test failed"
    print("✓ Node types test passed")


def test_annotations():
    """Test node annotations."""
    flow_dict = {
        "title": "Annotations Test",
        "nodes": [
            {
                "id": "n1",
                "label": "Annotated Node",
                "type": "process",
                "annotations": ["Annotation 1", "Annotation 2"]
            }
        ],
        "edges": []
    }
    
    generator = AlgorithmImageGenerator()
    img = generator.from_dict(flow_dict)
    
    assert img is not None, "Annotations test failed"
    print("✓ Annotations test passed")


def test_save_functionality():
    """Test saving image to file."""
    flow_dict = {
        "title": "Save Test",
        "nodes": [{"id": "n1", "label": "Node", "type": "process"}],
        "edges": []
    }
    
    generator = AlgorithmImageGenerator()
    test_output = os.path.join(tempfile.gettempdir(), "test_output.png")
    
    generator.generate_and_save(flow_dict, test_output)
    
    assert os.path.exists(test_output), "Image file was not created"
    
    # Verify it's a valid image
    img = Image.open(test_output)
    assert img.size == (2400, 1260), "Saved image has incorrect dimensions"
    
    # Clean up
    os.remove(test_output)
    
    print("✓ Save functionality test passed")


def main():
    """Run all validation tests."""
    print("Running algorithm_image validation tests...\n")
    
    tests = [
        test_basic_generation,
        test_json_loading,
        test_custom_dimensions,
        test_node_types,
        test_annotations,
        test_save_functionality
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {len(tests) - failed}/{len(tests)} tests passed")
    
    if failed > 0:
        print(f"FAILED: {failed} test(s) failed")
        sys.exit(1)
    else:
        print("SUCCESS: All tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
