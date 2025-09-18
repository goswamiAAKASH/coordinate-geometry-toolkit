# Coordinate Geometry Toolkit

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive **Coordinate Geometry Toolkit** built using **Object-Oriented Programming (OOP) in Python**. This project provides a complete suite of geometric classes and methods for 2D coordinate geometry, including interactive visualization through a modern Streamlit web application.

## Features

### Core Geometry Classes
- **Point**: Distance calculations, midpoint, slope, reflections, translations, quadrant detection
- **Line**: Slope, equation, length, parallel/perpendicular checks, intersections, angles
- **Circle**: Area, perimeter, diameter, point-on-circle detection, chord equations
- **Triangle**: Area, perimeter, centroid, triangle type classification, angle calculations
- **Rectangle & Square**: Area, perimeter, diagonal length, point containment
- **Polygon**: Area, perimeter, centroid, point containment for n-sided polygons
- **Vector**: Magnitude, dot/cross products, angles, projections, transformations

### Conic Sections
- **Parabola**: Focus, directrix, latus rectum, vertex form, point verification
- **Ellipse**: Eccentricity, foci, vertices, major/minor axes, area calculations
- **Hyperbola**: Asymptotes, foci, vertices, transverse/conjugate axes

### Interactive Web Application
- **Modern UI**: Clean, responsive design with dark theme
- **Real-time Visualization**: Interactive plotting with matplotlib
- **Method Explorer**: Dynamic method calling with parameter inputs
- **Export Features**: PDF reports, CSV data, PNG images
- **Educational Tools**: Built-in help and examples

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/goswamiAAKASH/coordinate-geometry-toolkit.git
cd coordinate-geometry-toolkit

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Web Application

```bash
# Start the Streamlit web app
streamlit run coordinate_geometry_toolkit/web_app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
coordinate-geometry-toolkit/
├── README.md
├── requirements.txt
├── .gitignore
│
└── coordinate_geometry_toolkit/
    ├── __init__.py              # Package initialization
    ├── base.py                  # Abstract Shape base class
    ├── point.py                 # Point class with all methods
    ├── line.py                  # Line class with geometry operations
    ├── circle.py                # Circle class with calculations
    ├── triangle.py              # Triangle class with properties
    ├── rectangle.py             # Rectangle class
    ├── square.py                # Square class
    ├── polygon.py               # Polygon class for n-sided shapes
    ├── vector.py                # Vector class with operations
    ├── ellipse.py               # Ellipse conic section
    ├── parabola.py              # Parabola conic section
    ├── hyperbola.py             # Hyperbola conic section
    ├── main.py                  # Command-line interface
    └── web_app.py               # Streamlit web application
```

## Usage Examples

### Basic Geometry Operations

```python
from coordinate_geometry_toolkit.point import Point
from coordinate_geometry_toolkit.line import Line
from coordinate_geometry_toolkit.circle import Circle
from coordinate_geometry_toolkit.triangle import Triangle

# Create points
p1 = Point(0, 0)
p2 = Point(3, 4)
p3 = Point(0, 4)

# Calculate distance
distance = p1.distance_between_points(p2)
print(f"Distance: {distance}")  # Output: 5.0

# Create a line
line = Line(p1, p2)
print(f"Line equation: {line.equation()}")  # Output: y=1.33x +0.00

# Create a circle
circle = Circle(p1, 5)
print(f"Circle area: {circle.area()}")  # Output: 78.54

# Create a triangle
triangle = Triangle(p1, p2, p3)
print(f"Triangle type: {triangle.type_of_triangle()}")  # Output: Scalene Triangle
```

### Advanced Operations

```python
# Vector operations
from coordinate_geometry_toolkit.vector import Vector

v1 = Vector(3, 4)
v2 = Vector(1, 2)

# Dot product
dot_product = v1.dot(v2)
print(f"Dot product: {dot_product}")

# Angle between vectors
angle = v1.angle_with(v2)
print(f"Angle: {angle} degrees")

# Conic sections
from coordinate_geometry_toolkit.ellipse import Ellipse

ellipse = Ellipse(Point(0, 0), 3, 2)
print(f"Ellipse eccentricity: {ellipse.eccentricity()}")
```

## Web Application Features

### Interactive Shape Creation
- Create points, lines, circles, triangles, and more
- Real-time parameter input with validation
- Automatic shape naming and color assignment

### Method Explorer
- Dynamic method calling for any created shape
- Parameter input forms for complex methods
- Results automatically added to the visualization

### Export Capabilities
- **PDF Reports**: Professional geometry reports with visualizations
- **CSV Data**: Shape data in spreadsheet format
- **PNG Images**: High-quality plot exports

### Educational Tools
- Built-in help and examples
- Step-by-step problem solving guides
- Interactive learning environment

## Testing

The project includes comprehensive testing to ensure all functionality works correctly:

```bash
# All tests pass - verified functionality
- Point class: Distance, midpoint, reflections, transformations
- Line class: Slope, equations, parallel/perpendicular checks
- Circle class: Area, perimeter, point detection
- Triangle class: Area, perimeter, centroid, type classification
- Vector class: Magnitude, dot/cross products, angles
- Conic sections: Parabola, ellipse, hyperbola calculations
- Web application: All imports and object creation
```

## Requirements

- **Python**: 3.8 or higher
- **Streamlit**: 1.28.0+
- **Matplotlib**: 3.7.0+
- **NumPy**: 1.24.0+
- **ReportLab**: 4.0.0+

## Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click

### Local Network Sharing
```bash
streamlit run coordinate_geometry_toolkit/web_app.py --server.address 0.0.0.0
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Educational Use

This toolkit is perfect for:
- **Students**: Learning coordinate geometry concepts
- **Teachers**: Creating interactive geometry lessons
- **Developers**: Understanding OOP principles in Python
- **Researchers**: Prototyping geometric algorithms

## Future Enhancements

- [ ] 3D geometry support
- [ ] Advanced conic section analysis
- [ ] Geometric transformations (rotation, scaling, shearing)
- [ ] Collision detection algorithms
- [ ] Bezier curves and splines
- [ ] Fractal geometry support
- [ ] Mobile app version
- [ ] API endpoints for programmatic access

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Aakash Goswami**
- GitHub: [@goswamiAAKASH](https://github.com/goswamiAAKASH)
- Project: [Coordinate Geometry Toolkit](https://github.com/goswamiAAKASH/coordinate-geometry-toolkit)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io) for the web interface
- Visualization powered by [Matplotlib](https://matplotlib.org)
- Mathematical computations using [NumPy](https://numpy.org)
- PDF generation with [ReportLab](https://reportlab.com)

---

**Star this repository if you find it helpful!**
