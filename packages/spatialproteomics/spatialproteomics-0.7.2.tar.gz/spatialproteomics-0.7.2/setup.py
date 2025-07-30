# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spatialproteomics',
 'spatialproteomics.image_container',
 'spatialproteomics.la',
 'spatialproteomics.nh',
 'spatialproteomics.pl',
 'spatialproteomics.pp',
 'spatialproteomics.sd',
 'spatialproteomics.tl']

package_data = \
{'': ['*']}

install_requires = \
['cffi>=1.15.0,<2.0.0',
 'matplotlib>=3.8.0,<4.0.0',
 'numpy>=1.23',
 'opencv-python>=4.11.0,<5.0.0',
 'pyyaml>=6.0,<7.0',
 'scikit-image>=0.25',
 'scikit-learn>=1.4.2,<2.0.0',
 'tqdm>=4.64.0',
 'xarray>=2024.0.0,<2025.0.0',
 'zarr<3.0.0']

extras_require = \
{'all': ['spatialdata>=0.4.0,<0.5.0',
         'cellpose>=3.1.0',
         'stardist>=0.9.1,<0.10.0'],
 'cellpose': ['cellpose>=3.1.0'],
 'dev': ['pytest>=7.1.2,<8.0.0'],
 'docs': ['Sphinx>=7.0.0,<8.0.0',
          'sphinxcontrib-napoleon==0.7',
          'nbsphinx==0.8.9',
          'sphinx-book-theme>=0.0.39,<0.0.40',
          'sphinx-multiversion>=0.2.4,<0.3.0',
          'IPython>=8.0.0,<9.0.0'],
 'spatialdata': ['spatialdata>=0.4.0,<0.5.0'],
 'stardist': ['stardist>=0.9.1,<0.10.0']}

setup_kwargs = {
    'name': 'spatialproteomics',
    'version': '0.7.2',
    'description': 'spatialproteomics provides tools for the analysis of highly multiplexed immunofluorescence data',
    'long_description': '# spatialproteomics\n\n[![PyPI version](https://badge.fury.io/py/spatialproteomics.svg)](https://badge.fury.io/py/spatialproteomics)\n\n`Spatialproteomics` is an interoperable toolbox for analyzing highly multiplexed fluorescence image data. This analysis involves a sequence of steps, including segmentation, image processing, marker quantification, cell type classification, and neighborhood analysis. \n\n<p align="center" width="100%">\n    <img src="docs/_static/img/figure_1.png" alt="Spatialproteomics orchestrates analysis workflows for highly multiplexed fluorescence images." style="width:70%;">\n</p>\n\n## Principles\n\nMultiplexed imaging data comprises at least 3 dimensions (i.e. `channels`, `x`, and `y`) and has often additional data such as segmentation masks or cell type annotations associated with it. In `spatialproteomics`, we use `xarray` to create a data structure that keeps all of these data dimension in sync. This data structure can then be used to apply all sorts of operations to the data. Users can segment cells, perform different image processing steps, quantify protein expression, predict cell types, and plot their data in various ways. By providing researchers with those tools, `spatialproteomics` can be used to quickly explore highly multiplexed spatial proteomics data directly within jupyter notebooks.\n\n<p align="center" width="100%">\n    <img src="docs/_static/img/supplementary_figure_1.png" alt="The spatialproteomics data structure enables synchronized subsetting across shared dimensions." style="width:70%;">\n</p>\n\n## Getting Started\n\nPlease refer to the [documentation](https://sagar87.github.io/spatialproteomics) for details on the API and tutorials.\n\n## Installation\n\nTo install `spatialproteomics`, first create a python environment and install the package using \n\n```\npip install spatialproteomics\n```\n\n## Citation\nSpatialproteomics - an interoperable toolbox for analyzing highly multiplexed fluorescence image data\n\nMatthias Fabian Meyer-Bender, Harald Sager Voehringer, Christina Schniederjohann, Sarah Patricia Koziel, Erin Kim Chung, Ekaterina Popova, Alexander Brobeil, Lisa-Maria Held, Aamir Munir, Scverse Community, Sascha Dietrich, Peter-Martin Bruch, Wolfgang Huber\n\nbioRxiv 2025.04.29.651202; doi: https://doi.org/10.1101/2025.04.29.651202\n',
    'author': 'Matthias Meyer-Bender',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
