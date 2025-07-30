import json
import re
import numpy as np
from typing import Optional, List, Dict, Any

class XYZ:
    def __init__(self, file_location: str = None, name: str = None, **kwargs):
        """
        Initializes the XYZ object.

        Parameters:
            file_location (str): The default path for reading/writing XYZ files.
            name (str): An identifier for this XYZ object.
            **kwargs: Additional keyword arguments passed to the parent constructor.
        """
        self.property_info = None
        self.metadata = None  # Initialize metadata; can hold a dict of lists or any structured data.

    def export_as_xyz(self, file_location: str = None, save_to_file: str = 'w', verbose: bool = False,
                      species: bool = True, position: bool = True, energy: bool = True, forces: bool = True,
                      charge: bool = True, magnetization: bool = True, lattice: bool = True, pbc: bool = True,
                      time: bool = True, fixed: bool = True, class_ID: bool = True,
                      position_tag: str = 'pos', forces_tag: str = 'forces', charge_tag: str = 'charge',
                      magnetization_tag: str = 'magnetization', energy_tag: str = 'energy',
                      fixed_tag: str = 'fixed', time_tag: str = 'time', pbc_tag: str = 'pbc',
                      classID_tag: str = 'class_ID') -> str:
        """
        Export atomistic information in an extended XYZ format and optionally write it to a file.

        This method has been extended to also serialize and store self.metadata (if present)
        in the header using JSON.

        Parameters:
            file_location (str): Path to save the XYZ file (if save_to_file is not 'none').
            save_to_file (str): File write mode or 'none' to disable file writing.
            verbose (bool): If True, prints additional information about the saving process.
            species, position, energy, forces, charge, magnetization, lattice, pbc, time, fixed, class_ID (bool):
                Toggle whether the corresponding data is included in the XYZ export.
            position_tag, forces_tag, charge_tag, magnetization_tag, energy_tag, fixed_tag, time_tag,
            pbc_tag, classID_tag (str): Customizable tags for each property in the header.

        Returns:
            str: The extended XYZ content generated.
        """
        # Resolve file_location; if None, fall back to the object's file_location or default suffix
        file_location = (file_location if file_location is not None
                         else (self.file_location + 'config.xyz'
                               if isinstance(self.file_location, str)
                               else self.file_location))

        # Ensure data grouping or preparation before accessing members
        self.group_elements_and_positions()

        # Determine which properties exist and are non-None
        include_lattice = hasattr(self, 'latticeVectors') and self.latticeVectors is not None and lattice
        include_species = hasattr(self, 'atomLabelsList') and self.atomLabelsList is not None and species
        include_position = hasattr(self, 'atomPositions') and self.atomPositions is not None and position
        include_forces = hasattr(self, 'total_force') and self.total_force is not None and forces
        include_charge = hasattr(self, 'charge') and self.charge is not None and charge
        include_magnetization = hasattr(self, 'magnetization') and self.magnetization is not None and magnetization
        include_energy = hasattr(self, 'E') and self.E is not None and energy
        include_pbc = hasattr(self, 'latticeVectors') and self.latticeVectors is not None and pbc
        include_time = hasattr(self, 'time') and self.time is not None and time
        include_fixed = hasattr(self, 'selectiveDynamics') and self.selectiveDynamics and fixed
        include_classID = hasattr(self, 'class_ID') and self.class_ID is not None and class_ID
        # Check if metadata is present
        include_metadata = hasattr(self, 'metadata') and self.metadata is not None

        if include_metadata:
            metadata_str = ''
            for key, items in self.metadata.items():
                metadata_str += f'{key}={json.dumps(items)}  '

        # Build the extended XYZ header, placing each requested property.
        # We add a 'metadata="...JSON..."' block if include_metadata is True.
        properties_list = [
            f'Lattice="{" ".join(map(str, self.latticeVectors.flatten()))}"' if include_lattice else '',
            'Properties=' + ':'.join(filter(None, [
                "species:S:1" if include_species else "",
                f"{position_tag}:R:3" if include_position else "",
                f"{forces_tag}:R:3" if include_forces else "",
                f"{charge_tag}:R:1" if include_charge else "",
                f"{magnetization_tag}:R:1" if include_magnetization else "",
                f"{fixed_tag}:I:3" if include_fixed else "",
                f"{classID_tag}:I:1" if include_classID else ""
            ])),
            f'{energy_tag}={self.E}' if include_energy else '',
            f'{pbc_tag}="T T T"' if include_pbc else '',
            f'{time_tag}={self.time}' if include_time else '',
            # Serialize metadata to JSON and place it in the header
            metadata_str if include_metadata else '',
        ]
        # Filter out empty strings, then join them into a single header line
        properties_str = ' '.join(filter(None, properties_list))

        # Prepare each atom's line of data according to requested properties
        atom_lines = []
        for i in range(self.atomCount):
            line_parts = []
            if include_species:
                line_parts.append(f"{self.atomLabelsList[i]}")
            if include_position:
                line_parts.extend(f"{coord:13.10f}" for coord in self.atomPositions[i])
            if include_forces:
                line_parts.extend(f"{force:14.10f}" for force in self.total_force[i])
            if include_charge:
                # If charge is an array, decide how to handle shape; assume single value or last column
                if np.ndim(self.charge) == 1:
                    line_parts.append(f"{self.charge[i]:14.10f}")
                else:
                    line_parts.append(f"{self.charge[i, -1]:14.10f}")
            if include_magnetization:
                # Similarly handle magnetization
                if np.ndim(self.magnetization) == 1:
                    line_parts.append(f"{self.magnetization[i]:14.10f}")
                else:
                    line_parts.append(f"{self.magnetization[i, -1]:14.10f}")
            if include_fixed:
                line_parts.extend(f"{val:2d}" for val in np.array(self.atomicConstraints[i], dtype=np.int32))
            if include_classID:
                # Use -1 if something is missing or out of range
                class_id_val = (self.class_ID[i]
                                if i < len(self.class_ID)
                                else -1)
                line_parts.append(f"{class_id_val}")
            # Combine into one line
            atom_lines.append(" ".join(line_parts))

        # Construct the full XYZ content (atom count, then header line, then atom lines)
        xyz_content = f"{self.atomCount}\n{properties_str}\n" + "\n".join(atom_lines) + "\n"

        # Save to file if requested
        if file_location and save_to_file != 'none':
            with open(file_location, save_to_file) as f:
                f.write(xyz_content)
            if verbose:
                print(f"XYZ content saved to {file_location}")

        return xyz_content

    def read_XYZ(self, file_location: Optional[str] = None, lines: Optional[List[str]] = None,
                 verbose: bool = False, tags: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Reads and parses data from an extended XYZ configuration file.

        This method also attempts to deserialize the 'metadata' JSON (if present in the header)
        back into self.metadata.

        Parameters:
            file_location (str, optional): Location of the XYZ file to read.
            lines (list, optional): List of lines from the file to be read directly if provided.
            verbose (bool, optional): Enables detailed logging if set to True.
            tags (dict, optional): Dictionary of tags for backward compatibility (not used here).
            **kwargs: Additional keyword arguments for backward compatibility.

        Returns:
            dict: Parsed data including positions, atom count, species, forces, charge, magnetization,
                  lattice vectors, energy, and pbc. Also updates self.metadata if present.
        """
        file_location = file_location or self.file_location
        if not lines and not file_location:
            raise ValueError("Either 'lines' or 'file_location' must be provided.")

        # If lines not provided, read from file
        lines = lines or list(self.read_file(file_location, strip=False))

        if len(lines) < 2:
            raise ValueError("File must contain at least 2 lines (atom count and at least one header line).")

        # First line: number of atoms
        self.atomCount = int(lines[0].strip())
        if self.atomCount <= 0:
            raise ValueError(f"Invalid number of atoms: {self.atomCount}")

        # Second line: parse extended XYZ header
        self._parse_header(lines[1])

        # Remaining lines: parse atomic data
        self._parse_atom_data(lines[2:])

        return {
            'position': self.atomPositions,
            'atomCount': self.atomCount,
            'species': self.atomLabelsList,
            'forces': self.total_force,
            'charge': self.charge,
            'magnetization': self.magnetization,
            'latticeVectors': self.latticeVectors,
            'energy': self.E,
            'pbc': self.pbc,
            'metadata': self.metadata
        }

    def _parse_header(self, header_line: str) -> None:
        """
        Parses the header line of the extended XYZ format, extracting information such as
        Lattice, Properties, energy, pbc, and metadata (if present).
        """
        # Use a regex to find key=value pairs. Values may be in quotes or unquoted.
        header_parts = re.findall(r'(\w+)=("[^"]+"|[^\s]+)', header_line)

        for key, value in header_parts:
            if key == 'Lattice':
                # Convert the flattened numeric string into a 3x3 numpy array
                self.latticeVectors = np.array(list(map(float, value.strip('"').split()))).reshape(3, 3)
            elif key == 'Properties':
                # This sets self.property_info so we know how many columns each property occupies
                self._parse_properties(value.strip('"'))
            elif key == 'energy':
                self.E = float(value)
            elif key == 'pbc':
                # Expecting strings like "T T T" to indicate True/False for each dimension
                self.pbc = [v.lower() == 't' for v in value.strip('"').split()]
            elif key == 'metadata':
                # Attempt to parse JSON back into a Python object
                self.metadata = json.loads(value.strip('"'))
            else:
                # If we have other custom keys, store them in an info dictionary
                if not hasattr(self, 'info_system'):
                    self.info_system = {}
                self.info_system[key] = value

    def _parse_properties(self, properties_str: str) -> None:
        """
        Parses the 'Properties=' definition to understand the data columns that follow
        in the atomic section.

        E.g., a string like: species:S:1:pos:R:3:forces:R:3
        tells us that the columns are:

            1) species (string)  # 1 column
            2) pos (real)        # 3 columns
            3) forces (real)     # 3 columns
        """
        self.property_info = []
        parts = properties_str.split(':')
        for i in range(0, len(parts), 3):
            name, dtype, ncols = parts[i:i+3]
            self.property_info.append((name, dtype, int(ncols)))

    def _parse_atom_data(self, atom_lines: List[str]) -> None:
        """
        Parses the per-atom data lines according to the structure defined
        in self.property_info from the header line.

        Parameters:
            atom_lines (List[str]): The lines following the header in the extended XYZ file.
        """
        # Split each line by whitespace and form a 2D array
        clean_lines = [line.strip() for line in atom_lines if line.strip()]
        data = np.array([line.split() for line in clean_lines])

        if len(data) != self.atomCount:
            raise ValueError(f"Number of data lines ({len(data)}) does not match atomCount ({self.atomCount})")

        col_index = 0
        for name, dtype, ncols in self.property_info:
            end_index = col_index + ncols
            if end_index > data.shape[1]:
                raise ValueError(f"Not enough columns in data for property '{name}'")

            if dtype == 'S':
                # String columns
                setattr(self, name, data[:, col_index])
            elif dtype == 'R':
                # Float columns
                setattr(self, name, data[:, col_index:end_index].astype(float))
            elif dtype == 'I':
                # Integer columns
                if ncols == 1:
                    setattr(self, name, data[:, col_index].astype(int))
                else:
                    setattr(self, name, data[:, col_index:end_index].astype(int))
            col_index = end_index

        # Assign aliases to known property names
        self.atomLabelsList = getattr(self, 'species', None)
        self.atomPositions = getattr(self, 'pos', None)
        self.total_force = getattr(self, 'forces', None)
        self.charge = getattr(self, 'charge', None)
        self.magnetization = getattr(self, 'magnetization', None)

    @staticmethod
    def read_file(file_location: str, strip: bool = True) -> List[str]:
        """
        Reads the content of a file and returns its lines.

        Parameters:
            file_location (str): The location of the file to read.
            strip (bool): If True, strips whitespace from each line.

        Returns:
            List[str]: All lines from the file.
        """
        with open(file_location, 'r') as f:
            if strip:
                return [line.strip() for line in f]
            else:
                return [line for line in f]
