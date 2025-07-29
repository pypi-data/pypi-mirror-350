.. raw:: html

  <p>
  <a href="https://badge.fury.io/py/calorine"><img src="https://badge.fury.io/py/calorine.svg" alt="PyPI version" height="18"></a>
  <a href="https://doi.org/10.5281/zenodo.7919206"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.7919206.svg" alt="zenodo" height="18"></a>
  </p>

:program:`calorine`
*******************

:program:`calorine` is a Python library for constructing and sampling neuroevolution potential (NEP) models via the `GPUMD <https://gpumd.org/>`_ package.
It provides ASE calculators, IO functions for reading and writing :program:`GPUMD` input and output files, as well as a Python interface that allows inspection of NEP models.
Tutorials with common usage examples can be found under :ref:`Tutorials <tutorials>`, and a detailed function reference can be found under :ref:`Function reference <reference>`.

The following snippet illustrates how a :doc:`CPUNEP calculator <calculators>` instance can be created given a NEP potential file, and how it can be used to predict the potential energy, forces, and stress for a structure. ::

    from ase.io import read
    from ase.build import bulk
    from calorine.calculators import CPUNEP
    
    structure = bulk('PbTe', crystalstructure='rocksalt', a=6.7)
    calc = CPUNEP('nep-PbTe.txt')
    structure.calc = calc

    print('Energy (eV):', structure.get_potential_energy())
    print('Forces (eV/Å):\n', structure.get_forces())
    print('Stress (GPa):\n', structure.get_stress())

If you use :program:`calorine` in any of your publications, please follow the :doc:`citation instructions <credits>` for how to properly cite this work.

:program:`calorine` and its development are hosted on `gitlab <https://gitlab.com/materials-modeling/calorine>`_.

.. toctree::
   :maxdepth: 2
   :caption: Main

   installation
   credits

.. toctree::
   :name: tutorials
   :maxdepth: 2
   :caption: Tutorials

   tutorials/calculators
   tutorials/nep_descriptors
   tutorials/nep_model_inspection
   tutorials/visualize_descriptor_space_with_pca
   tutorials/generate_training_structures_and_training
   tutorials/structure_relaxation
   tutorials/phonons
   tutorials/elastic_stiffness_tensor
   tutorials/free_energy_tutorial
   tutorials/thermal_conductivity_from_bte

.. toctree::
   :name: reference
   :maxdepth: 2
   :caption: Function reference

   calculators
   gpumd
   nep
   tools

.. toctree::
   :maxdepth: 2
   :caption: Backmatter

   genindex
