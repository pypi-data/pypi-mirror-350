from setuptools import setup, find_packages


setup(
    name="geo",
    version="1.0.0",
    author="Minh-Chien Trinh",
    author_email="mctrinh@jbnu.ac.kr",
    description="A Python package for computational geometry.",
    url="https://github.com/mctrinh/geo",
    license="MIT",
    python_requires = ">=3.9",
    packages=find_packages(),
    keywords="geometry, geo",
    install_requires = [],
    extras_require={
        "full": ["shapely", "trimesh", "scipy", "matplotlib"],
        "dev": ["pytest", "sphinx", "furo", "black", "mypy"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)