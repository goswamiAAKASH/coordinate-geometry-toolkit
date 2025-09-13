# coordinate-geometry-toolkit (OOP in Python)

A complete **Coordinate Geometry Toolkit** built using **Object-Oriented Programming (OOP) in Python**.  
This project implements classes and methods for 2D geometry concepts like **Point, Line, Circle, Triangle, and Conic Sections** (Parabola, Ellipse, Hyperbola).

---

## Features
- **Point Class**: distance, midpoint, slope.
- **Line Class**: slope, equation, intercepts, parallel/perpendicular checks.
- **Circle Class**: radius, diameter, area, circumference, equation, point check.
- **Triangle Class**: area, perimeter, centroid, type check.
- **Parabola, Ellipse, Hyperbola Classes**: equations, latus rectum, eccentricity.
- **Visualization**: `matplotlib` support for plotting shapes.
- **Precision Handling** with `math.isclose()` and rounding.

---

## Project Structure
```
coordinate-geometry-toolkit/
├── .gitignore
├── README.md
├── requirements.txt
│
├── coordinate_geometry_toolkit/
│   ├── __init__.py
│   ├── base.py
│   ├── circle.py
│   ├── ellipse.py
│   ├── hyperbola.py
│   ├── line.py
│   ├── main.py
│   ├── parabola.py
│   ├── point.py
│   ├── polygon.py
│   ├── rectangle.py
│   ├── square.py
│   ├── triangle.py
│   ├── vector.py
│   └── web_app.py

```


---

## Installation
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/geometry-toolkit.git
cd geometry-toolkit

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

```
## Future Enhancements

This project is a work in progress. Future updates may include:

- Additional geometric shapes and conic sections
- More advanced computational methods for geometry
- Interactive visualizations and GUI improvements
- Enhanced Streamlit app features for educational purposes
- Utility functions and helper classes for faster computations

Contributions and suggestions are always welcome to make this toolkit more comprehensive and user-friendly.
