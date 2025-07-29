<h1 align="center">
  <img src="https://raw.githubusercontent.com/mctrinh/geo/refs/heads/main/asset/geologo.svg" width="300"> 
</h1><br>

[![PyPI Downloads](https://img.shields.io/pypi/dm/geo)](https://pypi.org/project/geo/)

A Python package for computational geometry.

# Download
`geo` can be downloaded from [PyPi](https://pypi.org/project/geo/) using the following command.

```pip install geo```

# Project tree

```
geo/
│
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── point.py
│   ├── precision.py
│   ├── transform.py
│   └── vector.py
│
├── primitives_2d/
│   ├── __init__.py
│   ├── circle.py
│   ├── ellipse.py
│   ├── line.py
│   ├── polygon.py
│   ├── rectangle.py
│   ├── triangle.py
│   └── curve/
│       ├── __init__.py
│       ├── base.py
│       ├── bezier.py
│       └── spline.py
│
├── primitives_3d/
│   ├── __init__.py
│   ├── cone.py
│   ├── cube.py
│   ├── cylinder.py
│   ├── line_3d.py
│   ├── plane.py
│   ├── polyhedra.py
│   └── sphere.py
│
├── operations/
│   ├── __init__.py
│   ├── boolean_ops.py
│   ├── containment.py
│   ├── convex_hull.py
│   ├── intersections_2d.py
│   ├── intersections_3d.py
│   ├── measurements.py
│   └── triangulation.py
│
└── utils/
    ├── __init__.py
    ├── io.py
    └── validators.py
```

# Call for Contributions
The `geo` project welcomes your expertise and enthusiasm.