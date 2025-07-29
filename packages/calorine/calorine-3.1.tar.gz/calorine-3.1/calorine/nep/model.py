from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Tuple

import numpy as np


def _get_model_type(first_row: List[str]) -> str:
    """Parses a the first row of a ``nep.txt`` file,
    and returns the type of NEP model. Available types
    are ``potential``, ``dipole`` and ``polarizability``.

    Parameters
    ----------
    first_row
        first row of a NEP file, split by white space.
    """
    model_type = first_row[0]
    if 'dipole' in model_type:
        return 'dipole'
    elif 'polarizability' in model_type:
        return 'polarizability'
    return 'potential'


def _get_nep_contents(filename: str) -> Tuple[Dict, List]:
    """Parses a ``nep.txt`` file, and returns a dict describing the header
    and an unformatted list of all model parameters.
    Intended to be used by the :func:`read_model <calorine.nep.read_model>` function.

    Parameters
    ----------
    filename
        input file name
    """
    # parse file and split header and parameters
    header = []
    parameters = []
    nheader = 5  # 5 rows for NEP2, 6-7 rows for NEP3 onwards
    base_line = 3
    with open(filename) as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            assert len(flds) != 0, f'Empty line number {k}'
            if k == 0 and 'zbl' in flds[0]:
                base_line += 1
                nheader += 1
            if k == base_line and 'basis_size' in flds[0]:
                # Introduced in nep.txt after GPUMD v3.2
                nheader += 1
            if k < nheader:
                header.append(tuple(flds))
            elif len(flds) == 1:
                parameters.append(float(flds[0]))
            else:
                raise IOError(f'Failed to parse line {k} from {filename}')
    # compile data from the header into a dict
    data = {}
    for flds in header:
        if flds[0] in ['cutoff', 'zbl']:
            data[flds[0]] = tuple(map(float, flds[1:]))
        elif flds[0] in ['n_max', 'l_max', 'ANN', 'basis_size']:
            data[flds[0]] = tuple(map(int, flds[1:]))
        elif flds[0].startswith('nep'):
            version = flds[0].replace('nep', '').split('_')[0]
            version = int(version)
            data['version'] = version
            data['types'] = flds[2:]
            data['model_type'] = _get_model_type(flds)
        else:
            raise ValueError(f'Unknown field: {flds[0]}')
    return data, parameters


@dataclass
class Model:
    r"""Objects of this class represent a NEP model in a form suitable for
    inspection and manipulation. Typically a :class:`Model` object is instantiated
    by calling the :func:`read_model <calorine.nep.read_model>` function.

    Attributes
    ----------
    version : int
        NEP version.
    model_type: str
        One of ``potential``, ``dipole`` or ``polarizability``.
    types : Tuple[str, ...]
        Chemical species that this model represents.
    radial_cutoff : float
        The radial cutoff parameter in Å.
    angular_cutoff : float
        The angular cutoff parameter in Å.
    max_neighbors_radial : int
        Maximum number of neighbors in neighbor list for radial terms.
    max_neighbors_angular : int
        Maximum number of neighbors in neighbor list for angular terms.
    radial_typewise_cutoff_factor : float
        The radial cutoff factor if use_typewise_cutoff is used.
    angular_typewise_cutoff_factor : float
        The angular cutoff factor if use_typewise_cutoff is used.
    zbl : Tuple[float, float]
        Inner and outer cutoff for transition to ZBL potential.
    zbl_typewise_cutoff_factor : float
        Typewise cutoff when use_typewise_cutoff_zbl is used.
    n_basis_radial : int
        Number of radial basis functions :math:`n_\mathrm{basis}^\mathrm{R}`.
    n_basis_angular : int
        Number of angular basis functions :math:`n_\mathrm{basis}^\mathrm{A}`.
    n_max_radial : int
        Maximum order of Chebyshev polymonials included in
        radial expansion :math:`n_\mathrm{max}^\mathrm{R}`.
    n_max_angular : int
        Maximum order of Chebyshev polymonials included in
        angular expansion :math:`n_\mathrm{max}^\mathrm{A}`.
    l_max_3b : int
        Maximum expansion order for three-body terms :math:`l_\mathrm{max}^\mathrm{3b}`.
    l_max_4b : int
        Maximum expansion order for four-body terms :math:`l_\mathrm{max}^\mathrm{4b}`.
    l_max_5b : int
        Maximum expansion order for five-body terms :math:`l_\mathrm{max}^\mathrm{5b}`.
    n_descriptor_radial : int
        Dimension of radial part of descriptor.
    n_descriptor_angular : int
        Dimension of angular part of descriptor.
    n_neuron : int
        Number of neurons in hidden layer.
    n_parameters : int
        Total number of parameters including scalers (which are not fit parameters).
    n_descriptor_parameters : int
        Number of parameters in descriptor.
    n_ann_parameters : int
        Number of neural network weights.
    ann_parameters : Dict[Tuple[str, Dict[str, np.darray]]]
        Neural network weights.
    q_scaler : List[float]
        Scaling parameters.
    radial_descriptor_weights : Dict[Tuple[str, str], np.ndarray]
        Radial descriptor weights by combination of species; the array for each combination
        has dimensions of
        :math:`(n_\mathrm{max}^\mathrm{R}+1) \times (n_\mathrm{basis}^\mathrm{R}+1)`.
    angular_descriptor_weights : Dict[Tuple[str, str], np.ndarray]
        Angular descriptor weights by combination of species; the array for each combination
        has dimensions of
        :math:`(n_\mathrm{max}^\mathrm{A}+1) \times (n_\mathrm{basis}^\mathrm{A}+1)`.
    """

    version: int
    model_type: str
    types: Tuple[str, ...]

    radial_cutoff: float
    angular_cutoff: float

    n_basis_radial: int
    n_basis_angular: int
    n_max_radial: int
    n_max_angular: int
    l_max_3b: int
    l_max_4b: int
    l_max_5b: int
    n_descriptor_radial: int
    n_descriptor_angular: int

    n_neuron: int
    n_parameters: int
    n_descriptor_parameters: int
    n_ann_parameters: int
    ann_parameters: Dict[str, Dict[str, np.ndarray]]
    q_scaler: List[float]
    radial_descriptor_weights: Dict[Tuple[str, str], np.ndarray]
    angular_descriptor_weights: Dict[Tuple[str, str], np.ndarray]

    zbl: Tuple[float, float] = None
    zbl_typewise_cutoff_factor: float = None
    max_neighbors_radial: int = None
    max_neighbors_angular: int = None
    radial_typewise_cutoff_factor: float = None
    angular_typewise_cutoff_factor: float = None

    _special_fields = [
        'ann_parameters',
        'q_scaler',
        'radial_descriptor_weights',
        'angular_descriptor_weights',
    ]

    def __str__(self) -> str:
        s = []
        for fld in self.__dataclass_fields__:
            if fld not in self._special_fields:
                s += [f'{fld:22} : {getattr(self, fld)}']
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += ['<table border="1" class="dataframe"']
        s += [
            '<thead><tr><th style="text-align: left;">Field</th><th>Value</th></tr></thead>'
        ]
        s += ['<tbody>']
        for fld in self.__dataclass_fields__:
            if fld not in self._special_fields:
                s += [
                    f'<tr><td style="text-align: left;">{fld:22}</td>'
                    f'<td>{getattr(self, fld)}</td><tr>'
                ]
        for fld in self._special_fields:
            d = getattr(self, fld)
            if fld.endswith('descriptor_weights'):
                dim = list(d.values())[0].shape
            if fld == 'ann_parameters' and self.version == 4:
                dim = (len(self.types), len(list(d.values())[0]))
            else:
                dim = len(d)
            s += [
                f'<tr><td style="text-align: left;">Dimension of {fld:22}</td><td>{dim}</td><tr>'
            ]
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)

    def write(self, filename: str) -> None:
        """Write NEP model to file in ``nep.txt`` format."""
        with open(filename, 'w') as f:
            # header
            version_name = f'nep{self.version}'
            if self.zbl is not None:
                version_name += '_zbl'
            elif self.model_type != 'potential':
                version_name += f'_{self.model_type}'
            f.write(f'{version_name} {len(self.types)} {" ".join(self.types)}\n')
            if self.zbl is not None:
                f.write(f'zbl {" ".join(map(str, self.zbl))}\n')
            f.write(f'cutoff {self.radial_cutoff} {self.angular_cutoff}')
            f.write(f' {self.max_neighbors_radial} {self.max_neighbors_angular}')
            if (
                self.radial_typewise_cutoff_factor is not None
                and self.angular_typewise_cutoff_factor is not None
            ):
                f.write(f' {self.radial_typewise_cutoff_factor}'
                        f' {self.angular_typewise_cutoff_factor}')
            if self.zbl_typewise_cutoff_factor:
                f.write(f' {self.zbl_typewise_cutoff_factor}')
            f.write('\n')
            f.write(f'n_max {self.n_max_radial} {self.n_max_angular}\n')
            f.write(f'basis_size {self.n_basis_radial} {self.n_basis_angular}\n')
            f.write(f'l_max {self.l_max_3b} {self.l_max_4b} {self.l_max_5b}\n')
            f.write(f'ANN {self.n_neuron} 0\n')

            # neural network weights
            keys = self.types if self.version in (4, 5) else ['all_species']
            suffixes = ['', '_polar'] if self.model_type == 'polarizability' else ['']
            for suffix in suffixes:
                for s in keys:
                    # Order: w0, b0, w1 (, b1 if NEP5)
                    # w0 indexed as: n*N_descriptor + nu
                    w0 = self.ann_parameters[s][f'w0{suffix}']
                    b0 = self.ann_parameters[s][f'b0{suffix}']
                    w1 = self.ann_parameters[s][f'w1{suffix}']
                    for n in range(self.n_neuron):
                        for nu in range(
                            self.n_descriptor_radial + self.n_descriptor_angular
                        ):
                            f.write(f'{w0[n, nu]:15.7e}\n')
                    for b in b0[:, 0]:
                        f.write(f'{b:15.7e}\n')
                    for v in w1[0, :]:
                        f.write(f'{v:15.7e}\n')
                    if self.version == 5:
                        b1 = self.ann_parameters[s][f'b1{suffix}']
                        f.write(f'{b1:15.7e}\n')
                b1 = self.ann_parameters[f'b1{suffix}']
                f.write(f'{b1:15.7e}\n')

            # descriptor weights
            mat = []
            for s1 in self.types:
                for s2 in self.types:
                    mat = np.hstack(
                        [mat, self.radial_descriptor_weights[(s1, s2)].flatten()]
                    )
                    mat = np.hstack(
                        [mat, self.angular_descriptor_weights[(s1, s2)].flatten()]
                    )
            n_types = len(self.types)
            n = int(len(mat) / (n_types * n_types))
            mat = mat.reshape((n_types * n_types, n)).T
            for v in mat.flatten():
                f.write(f'{v:15.7e}\n')

            # scaler
            for v in self.q_scaler:
                f.write(f'{v:15.7e}\n')


def read_model(filename: str) -> Model:
    """Parses a file in ``nep.txt`` format and returns the
    content in the form of a :class:`Model <calorine.nep.model.Model>`
    object.

    Parameters
    ----------
    filename
        Input file name.
    """
    data, parameters = _get_nep_contents(filename)

    # sanity checks
    for fld in ['cutoff', 'basis_size', 'n_max', 'l_max', 'ANN']:
        assert fld in data, f'Invalid model file; {fld} line is missing'
    assert data['version'] in [
        3,
        4,
        5,
    ], 'Invalid model file; only NEP versions 3, 4 and 5 are currently supported'

    # split up cutoff tuple
    assert len(data['cutoff']) in [4, 6, 7]
    data['radial_cutoff'] = data['cutoff'][0]
    data['angular_cutoff'] = data['cutoff'][1]
    data['max_neighbors_radial'] = int(data['cutoff'][2])
    data['max_neighbors_angular'] = int(data['cutoff'][3])
    if len(data['cutoff']) >= 6:
        data['radial_typewise_cutoff_factor'] = data['cutoff'][4]
        data['angular_typewise_cutoff_factor'] = data['cutoff'][5]
    if len(data['cutoff']) == 7:
        data['zbl_typewise_cutoff_factor'] = data['cutoff'][6]
    del data['cutoff']

    # split up basis_size tuple
    assert len(data['basis_size']) == 2
    data['n_basis_radial'] = data['basis_size'][0]
    data['n_basis_angular'] = data['basis_size'][1]
    del data['basis_size']

    # split up n_max tuple
    assert len(data['n_max']) == 2
    data['n_max_radial'] = data['n_max'][0]
    data['n_max_angular'] = data['n_max'][1]
    del data['n_max']

    # split up nl_max tuple
    len_l = len(data['l_max'])
    assert len_l in [1, 2, 3]
    data['l_max_3b'] = data['l_max'][0]
    data['l_max_4b'] = data['l_max'][1] if len_l > 1 else 0
    data['l_max_5b'] = data['l_max'][2] if len_l > 2 else 0
    del data['l_max']

    # compute dimensions of descriptor components
    data['n_descriptor_radial'] = data['n_max_radial'] + 1
    l_max_enh = data['l_max_3b'] + (data['l_max_4b'] > 0) + (data['l_max_5b'] > 0)
    data['n_descriptor_angular'] = (data['n_max_angular'] + 1) * l_max_enh
    n_descriptor = data['n_descriptor_radial'] + data['n_descriptor_angular']

    # compute number of parameters
    data['n_neuron'] = data['ANN'][0]
    del data['ANN']
    n_types = len(data['types'])
    if data['version'] == 3:
        n = 1
        n_bias = 1
    elif data['version'] == 4:
        # one hidden layer per atomic species
        n = n_types
        n_bias = 1
    else:  # NEP5
        # like nep4, but additionally has an
        # individual bias term in the output
        # layer for each species.
        n = n_types
        n_bias = 1 + n_types  # one global bias + one per species

    n_ann_input_weights = (n_descriptor + 1) * data['n_neuron']  # weights + bias
    n_ann_output_weights = data['n_neuron']  # only weights
    n_ann_parameters = (
        n_ann_input_weights + n_ann_output_weights
    ) * n + n_bias

    n_descriptor_weights = n_types**2 * (
        (data['n_max_radial'] + 1) * (data['n_basis_radial'] + 1)
        + (data['n_max_angular'] + 1) * (data['n_basis_angular'] + 1)
    )
    data['n_parameters'] = n_ann_parameters + n_descriptor_weights + n_descriptor
    is_polarizability_model = data['model_type'] == 'polarizability'
    if data['n_parameters'] + n_ann_parameters == len(parameters):
        data['n_parameters'] += n_ann_parameters
        assert is_polarizability_model, (
            'Model is not labelled as a polarizability model, but the number of '
            'parameters matches a polarizability model.\n'
            'If this is a polarizability model trained with GPUMD <=v3.8, please '
            'modify the header in the nep.txt file to read '
            f'`nep{data["version"]}_polarizability`.\n'
        )
    assert data['n_parameters'] == len(parameters), (
        'Parsing of parameters inconsistent; please submit a bug report\n'
        f'{data["n_parameters"]} != {len(parameters)}'
    )
    data['n_ann_parameters'] = n_ann_parameters

    # split up parameters into the ANN weights, descriptor weights, and scaling parameters
    n1 = n_ann_parameters
    n1 *= 2 if is_polarizability_model else 1
    n2 = n1 + n_descriptor_weights
    data['ann_parameters'] = parameters[:n1]
    descriptor_weights = np.array(parameters[n1:n2])
    data['q_scaler'] = parameters[n2:]

    # Group ANN parameters
    pars = {}
    n1 = 0
    n_network_params = n_ann_input_weights + n_ann_output_weights  # except last bias
    n_neuron = data['n_neuron']
    keys = data['types'] if data['version'] in (4, 5) else ['all_species']

    n_count = 2 if is_polarizability_model else 1
    for count in range(n_count):
        # if polarizability model, all parameters including bias are repeated
        # need to offset n1 by +1 to handle bias
        n1 += count
        for s in keys:
            # Get the parameters for the ANN; in the case of NEP4, there is effectively
            # one network per atomic species.
            ann_parameters = data['ann_parameters'][n1 : n1 + n_network_params]
            ann_input_weights = ann_parameters[:n_ann_input_weights]
            w0 = np.zeros((n_neuron, n_descriptor))
            w0[...] = np.nan
            b0 = np.zeros((n_neuron, 1))
            b0[...] = np.nan
            for n in range(n_neuron):
                for nu in range(n_descriptor):
                    w0[n, nu] = ann_input_weights[n * n_descriptor + nu]
            b0[:, 0] = ann_input_weights[n_neuron * n_descriptor :]

            assert np.all(
                w0.shape == (n_neuron, n_descriptor)
            ), f'w0 has invalid shape for key {s}; please submit a bug report'
            assert np.all(
                b0.shape == (n_neuron, 1)
            ), f'b0 has invalid shape for key {s}; please submit a bug report'
            assert not np.any(
                np.isnan(w0)
            ), f'some weights in w0 are nan for key {s}; please submit a bug report'
            assert not np.any(
                np.isnan(b0)
            ), f'some weights in b0 are nan for key {s}; please submit a bug report'

            ann_output_weights = ann_parameters[
                n_ann_input_weights : n_ann_input_weights + n_ann_output_weights
            ]

            w1 = np.zeros((1, n_neuron))
            w1[0, :] = ann_output_weights[:]
            assert np.all(
                w1.shape == (1, n_neuron)
            ), f'w1 has invalid shape for key {s}; please submit a bug report'
            assert not np.any(
                np.isnan(w1)
            ), f'some weights in w1 are nan for key {s}; please submit a bug report'

            if count == 0:
                pars[s] = dict(w0=w0, b0=b0, w1=w1)
            else:
                pars[s].update({'w0_polar': w0, 'b0_polar': b0, 'w1_polar': w1})
            # Jump to bias
            n1 += n_network_params
            if n_bias > 1:
                # For NEP5 models we additionally have one bias term per species.
                # Currently NEP5 only exists for potential models, but we'll
                # keep it here in case it gets added down the line.
                bias_label = 'b1' if count == 0 else 'b1_polar'
                pars[s][bias_label] = data['ann_parameters'][n1]
                n1 += 1
        # For NEP3 and NEP4 we only have one bias.
        # For NEP5 we have one bias per species, and one global.
        if count == 0:
            pars['b1'] = data['ann_parameters'][n1]
        else:
            pars['b1_polar'] = data['ann_parameters'][n1]
    sum = 0
    for s in pars.keys():
        if s.startswith('b1'):
            sum += 1
        else:
            sum += np.sum([np.count_nonzero(p) for p in pars[s].values()])
    assert sum == n_ann_parameters * n_count, (
        'Inconsistent number of parameters accounted for; please submit a bug report\n'
        f'{sum} != {n_ann_parameters}'
    )
    data['ann_parameters'] = pars

    # split up descriptor by chemical species and radial/angular
    data['n_descriptor_parameters'] = len(descriptor_weights)
    n = int(len(descriptor_weights) / (n_types * n_types))
    n_max_radial = data['n_max_radial']
    n_max_angular = data['n_max_angular']
    n_basis_radial = data['n_basis_radial']
    n_basis_angular = data['n_basis_angular']
    m = (n_max_radial + 1) * (n_basis_radial + 1)
    descriptor_weights = descriptor_weights.reshape((n, n_types * n_types)).T
    descriptor_weights_radial = descriptor_weights[:, :m]
    descriptor_weights_angular = descriptor_weights[:, m:]

    # add descriptors to data dict
    data['radial_descriptor_weights'] = {}
    data['angular_descriptor_weights'] = {}
    m = -1
    for i, j in product(range(n_types), repeat=2):
        m += 1
        s1, s2 = data['types'][i], data['types'][j]
        subdata = descriptor_weights_radial[m, :].reshape(
            (n_max_radial + 1, n_basis_radial + 1)
        )
        data['radial_descriptor_weights'][(s1, s2)] = subdata
        subdata = descriptor_weights_angular[m, :].reshape(
            (n_max_angular + 1, n_basis_angular + 1)
        )
        data['angular_descriptor_weights'][(s1, s2)] = subdata

    return Model(**data)
