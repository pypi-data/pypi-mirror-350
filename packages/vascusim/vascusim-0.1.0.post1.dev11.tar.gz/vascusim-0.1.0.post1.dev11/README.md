# VascuSim

[![PyPI Version](https://img.shields.io/pypi/v/vascusim.svg)](https://pypi.org/project/vascusim/)
[![Python Versions](https://img.shields.io/pypi/pyversions/vascusim.svg)](https://pypi.org/project/vascusim/)
[![Documentation Status](https://readthedocs.org/projects/vascusim/badge/?version=latest)](https://vascusim.readthedocs.io/en/latest/?badge=latest)
[![Tests](https://github.com/BioSiMMLab/vascusim/workflows/Tests/badge.svg)](https://github.com/BioSiMMLab/vascusim/actions?query=workflow%3ATests)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/WenzhuoXu/vascusim.svg)](LICENSE)

A Python package for working with cardiovascular simulation datasets from the BioSiMMLab.

## Overview

VascuSim provides tools for processing, streaming, and analyzing vascular simulation data stored in VTU/VTP format, with efficient conversion to PyTorch Geometric data formats for graph neural network training.

Key features:
- Loading and conversion of VTU/VTP files to PyTorch Geometric data format
- Streaming functionality for efficient access to large datasets
- Support for various data sources (local files, NAS, Hugging Face)
- Comprehensive geometric processing utilities
- Visualization tools for vascular structures
- Domain decomposition for distributed processing

📚 **[Documentation](https://vascusim.readthedocs.io/en/latest/)** | 📦 **[PyPI Package](https://pypi.org/project/vascusim/)** | 🐛 **[Issue Tracker](https://github.com/BioSiMMLab/vascusim/issues)**

## Installation

### Basic Installation

```bash
pip install vascusim
```

### Development Installation

```bash
git clone https://github.com/BioSiMMLab/vascusim.git
cd vascusim
pip install -e ".[dev]"
```

### Optional Dependencies

For SMB/CIFS support (for NAS streaming):
```bash
pip install "vascusim[smb]"
```

For documentation building:
```bash
pip install "vascusim[docs]"
```

## Usage Examples

### Loading Vascular Data

```python
import torch
from vascusim.data.conversion import vtu_to_pyg

# Convert a VTU file to PyTorch Geometric format
data = vtu_to_pyg("path/to/simulation.vtu")

# Access node positions and connectivity
pos = data.pos
edge_index = data.edge_index

# Access node attributes
velocity = data.node_velocity  # if available in the VTU file
pressure = data.node_pressure  # if available in the VTU file
```

### Using the Dataset API

```python
from vascusim.data.dataset import VascuDataset

# Create a dataset from a local directory
dataset = VascuDataset(
    source_url="path/to/data",
    cache_dir="~/.vascusim/cache",
    normalize=True
)

# Access an item
data = dataset[0]

# Use with PyTorch DataLoader
from torch_geometric.loader import DataLoader
loader = DataLoader(dataset, batch_size=4, shuffle=True)
```

### Streaming from Remote Sources

```python
from vascusim.data.dataset import StreamingVascuDataset

# Stream from Hugging Face dataset
hf_dataset = StreamingVascuDataset(
    source_url="huggingface.co/datasets/biosimmlab/vascu-example",
    streaming_type="hf",
    prefetch=True
)

# Stream from NAS
nas_dataset = StreamingVascuDataset(
    source_url="192.168.1.100",
    streaming_type="nas",
    username="user",
    password="pass"
)
```

### Visualization

```python
import matplotlib.pyplot as plt
from vascusim.utils.visualization import plot_geometry, plot_flow

# Plot geometry
fig = plot_geometry(data, show_points=True)
plt.savefig("geometry.png")

# Visualize flow fields
plot_flow(data, flow_field="velocity", color_by_magnitude=True)
```

### Processing Vascular Geometry

```python
from vascusim.processing.geometry import compute_curvature, extract_centerline

# Compute curvature for each node
curvature = compute_curvature(data)

# Extract centerline
centerline = extract_centerline(data, smoothing=0.1)

# Apply transformations
from vascusim.data.transforms import Normalize, AddNoise

transform = Normalize()
normalized_data = transform(data)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run the tests (`python run_test.py`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citing

If you use VascuSim in your research, please cite:

```bibtex
@software{vascusim2025,
  author = {Xu, Wenzhuo},
  title = {VascuSim: Dataset package for cardiovascular simulations},
  url = {https://github.com/biosimmlab/vascusim},
  year = {2025}
}
```

## Acknowledgements

This project is maintained by the [BioSiMMLab](https://www.meche.engineering.cmu.edu/faculty/gutierrez-biosimm-lab.html).