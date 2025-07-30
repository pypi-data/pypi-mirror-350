# from sys import argv  # for benchmarking only
import logging
import time
# import warnings
from functools import partial
from typing import Union

from MDAnalysis.transformations.wrap import wrap
import MDAnalysis as mda
import numpy as np

from scipy.spatial import ConvexHull
from tqdm import tqdm
# from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from multiprocessing import Manager

from PUCHIK.grid_project.core.AlphaShape import AlphaShape
from PUCHIK.grid_project.utilities.MoleculeSystem import MoleculeSystem
# Local imports
from PUCHIK.grid_project.utilities.decorators import logger  # , timer
from PUCHIK.grid_project.settings import DEBUG, CPU_COUNT, TQDM_BAR_FORMAT
from PUCHIK.grid_project.core.utils import find_distance, _is_inside

# from .utils_python import find_distance, _is_inside
logging.basicConfig(format='%(message)s')
np.seterr(invalid='ignore', divide='ignore')

"""
    Grid method for analyzing complex shaped structures
"""


class Interface(MoleculeSystem):
    """
        Class creates to create a mesh of points representing different molecule
        types of the system in a grid

        Attributes:
            traj (str): Path to any trajectory format supported by MDAnalysis package
            top (str): Path to any topology format supported by MDAnalysis package. Defaults to None
    """

    def __init__(self, traj, top=None):
        self.grid_matrix = None
        self.u: mda.Universe = mda.Universe(top, traj) if top else mda.Universe(traj)
        self.ag = None
        self.unique_resnames = None
        self.main_structure_selection = None
        self.current_frame = 0

        manager = Manager()
        self._hull = manager.dict()

        self._use_alpha_shape = False

    @property
    def use_alpha_shape(self):
        return self._use_alpha_shape

    @use_alpha_shape.setter
    def use_alpha_shape(self, val):
        if type(val) is not bool:
            raise TypeError('use_alpha_shape must be a boolean')
        self._use_alpha_shape = val

    def select_atoms(self, sel='all'):
        """
        Method for selecting the atoms using MDAnalysis selections

        :param sel: selection string
        :return:
        """
        self.ag = self.u.select_atoms(sel)
        self.unique_resnames = np.unique(self.ag.resnames)
        print('Wrapping trajectory...')
        transform = wrap(self.ag)
        self.u.trajectory.add_transformations(transform)

    def select_structure(self, selection):
        """
        Use this method to select the structure for density calculations․

        :param selection: selection(s) of the main structure
        :return: None
        """
        self.main_structure_selection = selection

    def _get_int_dim(self):
        """
        Utility function to get box dimensions

        Returns:
            Dimensions of the box as an int
        """
        return int(np.ceil(self.u.dimensions[0]))

    @staticmethod
    def make_grid(pbc_dim: int, dim=1, d4=None) -> np.ndarray:
        """
        Returns a 4D matrix

        Args:
             pbc_dim (int): Dimensions of the box
             dim (int): Dimensions of the box
             d4 (int): Returns an 4-D matrix if d4 is given. 4th dimension contains d4 elements
        """

        x = y = z = pbc_dim // dim + 1
        grid_matrix = np.zeros((x, y, z)) if d4 is None else np.zeros((x, y, z, d4))

        return grid_matrix

    @staticmethod
    def check_cube(x: float, y: float, z: float) -> tuple:
        """
        Find to which cube does the atom belong to
        Args:
            x (float): x coordinate
            y (float): y coordinate
            z (float): z coordinate

        Returns:
            tuple: Coordinates of the node inside the grid where the point belongs
        """

        n_x = int(x)
        n_y = int(y)
        n_z = int(z)

        return n_x, n_y, n_z

    @staticmethod
    def make_coordinates(mesh):
        """
        Converts the mesh to coordinates
        Args:
            mesh (np.ndarray):  Mesh to convert into 3D coordinates

        Returns:
            np.ndarray: Ndarray of tuples representing coordinates of each of the points in the mesh
        """

        return np.argwhere(mesh > 0)

    def _calc_mesh(self, grid_dim, selection):
        """
        Calculates the mesh according the atom positions in the box

        Args:
            grid_dim (int): Box dimensions

        Returns:
            np.ndarray: The grid
        """
        atom_group = self.u.select_atoms(selection)
        grid_matrix = self.make_grid(grid_dim)

        for atom in atom_group:
            x, y, z = self.check_cube(*atom.position)
            # Correct outlying coordinates !TODO Create a separate utility function for such checks
            x = min(max(x, 0), grid_dim - 1)
            y = min(max(y, 0), grid_dim - 1)
            z = min(max(z, 0), grid_dim - 1)

            grid_matrix[x, y, z] += 1

        return grid_matrix

    # @logger(DEBUG)
    def calculate_mesh(self, selection, main_structure=False):
        """
        Calculates the mesh using _calc_mesh method
        Args:
            selection (str): Selection for atom group to calculate mesh
            main_structure (bool): use as the main structure if true (e.g. densities are calculated relative to this)
        Returns:
            np.ndarray: Returns the grid matrix
        """
        # define the matrices

        grid_matrix = self._calc_mesh(self._get_int_dim(), selection)  # !TODO _get_int_dim փոխի

        if main_structure:  # if selection is None, then it's the main structure
            self.grid_matrix = grid_matrix

        return grid_matrix

    # @logger(DEBUG)

    def _calculate_density_grid(self, coords, bin_count):
        # Works on a cubic box. !TODO Generalize later
        self.u.trajectory[self.current_frame]  # Set the frame to the current frame. Must be a better way...

        coords = np.array(coords)
        density_grid = np.zeros((bin_count, bin_count, bin_count))

        edges, step = np.linspace(0, self._get_int_dim(), bin_count + 1, retstep=True)
        grid_cell_volume = step ** 3

        # y_edges = np.linspace(0, self._get_int_dim(), bin_count + 1)
        # z_edges = np.linspace(0, self._get_int_dim(), bin_count + 1)

        for x, y, z in coords:
            x_idx = np.digitize(x, edges) - 1
            y_idx = np.digitize(y, edges) - 1
            z_idx = np.digitize(z, edges) - 1

            # This is to ensure indices are within the grid bounds
            x_idx = min(max(x_idx, 0), bin_count - 1)
            y_idx = min(max(y_idx, 0), bin_count - 1)
            z_idx = min(max(z_idx, 0), bin_count - 1)

            density_grid[x_idx, y_idx, z_idx] += 1

        density_grid /= grid_cell_volume

        return density_grid

    def _grid_centers(self, bin_count):
        edges, step = np.linspace(0, self._get_int_dim(), bin_count + 1, retstep=True)
        x_centers = (edges[:-1] + edges[1:]) / 2
        y_centers = (edges[:-1] + edges[1:]) / 2
        z_centers = (edges[:-1] + edges[1:]) / 2
        x_grid, y_grid, z_grid = np.meshgrid(x_centers, y_centers, z_centers, indexing='ij')

        return np.vstack([x_grid.ravel(), y_grid.ravel(), z_grid.ravel()]).T

    def _normalize_density(self, coords, bin_count):
        density_grid = self._calculate_density_grid(coords, bin_count)
        density_grid = density_grid.flatten()

        return density_grid

    def _extract_from_mesh(self, mol_type):
        if mol_type not in self.unique_resnames:
            raise ValueError(
                f'Molecule type "{mol_type}" is not present in the system. Available types: {self.unique_resnames}'
            )

        mol_index = np.where(self.unique_resnames == mol_type)

        return self.grid_matrix[:, :, :, mol_index]

    def _create_hull(self):
        if not self.main_structure_selection:
            raise ValueError('Select the main structure with "select_structure" before running calculations')
        if self._hull.get(self.current_frame):
            # If the hull was calculated for this frame, just return it
            return self._hull[self.current_frame]

        mesh = self.calculate_mesh(selection=self.main_structure_selection, main_structure=True)

        mesh_coords = self.make_coordinates(mesh[:, :, :])
        mesh_coordinates = np.array(mesh_coords)
        # try:
        if self.use_alpha_shape:
            hull = AlphaShape(mesh_coordinates).calculate_as(self.current_frame)
        else:
            hull = ConvexHull(mesh_coordinates)
        self._hull[self.current_frame] = hull
        return hull

    def _calc_dens(self, frame_num, selection, norm_bin_count):
        """
        Calculates the density of selection from interface.

        Args:
            frame_num (int): Number of the frame
            selection (str): Selection of the atom group density of which is to be calculated
            ratio (float): Ratio moltype/water !TODO for testing. Remove later
        Returns:
            tuple: Density array and corresponding distances
        """
        self.current_frame = frame_num
        self.u.trajectory[self.current_frame]

        selection_coords = self.u.select_atoms(selection).positions  # self.make_coordinates(selection_mesh)

        hull = self._create_hull()

        grid_centers = self._grid_centers(bin_count=norm_bin_count)

        distances = np.array(
            find_distance(hull, grid_centers)
        )  # Calculate distances from the interface to each grid cell
        densities = self._normalize_density(
            selection_coords,
            bin_count=norm_bin_count
        )  # Calculate the density of each cell

        indices = np.argsort(distances)
        distances = distances[indices]
        densities = densities[indices]

        return distances, densities

    # @timer
    def calculate_density(self, selection=None, start=0, skip=1, end=None,
                          norm_bin_count=20, cpu_count=CPU_COUNT, mp=True):
        """
        Calculates density of selection from the interface
        :param end: Final frame
        :param norm_bin_count: Bin count for normalization
        :param cpu_count: Number of cores to use
        :param selection: MDAnalysis selection of ag
        :param interface_selection: Selection of what is considered as interface
        :param start: Starting frame
        :param skip: Skip every n-th frame
        :param mp: If False, computation will be performed iteratively on a single process

        :return:
        """
        n_frames = self.u.trajectory.n_frames if end is None else end
        frame_range = range(start, n_frames, skip)
        print(f'Running density calculation for the following atom group: {selection}')
        if mp:
            res = self._mp_calc(self._calc_dens, frame_range, cpu_count, selection=selection,
                                norm_bin_count=norm_bin_count)
        else:
            # Single-process calculation
            start = time.perf_counter()

            res = [None] * len(frame_range)
            for index, i in enumerate(tqdm(frame_range, bar_format=TQDM_BAR_FORMAT)):
                res[index] = self._calc_dens(i, selection, norm_bin_count)
            res = np.array(res)
            print(f'Execution time for {len(frame_range)} frames:', time.perf_counter() - start)

        distances, densities = self._process_result(res)

        # Simply taking the mean might not be the best option
        # distances = distances.mean(axis=0)
        # densities = densities.mean(axis=0)

        return distances, densities

    @staticmethod
    def _process_result(res):
        """ Helper method to correctly calculate the average of the result """
        distances = res[:, 0]
        densities = res[:, 1]
        dim_1, dim_2 = distances.shape
        offset = 50  # an offset to shift the distances to correct positions

        offset_distances = np.zeros((dim_1, dim_2 + offset))
        offset_densities = np.zeros((dim_1, dim_2 + offset))
        for i, arr in enumerate(distances):
            minim = abs(int(arr[0]))

            offset_minim = offset - minim  # Ensure index is non-negative

            offset_distances[i, offset_minim:dim_2 + offset_minim] = arr
            offset_densities[i, offset_minim:dim_2 + offset_minim] = densities[i]

        # Trim zeros
        global_min = abs(int(distances.min()))

        offset_global_min = offset - global_min  # Again, ensure index is non-negative

        final_distances = offset_distances[:, offset_global_min:dim_2 + offset_global_min]
        final_densities = offset_densities[:, offset_global_min:dim_2 + offset_global_min]

        final_distances = final_distances.mean(axis=0, where=final_distances != 0)
        final_densities = final_densities.mean(axis=0, where=final_distances != 0)

        return final_distances, final_densities

    def _calc_count(self, frame_num, selection) -> int:

        self.current_frame = frame_num
        self.u.trajectory[self.current_frame]

        ag = self.u.select_atoms(selection)
        n_atoms = len(ag) // ag.n_residues

        hull = self._create_hull()
        coms = []
        count = 0

        for i in range(ag.n_residues):
            coms.append(ag[i * n_atoms: (i + 1) * n_atoms].center_of_mass())

        for com in coms:
            if _is_inside(com, hull, self.use_alpha_shape):
                count += 1

        return count

    def mol_count(self, selection, start=0, skip=1, end=None, cpu_count=CPU_COUNT):
        """
        The method calculates and returns the number of <selection> molecules inside the interface
        :param selection: Selection for molecules to check if they are solubilized in the NP or no
        :param start:
        :param skip:
        :param end:
        :param cpu_count:
        :return: ndarray containing number of molecules each frame
        """
        n_frames = self.u.trajectory.n_frames if end is None else end
        frame_range = range(start, n_frames, skip)

        print(f'Calculating number of "{selection}" molecules inside the interface')

        res = self._mp_calc(self._calc_count, frame_range, cpu_count, selection=selection)

        return res

    def _calc_hull(self, frame_num):
        self.current_frame = frame_num
        self.u.trajectory[self.current_frame]

        return self._create_hull()

    @logger(DEBUG)
    def calculate_volume(self, area=False, start=0, skip=1, end=None, cpu_count=CPU_COUNT) -> Union[tuple, np.ndarray]:
        """
        Returns the volume of the hull
        :param bool area: If True, return the area of the hull as well
        :param int start: First frame of the trajectory
        :param int skip: How many frames to skip
        :param int end: Final frame of the trajectory
        :param int cpu_count: Sets the number of cores to utilize during the calculation
        :return [tuple, np.ndarray] volume: ndarray containing the volume values of the hull at each frame, or a tuple
        of ndarrays for volumes and areas
        """
        if self.use_alpha_shape:
            raise NotImplementedError('Volume calculations using alpha shapes is not yet implemented')

        n_frames = self.u.trajectory.n_frames if end is None else end
        frame_range = range(start, n_frames, skip)
        print('Calculating the volume of the selected structure')
        hulls = self._mp_calc(self._calc_hull, frame_range, cpu_count)
        return np.array([hull.volume for hull in hulls]) if not area else (
            np.array([hull.volume for hull in hulls]),
            np.array([hull.area for hull in hulls])
        )

    @staticmethod
    def _sp_calc(func):
        ...

    @staticmethod
    def _mp_calc(func, frame_range, cpu_count, **kwargs) -> np.ndarray:
        """
        This method handles multiprocessing
        :param func:
        :param frame_range:
        :param cpu_count:
        :param kwargs:
        :return:
        """
        # start = time.perf_counter()
        per_frame_func = partial(func, **kwargs)
        res = process_map(per_frame_func, frame_range,
                          max_workers=cpu_count,
                          bar_format=TQDM_BAR_FORMAT
                          )
        # print(f'Execution time for {len(frame_range)} frames:', time.perf_counter() - start)

        return np.array(res)


if __name__ == '__main__':
    pass
