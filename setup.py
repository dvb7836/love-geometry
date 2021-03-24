import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('love_geometry_danil_buiko_v1.egg-info/requires.txt') as f:
    install_requires = f.read().strip().split('\n')

setuptools.setup(
    name="love-geometry-danil-buiko-v1",
    version="1",
    author="Danil Buiko",
    author_email="dvb7836@gmail.com",
    description="Love Geometry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires='>=3.9',
    options={"bdist_wheel": {"universal": True}}
)
