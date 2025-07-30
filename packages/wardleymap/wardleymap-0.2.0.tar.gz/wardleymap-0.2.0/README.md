# WardleyMap

`WardleyMap` is a Python package designed for creating and visualizing Wardley Maps. Wardley Maps provide a visual representation of the strategic landscape and the positioning of components within it, facilitating better decision-making in business strategy and technology development.

## Features

- Parse and interpret Wardley Map syntax.
- Visualize maps using `matplotlib` for easy integration into Python workflows.
- Export maps to SVG format for embedding in web applications or documents.
- With a set of utilities to convert Wardley Map text into JSON, TOML, GRAPH and Cypher Text.

## Installation

Install `wardleymap` using pip:

```bash
pip install wardleymap
```

Ensure you have Python 3.6 or newer installed.

## Quick Start

To create and visualize a Wardley Map, follow these steps:

```python
from wardley_map.create_wardley_map import create_wardley_map_plot
from wardley_map.wardley_maps_utils import create_svg_map

# Define the structure of your Wardley Map using a string.
map_definition = """
title Business Value Chain
anchor Customer [0.95, 0.9]
component User Needs [0.8, 0.8]
component Website [0.6, 0.6]
component Hosting [0.3, 0.4]
User Needs -> Website
Website -> Hosting
"""

# Process the Wardley Map text and generate a plot of the map
wm, map_plot = create_wardley_map_plot(map_definition)

# Display the map in a Jupyter notebook
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))
plt.show()

# Or convert the map plot into an SVG
svg_map = create_svg_map(map_plot)

# Or save as an image file
map_plot.savefig("business_value_chain.png", dpi=300, bbox_inches='tight')
```

## Documentation

For detailed usage and API documentation, please refer to the `docs` directory.

## Contributing

Contributions to `WardleyMap` are welcome! Please read the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgements

- Special thanks to the open-source community for the invaluable tools and libraries.
- Inspired by Simon Wardley's work on mapping and strategy.

## Example Usage

Below is an example of how to use the `wardleymap` package to create and visualize a Wardley Map:

```python
from wardley_map.create_wardley_map import create_wardley_map_plot
from wardley_map.wardley_maps_utils import create_svg_map

# Define the structure of your Wardley Map using a string.
map_definition = """
title Business Value Chain
anchor Customer [0.95, 0.9]
component User Needs [0.8, 0.8]
component Website [0.6, 0.6]
component Hosting [0.3, 0.4]
User Needs -> Website
Website -> Hosting
"""

# Process the Wardley Map text and generate a plot of the map
wm, map_plot = create_wardley_map_plot(map_definition)

# Convert the map plot into an SVG
svg_map = create_svg_map(map_plot)
```

## Advanced Features

This package supports several advanced Wardley Map elements:

### Markets

Markets represent user needs or groups and are visualized with a distinctive symbol:

```python
map_definition = """
title Customer Segments
component Product [0.6, 0.5]
market Enterprise Customers [0.9, 0.7]
market SMB Customers [0.9, 0.3]
Product -> Enterprise Customers
Product -> SMB Customers
"""
```

### Inertia

Components with resistance to evolution can be marked with inertia:

```python
map_definition = """
title Legacy System Migration
component Legacy System [0.6, 0.3] inertia
component Cloud Platform [0.6, 0.7]
"""
```

### Pipelines

Visualize value chains or processes that span multiple evolution stages:

```python
map_definition = """
title Development Pipeline
component Software Development [0.7, 0.5]
pipeline Software Development [0.2, 0.8]
"""
```

### Complete Example

A more complex example showcasing multiple features:

```python
map_definition = """
title Digital Transformation Strategy
component Business Strategy [0.9, 0.2]
component Legacy Systems [0.5, 0.2] inertia
component Cloud Migration [0.6, 0.5]
component New Digital Services [0.7, 0.6]
market Enterprise Customers [0.9, 0.7]
market SMB Customers [0.9, 0.4]
component DevOps [0.4, 0.6]
pipeline DevOps [0.4, 0.8]
Business Strategy -> Legacy Systems
Business Strategy -> Cloud Migration
Cloud Migration -> New Digital Services
New Digital Services -> Enterprise Customers
New Digital Services -> SMB Customers
DevOps -> Cloud Migration
"""

wm, map_plot = create_wardley_map_plot(map_definition)
map_plot.savefig("digital_transformation_strategy.png", dpi=300, bbox_inches='tight')
```
