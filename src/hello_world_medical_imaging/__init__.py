"""Hello World Deep Learning in Medical Imaging, from notebook to bedside.

The tutorial by Lakhani et al. (Journal of Digital Imaging, 2018,
https://doi.org/10.1007/s10278-018-0079-6) trains a chest-versus-abdomen
radiograph classifier in a Jupyter notebook. This package holds the same
pipeline in small modules:

- :mod:`.config` reads the experiment configuration (paths, hyperparameters,
  random seed) from a TOML file;
- :mod:`.data` provides the data sources: the radiographs, and synthetic
  images;
- :mod:`.model` builds the transfer-learning classifier;
- :mod:`.training` trains a model on the datasets it is given;
- :mod:`.predict` classifies one image with a trained model;
- :mod:`.cli` wires everything together for the command line.
"""
