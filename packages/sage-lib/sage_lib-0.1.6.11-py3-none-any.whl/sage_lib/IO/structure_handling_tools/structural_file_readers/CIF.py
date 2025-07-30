class CIF:
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        pass

    def read_CIF(self, file_location:str=None):
        try:
            import numpy as np
        except ImportError as e:
            import sys
            sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
            del sys

        file_location = file_location if type(file_location) == str else self._file_location

        lines = [n for n in self.read_file() ]
        # Initialize variables
        self._latticeParameters = [0,0,0]
        self._latticeAngles = [0,0,0]
        self._atomPositions = []
        self._symmetryEquivPositions = []
        self._atomLabelsList = []

        # Flags to indicate the reading context
        reading_atoms = False
        reading_symmetry = False

        for line in lines:
            line = line.strip()

            # Lattice Parameters
            if line.startswith('_cell_length_a'):
                self._latticeParameters[0] = float(line.split()[1])
            elif line.startswith('_cell_length_b'):
                self._latticeParameters[1] = float(line.split()[1])
            elif line.startswith('_cell_length_c'):
                self._latticeParameters[2] = float(line.split()[1])

            # Lattice angles
            if line.startswith('_cell_angle_alpha'):
                self._latticeAngles[0] = np.radians(float(line.split()[1]))
            elif line.startswith('_cell_angle_beta'):
                self._latticeAngles[1] = np.radians(float(line.split()[1]))
            elif line.startswith('_cell_angle_gamma'):
                self._latticeAngles[2] = np.radians(float(line.split()[1]))


            # Symmetry Equiv Positions
            elif line.startswith('loop_'):
                reading_atoms = False  # Reset flags
                reading_symmetry = False  # Reset flags
            elif line.startswith('_symmetry_equiv_pos_as_xyz'):
                reading_symmetry = True
                continue  # Skip the line containing the column headers
            elif reading_symmetry:
                self._symmetryEquivPositions.append(line)

            # Atom positions
            elif line.startswith('_atom_site_label'):
                reading_atoms = True  # Set flag to start reading atoms
                continue  # Skip the line containing the column headers
            elif reading_atoms:
                tokens = line.split()
                if len(tokens) >= 4:  # Make sure it's a complete line
                    label, x, y, z = tokens[:4]
                    self._atomPositions.append([float(x), float(y), float(z)])
                    self._atomLabelsList.append(label)

        # Convert to numpy arrays
        self._atomPositions = np.array(self._atomPositions, dtype=np.float64)
        self._atomicConstraints = np.ones_like(self._atomPositions)
        self._atomCount = self._atomPositions.shape[0]
        self._atomCoordinateType = 'direct'
        self._selectiveDynamics = True
        self._scaleFactor = [1]

        return True
        