try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

class AtomPositionMaker:
    """
    A class to build and manipulate molecular structures, particularly diatomic and triatomic compounds.

    Attributes:
        _diatomic_compounds (dict): A dictionary containing information about various diatomic compounds.
        _triatomic_compounds (dict): A dictionary containing information about various triatomic compounds.

    Methods:
        get_triatomic_compound(name): Retrieves the information of a triatomic compound based on its name.
        build_molecule(atomLabels, atomPositions, center): Constructs a molecule from atom labels and positions.
        build(name): Builds a molecule based on the given name, looking up its structure from predefined compounds.
    """

    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initializes the AtomPositionMaker class.

        Args:
            file_location (str, optional): The location of a file containing molecular data.
            name (str, optional): The name of the molecule.

        The class also accepts additional keyword arguments (**kwargs) for future extensions.
        """
        self._atomic_compounds = { f'{a}':  {'atomLabels': [f'{a}' ],   'atomPositions': [[0, 0, 0]]} for a in self.atomic_numbers }

        self._diatomic_compounds = {
            'H2':  {'atomLabels': ['H', 'H'],   'atomPositions': [[0, 0, 0], [0, 0, 0.74]]},  
            'O2':  {'atomLabels': ['O', 'O'],   'atomPositions': [[0, 0, 0], [0, 0, 1.21]]},  
            'OH':  {'atomLabels': ['O', 'H'],   'atomPositions': [[0, 0, 0], [0, 0, 0.97]]},  
            'N2':  {'atomLabels': ['N', 'N'],   'atomPositions': [[0, 0, 0], [0, 0, 1.10]]},  
            'F2':  {'atomLabels': ['F', 'F'],   'atomPositions': [[0, 0, 0], [0, 0, 1.42]]},  
            'Cl2': {'atomLabels': ['Cl', 'Cl'], 'atomPositions': [[0, 0, 0], [0, 0, 1.99]]},  
            'Br2': {'atomLabels': ['Br', 'Br'], 'atomPositions': [[0, 0, 0], [0, 0, 2.28]]},  
            'I2':  {'atomLabels': ['I', 'I'],   'atomPositions': [[0, 0, 0], [0, 0, 2.66]]},  
            'HF':  {'atomLabels': ['H', 'F'],   'atomPositions': [[0, 0, 0], [0, 0, 0.92]]},  
            'CO':  {'atomLabels': ['C', 'O'],   'atomPositions': [[0, 0, 0], [0, 0, 1.13]]},  
            'NO':  {'atomLabels': ['N', 'O'],   'atomPositions': [[0, 0, 0], [0, 0, 1.15]]},  
            'CN':  {'atomLabels': ['C', 'N'],   'atomPositions': [[0, 0, 0], [0, 0, 1.17]]},  
            'BO':  {'atomLabels': ['B', 'O'],   'atomPositions': [[0, 0, 0], [0, 0, 1.21]]},  
            'SiO': {'atomLabels': ['Si', 'O'],  'atomPositions': [[0, 0, 0], [0, 0, 1.52]]},  
            'CuO': {'atomLabels': ['Cu', 'O'],  'atomPositions': [[0, 0, 0], [0, 0, 1.82]]}   
        }

        self._triatomic_compounds = {
            'CO2': {'atomLabels': ['C', 'O', 'O'], 'atomPositions': [[0, 0, 0], [0, 0, 1.16], [0, 0, -1.16]]},
            'H2O': {'atomLabels': ['O', 'H', 'H'], 'atomPositions': [
                [0, 0, 0], 
                [0.96 * np.cos(np.radians(104.5 / 2)), 0, 0.96 * np.sin(np.radians(104.5 / 2))], 
                [0.96 * np.cos(np.radians(104.5 / 2)), 0, -0.96 * np.sin(np.radians(104.5 / 2))]]},
            'SO2': {'atomLabels': ['S', 'O', 'O'], 'atomPositions': [
                [0, 0, 0], 
                [1.43 * np.cos(np.radians(119.5)), 0, 1.43 * np.sin(np.radians(119.5))], 
                [-1.43 * np.cos(np.radians(119.5)), 0, -1.43 * np.sin(np.radians(119.5))]]},  
            'O3':  {'atomLabels': ['O', 'O', 'O'], 'atomPositions': [
                [0, 0, 0], 
                [1.28 * np.cos(np.radians(116.8)), 0, 1.28 * np.sin(np.radians(116.8))], 
                [-1.28 * np.cos(np.radians(116.8)), 0, -1.28 * np.sin(np.radians(116.8))]]},
            'HCN': {'atomLabels': ['H', 'C', 'N'], 'atomPositions': [[0, 0, 1.06], [0, 0, 0], [0, 0, -1.16]]},
            'H2S': {'atomLabels': ['S', 'H', 'H'], 'atomPositions': [
                [0, 0, 0], 
                [0.96 * np.cos(np.radians(92.1 / 2)), 0, 0.96 * np.sin(np.radians(92.1 / 2))], 
                [0.96 * np.cos(np.radians(92.1 / 2)), 0, -0.96 * np.sin(np.radians(92.1 / 2))]]},  
            'CS2': {'atomLabels': ['C', 'S', 'S'], 'atomPositions': [[0, 0, 0], [0, 0, 1.55], [0, 0, -1.55]]},  
            'NO2': {'atomLabels': ['N', 'O', 'O'], 'atomPositions': [
                [0, 0, 0], 
                [1.20 * np.cos(np.radians(134.1)), 0, 1.20 * np.sin(np.radians(134.1))], 
                [-1.20 * np.cos(np.radians(134.1)), 0, -1.20 * np.sin(np.radians(134.1))]]},  
            'HCO': {'atomLabels': ['H', 'C', 'O'], 'atomPositions': [[0, 0, 1.10], [0, 0, 0], [0, 0, -1.12]]}, 
            'HOF': {'atomLabels': ['H', 'O', 'F'], 'atomPositions': [[0, 0, 1.10], [0, 0, 0], [0, 0, -1.44]]}, 
            'C2H2': {'atomLabels': ['C', 'C', 'H', 'H'], 'atomPositions': [[0, 0, 0], [1.20, 0, 0], [0, 0, 1.08], [1.20, 0, -1.08]]}  
        }

    def get_triatomic_compound(self, name):
        """
        Retrieves the information of a specified triatomic compound.

        Args:
            name (str): The name of the triatomic compound.

        Returns:
            dict: A dictionary containing the atom labels and positions of the compound, or None if not found.
        """
        return self._triatomic_compounds.get(name, None)

    def build_molecule(self, atomLabels:list, atomPositions:np.array, center:str='mass_center'):
        """
        Constructs a molecule from provided atom labels and positions, and aligns it based on the specified center.

        Args:
            atomLabels (list): A list of atom labels.
            atomPositions (np.array): A NumPy array of atom positions.
            center (str): The centering method to be used for the molecule ('mass_center', 'gravity_center', 'geometric_center', or 'baricenter').

        This function adds atoms to the molecule, calculates the displacement based on the chosen centering method, and aligns the molecule accordingly.
        """
        # Add atoms to the molecule
        for al, ap in zip(atomLabels, atomPositions):
            self.add_atom(al, ap, [1,1,1])

        # Calculate displacement based on the centering method
        if center == 'mass_center' or center == 'gravity_center':
            displacement = np.sum(self.atomPositions.T * self.mass_list, axis=1) /  np.sum(self.mass_list)

        elif center == 'geometric_center' or center == 'baricenter':
            displacement = np.mean(self.atomPositions, axis=1)
        
        else:
            displacement = np.array([0,0,0])

        # Align the molecule by adjusting atom positions
        self.set_atomPositions(self.atomPositions-displacement)

    def build(self, name:str):
        """
        Builds a molecule based on the given name.

        Args:
            name (str): The name of the molecule to be built.

        This method looks up the molecule's structure from predefined compounds and constructs it.
        """

        if name in self.atomic_compounds:
            atomLabels = self.atomic_compounds[name]['atomLabels']
            atomPositions = self.atomic_compounds[name]['atomPositions']

        if name in self.diatomic_compounds:
            atomLabels = self.diatomic_compounds[name]['atomLabels']
            atomPositions = self.diatomic_compounds[name]['atomPositions']

        if name in self.triatomic_compounds:
            atomLabels = self.triatomic_compounds[name]['atomLabels']
            atomPositions = self.triatomic_compounds[name]['atomPositions']
        
        self.build_molecule(atomLabels, atomPositions)

