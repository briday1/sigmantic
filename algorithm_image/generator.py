"""Algorithm Image Generator

Generates visual representations of algorithm flows from JSON descriptions.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import io


class AlgorithmImageGenerator:
    """Generates algorithm flow diagrams as images from JSON descriptions."""
    
    # Default image dimensions matching the reference og.png
    DEFAULT_WIDTH = 2400
    DEFAULT_HEIGHT = 1260
    
    # Default color scheme (warm beige background like reference)
    DEFAULT_BG_COLOR = (254, 243, 192)
    DEFAULT_TEXT_COLOR = (40, 40, 40)
    DEFAULT_BOX_COLOR = (255, 255, 255)
    DEFAULT_BORDER_COLOR = (100, 100, 100)
    DEFAULT_ARROW_COLOR = (60, 60, 60)
    
    # Layout constants
    MARGIN = 100
    BOX_WIDTH = 300
    BOX_HEIGHT = 120
    BOX_SPACING = 150
    ARROW_WIDTH = 3
    
    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        bg_color: Tuple[int, int, int] = DEFAULT_BG_COLOR
    ):
        """Initialize the generator.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            bg_color: Background color as RGB tuple
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
        
    def from_json(self, json_data: str) -> Image.Image:
        """Generate image from JSON string.
        
        Args:
            json_data: JSON string containing algorithm flow description
            
        Returns:
            PIL Image object
        """
        flow_dict = json.loads(json_data)
        return self.from_dict(flow_dict)
    
    def from_dict(self, flow_dict: Dict[str, Any]) -> Image.Image:
        """Generate image from dictionary.
        
        Args:
            flow_dict: Dictionary containing algorithm flow description
            
        Expected format:
        {
            "title": "Algorithm Name",
            "nodes": [
                {
                    "id": "node1",
                    "label": "Step 1",
                    "type": "input|process|output",
                    "annotations": ["annotation1", "annotation2"]
                }
            ],
            "edges": [
                {
                    "from": "node1",
                    "to": "node2",
                    "label": "optional label"
                }
            ]
        }
        
        Returns:
            PIL Image object
        """
        # Create base image
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Get flow components
        title = flow_dict.get('title', 'Algorithm Flow')
        nodes = flow_dict.get('nodes', [])
        edges = flow_dict.get('edges', [])
        
        # Try to load a font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            annotation_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except (OSError, IOError):
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            annotation_font = ImageFont.load_default()
        
        # Draw title
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        draw.text((title_x, 60), title, fill=self.DEFAULT_TEXT_COLOR, font=title_font)
        
        # Calculate node positions
        node_positions = self._calculate_node_positions(nodes)
        
        # Draw edges first (so they appear behind nodes)
        self._draw_edges(draw, edges, node_positions)
        
        # Draw nodes
        self._draw_nodes(draw, nodes, node_positions, label_font, annotation_font)
        
        return img
    
    def _calculate_node_positions(self, nodes: List[Dict]) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for all nodes.
        
        Args:
            nodes: List of node dictionaries
            
        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        positions = {}
        
        if not nodes:
            return positions
        
        # Simple layout: arrange nodes in rows
        # Group nodes by type for better organization
        input_nodes = [n for n in nodes if n.get('type') == 'input']
        process_nodes = [n for n in nodes if n.get('type') == 'process']
        output_nodes = [n for n in nodes if n.get('type') == 'output']
        other_nodes = [n for n in nodes if n.get('type') not in ['input', 'process', 'output']]
        
        # Arrange in vertical flow
        all_node_groups = [input_nodes, process_nodes, output_nodes, other_nodes]
        all_node_groups = [g for g in all_node_groups if g]  # Remove empty groups
        
        y_start = 250
        
        for group_idx, group in enumerate(all_node_groups):
            y = y_start + group_idx * (self.BOX_HEIGHT + self.BOX_SPACING)
            
            # Center the group horizontally
            if len(group) == 0:
                continue
            total_width = len(group) * self.BOX_WIDTH + (len(group) - 1) * self.BOX_SPACING
            x_start = (self.width - total_width) // 2
            
            for node_idx, node in enumerate(group):
                x = x_start + node_idx * (self.BOX_WIDTH + self.BOX_SPACING)
                positions[node['id']] = (x, y)
        
        return positions
    
    def _draw_nodes(
        self,
        draw: ImageDraw.ImageDraw,
        nodes: List[Dict],
        positions: Dict[str, Tuple[int, int]],
        label_font: ImageFont.FreeTypeFont,
        annotation_font: ImageFont.FreeTypeFont
    ):
        """Draw all nodes on the image.
        
        Args:
            draw: ImageDraw object
            nodes: List of node dictionaries
            positions: Node positions
            label_font: Font for node labels
            annotation_font: Font for annotations
        """
        for node in nodes:
            node_id = node['id']
            if node_id not in positions:
                continue
                
            x, y = positions[node_id]
            label = node.get('label', node_id)
            node_type = node.get('type', 'process')
            annotations = node.get('annotations', [])
            
            # Determine colors based on node type
            if node_type == 'input':
                box_color = (220, 240, 255)  # Light blue
            elif node_type == 'output':
                box_color = (220, 255, 220)  # Light green
            else:
                box_color = self.DEFAULT_BOX_COLOR
            
            # Draw box
            draw.rectangle(
                [x, y, x + self.BOX_WIDTH, y + self.BOX_HEIGHT],
                fill=box_color,
                outline=self.DEFAULT_BORDER_COLOR,
                width=2
            )
            
            # Draw label (centered in box)
            label_bbox = draw.textbbox((0, 0), label, font=label_font)
            label_width = label_bbox[2] - label_bbox[0]
            label_height = label_bbox[3] - label_bbox[1]
            label_x = x + (self.BOX_WIDTH - label_width) // 2
            label_y = y + (self.BOX_HEIGHT - label_height) // 2
            draw.text((label_x, label_y), label, fill=self.DEFAULT_TEXT_COLOR, font=label_font)
            
            # Draw annotations below the box
            if annotations:
                annotation_y = y + self.BOX_HEIGHT + 10
                for annotation in annotations:
                    annotation_bbox = draw.textbbox((0, 0), annotation, font=annotation_font)
                    annotation_width = annotation_bbox[2] - annotation_bbox[0]
                    annotation_x = x + (self.BOX_WIDTH - annotation_width) // 2
                    draw.text(
                        (annotation_x, annotation_y),
                        annotation,
                        fill=(100, 100, 100),
                        font=annotation_font
                    )
                    annotation_y += 30
    
    def _draw_edges(
        self,
        draw: ImageDraw.ImageDraw,
        edges: List[Dict],
        positions: Dict[str, Tuple[int, int]]
    ):
        """Draw edges (arrows) between nodes.
        
        Args:
            draw: ImageDraw object
            edges: List of edge dictionaries
            positions: Node positions
        """
        for edge in edges:
            from_id = edge.get('from')
            to_id = edge.get('to')
            
            if from_id not in positions or to_id not in positions:
                continue
            
            from_x, from_y = positions[from_id]
            to_x, to_y = positions[to_id]
            
            # Calculate start and end points (bottom center of from node, top center of to node)
            start_x = from_x + self.BOX_WIDTH // 2
            start_y = from_y + self.BOX_HEIGHT
            end_x = to_x + self.BOX_WIDTH // 2
            end_y = to_y
            
            # Draw line
            draw.line(
                [(start_x, start_y), (end_x, end_y)],
                fill=self.DEFAULT_ARROW_COLOR,
                width=self.ARROW_WIDTH
            )
            
            # Draw arrow head
            arrow_size = 15
            self._draw_arrow_head(draw, end_x, end_y, arrow_size)
    
    def _draw_arrow_head(self, draw: ImageDraw.ImageDraw, x: int, y: int, size: int):
        """Draw an arrow head pointing down.
        
        Args:
            draw: ImageDraw object
            x: X coordinate of arrow tip
            y: Y coordinate of arrow tip
            size: Size of arrow head
        """
        points = [
            (x, y),
            (x - size // 2, y - size),
            (x + size // 2, y - size)
        ]
        draw.polygon(points, fill=self.DEFAULT_ARROW_COLOR)
    
    def save(self, img: Image.Image, filepath: str):
        """Save image to file.
        
        Args:
            img: PIL Image object
            filepath: Path to save the image
        """
        img.save(filepath, 'PNG')
    
    def generate_and_save(self, flow_dict: Dict[str, Any], filepath: str):
        """Generate image from dictionary and save to file.
        
        Args:
            flow_dict: Dictionary containing algorithm flow description
            filepath: Path to save the image
        """
        img = self.from_dict(flow_dict)
        self.save(img, filepath)
