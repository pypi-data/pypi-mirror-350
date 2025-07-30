try:
    from ..master.FileManager import FileManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing FileManager: {str(e)}\n")
    del sys

try:
    from ..master.AtomicProperties import AtomicProperties
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomicProperties: {str(e)}\n")
    del sys

try:
    from ..IO.KPointsManager import KPointsManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing KPointsManager: {str(e)}\n")
    del sys

try:
    from ..IO.input_handling_tools.InputFile import InputFile
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing InputFile: {str(e)}\n")
    del sys

try: 
    from ..IO.PotentialManager import PotentialManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PotentialManager: {str(e)}\n")
    del sys

try:
    from ..IO.structure_handling_tools.AtomPosition import AtomPosition
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomPosition: {str(e)}\n")
    del sys

try:
    import re
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing re: {str(e)}\n")
    del sys

try:
    import copy
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing copy: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

from typing import Dict

class OutFileManager(FileManager, AtomicProperties):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initializes the OutFileManager class, which manages the reading and processing of VASP OUTCAR files.

        Inherits from FileManager and AtomicProperties classes to utilize their functionalities.

        Parameters:
        file_location (str, optional): The path to the OUTCAR file.
        name (str, optional): A name identifier for the file.
        kwargs: Additional keyword arguments for extended functionality.
        """
        FileManager.__init__(self, name=name, file_location=file_location)
        
        # Initialize AtomicProperties
        AtomicProperties.__init__(self)

        self._comment = None  # Placeholder for comments within the file
        self._InputFileManager = InputFile(self.file_location)  # Manage the associated input file
        self._KPointsManager = KPointsManager(self.file_location)  # Manage KPoints data
        self._AtomPositionManager = []  # List to store atom position data
        self._PotentialManager = PotentialManager(self.file_location)  # Manage potential data
        
        # Dictionary to store parameters extracted from the OUTCAR file
        self._parameters = {}
        # List of recognized parameter names for parsing the OUTCAR file
        self._parameters_data = ['SYSTEM', 'POSCAR', 'Startparameter for this run:', 'NWRITE', 'PREC', 'ISTART', 
                                'ICHARG', 'ISPIN', 'LNONCOLLINEAR', 'LSORBIT', 'INIWAV', 'LASPH', 'METAGGA', 
                                'Electronic Relaxation 1', 'ENCUT', 'ENINI', 'ENAUG', 'NELM', 'EDIFF', 'LREAL', 
                                'NLSPLINE', 'LCOMPAT', 'GGA_COMPAT', 'LMAXPAW', 'LMAXMIX', 'VOSKOWN', 'ROPT', 
                                'ROPT', 'Ionic relaxation', 'EDIFFG', 'NSW', 'NBLOCK', 'IBRION', 'NFREE', 'ISIF',
                                'IWAVPR', 'ISYM', 'LCORR', 'POTIM', 'TEIN', 'TEBEG', 'SMASS', 'estimated Nose-frequenzy (Omega)', 
                                'SCALEE', 'NPACO', 'PSTRESS', 'Mass of Ions in am', 'POMASS', 'Ionic Valenz', 
                                'ZVAL', 'Atomic Wigner-Seitz radii', 'RWIGS', 'virtual crystal weights', 'VCA', 
                                'NELECT', 'NUPDOWN', 'DOS related values:', 'EMIN', 'EFERMI', 'ISMEAR', 
                                'Electronic relaxation 2 (details)', 'IALGO', 'LDIAG', 'LSUBROT', 'TURBO', 
                                'IRESTART', 'NREBOOT', 'NMIN', 'EREF', 'IMIX', 'AMIX', 'AMIX_MAG', 'AMIN', 'WC', 
                                'Intra band minimization:', 'WEIMIN', 'EBREAK', 'DEPER', 'TIME', 'volume/ion in A,a.u.', 
                                'Fermi-wavevector in a.u.,A,eV,Ry', 'Thomas-Fermi vector in A', 'Write flags', 
                                'LWAVE', 'LCHARG', 'LVTOT', 'LVHAR', 'LELF', 'LORBIT', 'Dipole corrections', 
                                'LMONO', 'LDIPOL', 'IDIPOL', 'EPSILON', 'Exchange correlation treatment:', 'GGA', 
                                'LEXCH', 'VOSKOWN', 'LHFCALC', 'LHFONE', 'AEXX', 'Linear response parameters', 
                                'LEPSILON', 'LRPA', 'LNABLA', 'LVEL', 'LINTERFAST', 'KINTER', 'CSHIFT', 'OMEGAMAX', 
                                'DEG_THRESHOLD', 'RTIME', 'Orbital magnetization related:', 'ORBITALMAG', 'LCHIMAG', 'TITEL', 
                                'DQ','type', 'uniqueAtomLabels', 'NIONS', 'atomCountByType']

        self._dynamical_eigenvalues = None  # IR positions for a finite diference avaluation. Type: FxNx3

        self._dynamical_eigenvector = None  # IR positions for a finite diference avaluation. Type: FxNx3
        self._dynamical_eigenvector_fractional = None  # IR displacement. Type: np.array or None

        self._dynamical_eigenvector_diff = None  # IR positions for a finite diference avaluation. Type: FxNx3
        self._dynamical_eigenvector_diff_fractional = None  # IR displacement. Type: np.array or None

    @property
    def dynamical_eigenvalues(self):
        """

        """
        if isinstance(self._dynamical_eigenvalues, list):
            self._dynamical_eigenvalues = np.array(self._dynamical_eigenvalues, dtype=np.float64)
            return self._dynamical_eigenvalues
        else:
            return self._dynamical_eigenvalues

    @property
    def dynamical_eigenvector(self):
        """

        """
        if isinstance(self._dynamical_eigenvector, list):
            self._dynamical_eigenvector = np.array(self._dynamical_eigenvector, dtype=np.float64)
            return self._dynamical_eigenvector
        else:
            return self._dynamical_eigenvector

    @property
    def dynamical_eigenvector_diff(self):
        """

        """
        if isinstance(self._dynamical_eigenvector_diff, list):
            self._dynamical_eigenvector_diff = np.array(self._dynamical_eigenvector_diff, dtype=np.float64)
            return self._dynamical_eigenvector_diff
        else:
            return self._dynamical_eigenvector_diff

    def _extract_variables(self, value):
        """
        Extracts variables from a string, recognizing and converting T/F to True/False, 
        and handles numerical and string values accordingly.

        Parameters:
        value (str): The string from which variables are to be extracted.

        Returns:
        str or list: A single processed value or a list of processed values.
        """
        tokens = re.split(r'[ \t]+', value.strip())  # Split the value into tokens by whitespace
        processed = []  # List to hold processed tokens
        
        for i, t in enumerate(tokens):
            # Convert T/F to True/False, numbers to numeric types, and keep strings as is
            token_value = 'True' if t == 'T' else 'False' if t == 'F' else str(t) if self.is_number(t) else t
            # Break loop if a non-numeric token is encountered after the first token
            if i > 0 and not self.is_number(t): 
                break
            processed.append(token_value)

        # Join the processed tokens into a string if there are multiple, otherwise return the single token
        return ' '.join(processed) if len(processed) > 1 else processed[0]

    def readOUTCAR(self, file_location: str = None, **kwargs):
        """
        Parses the OUTCAR file from a VASP simulation to extract various parameters and atom positions.

        This method processes the OUTCAR file line by line, extracting parameters like Fermi energy, 
        dispersion energy, lattice vectors, charges, magnetizations, total forces, and atom positions. 
        The information is stored in an AtomPosition object.

        Parameters:
        file_location (str, optional): The path to the OUTCAR file. If not specified, 
                                       uses the instance's default file location.

        Returns:
        None: The method updates the instance's _AtomPositionManager with the parsed data.
        """

        def _extract_parameter(APM_attribute, initial_j, columns_slice=slice(1, None)):
            """
            Extracts numerical data from the lines and adds them to the AtomPosition object.

            Parameters:
            APM_attribute (str): The attribute of the AtomPosition object to update.
            initial_j (int): The initial line offset from the current line to start reading data.
            columns_slice (slice, optional): The slice of columns to be extracted from each line.

            Returns:
            AtomPosition: The updated AtomPosition object.
            """
            j = initial_j
            data = []
            while True:
                if not lines[i + j].strip():break
                try:
                    data.append( list(map(float, lines[i + j].split()))[columns_slice] )
                    j += 1
                except:
                    break

            if isinstance(APM_attribute, str):
                setattr(APM, APM_attribute, np.array(data) )
    
            return data

        file_location = file_location if type(file_location) == str else self.file_location
        lines =list(self.read_file(file_location,strip=False))
        
        # Make frequently used methods local
        local_strip = str.strip
        local_split = str.split

        read_parameters = True
        APM_holder = []
        APM = None 
        uniqueAtomLabels = []

        # Precompile regular expressions for faster matching
        param_re = re.compile(r"(\w+)\s*=\s*([^=]+)(?:\s+|$)")
        keyword_re = re.compile(r'E-fermi|POTCAR|total charge|magnetization|TOTAL-FORCE|energy  without entropy=|Edisp|Ionic step|direct lattice vectors|2PiTHz')
        keyword_ion = re.compile(r'E-Ionic step|Iteration')

        for i, line in enumerate(lines):
            stripped_line = line.strip()
            line_vec = [x for x in line.strip().split(' ') if x]
            
            if read_parameters:
                # Extracting parameters from the initial section of the file
                if keyword_ion.search(line):
                    # Switch off parameter reading after encountering ionic step
                    read_parameters = False
                    # Store unique atom labels and atom count by type
                    self.parameters['uniqueAtomLabels'] = uniqueAtomLabels[:len(uniqueAtomLabels)//2]
                    self.parameters['atomCountByType'] = self.parameters['type']
                    APM = AtomPosition()
                    APM._atomCount = self.parameters['NIONS']
                    APM._uniqueAtomLabels = self.parameters.get('uniqueAtomLabels')
                    APM._atomCountByType = [ int(n) for n in self.parameters.get('atomCountByType').split(' ') ]

                elif 'POTCAR:' in line:
                    # Extracting unique atom labels from POTCAR line
                    uniqueAtomLabels.append( list(set(re.split(r'[ _]', line)).intersection(self.atomic_id))[0] )
                elif 'NIONS' in line:
                    # Extracting total number of ions
                    self.parameters['NIONS'] = int(line_vec[11])

                else:
                    # General parameter extraction
                    for key, value in re.findall(param_re, line.strip()):
                        self._update_parameters(key, self._extract_variables(value))
  
            elif keyword_re.search(line):  # Searching for specific keywords in the line
                    
                if 'Ionic step' in line:
                    # Storing the current APM object and creating a new one for the next ionic step
                    APM_holder.append(APM)
                    APM = AtomPosition()
                    
                    APM._atomCount = self.parameters['NIONS']
                    APM._uniqueAtomLabels = self.parameters.get('uniqueAtomLabels')
                    APM._atomCountByType = [ int(n) for n in self.parameters.get('atomCountByType').split(' ') ]

                elif 'E-fermi' in line:
                    # Extracting Fermi energy
                    APM._E_fermi = float(line_vec[2])
                elif 'Edisp' in line:
                    # Extracting dispersion energy
                    APM._Edisp = float(line_vec[-1][:-1])
                elif 'energy  without entropy=' in line:
                    # Extracting energy without entropy
                    APM._E = float(line_vec[-1])
                elif 'direct lattice vectors' in line: 
                    # Extracting lattice vectors
                    _extract_parameter('_latticeVectors', 1, slice(0, 3))
                    
                elif 'total charge' in line and 'charge-density' not in line: 
                    # Extracting total charge
                    _extract_parameter('_charge', 4, slice(1, None))

                elif 'magnetization (x)' in line: 
                    # Extracting magnetization
                    _extract_parameter('_magnetization', 4, slice(1, None))

                elif 'TOTAL-FORCE' in line: 
                    # Extracting total forces and atom positions
                    _extract_parameter('_total_force', 2, slice(3, None))
                    _extract_parameter('_atomPositions', 2, slice(0, 3))

                elif '2PiTHz' in line: 

                    if not hasattr(self, '_dynamical_eigenvalues') or not isinstance(self._dynamical_eigenvalues, list):
                        setattr(self, '_dynamical_eigenvalues', [re.findall(r'\d+\.\d+', line)])
                    else:
                        self._dynamical_eigenvalues.append( re.findall(r'\d+\.\d+', line) )

                    if not hasattr(self, '_dynamical_eigenvector') or not isinstance(self._dynamical_eigenvector, list):
                        setattr(self, '_dynamical_eigenvector', [_extract_parameter(None, 2, slice(0, 3))])
                    else:
                        self._dynamical_eigenvector.append( _extract_parameter(None, 2, slice(0, 3)) )

                    if not hasattr(self, '_dynamical_eigenvector_diff') or not isinstance(self._dynamical_eigenvector_diff, list):
                        setattr(self, '_dynamical_eigenvector_diff', [_extract_parameter(None, 2, slice(3, None))] )
                    else:
                        self._dynamical_eigenvector_diff.append( _extract_parameter(None, 2, slice(3, None)) ) 

        # Append the final APM object if it exists and is not already in APM_holder
        if isinstance(APM, AtomPosition): #and not APM in APM_holder: 
            APM_holder.append(APM)

        # Updating the instance's AtomPositionManager with the extracted data
        self._AtomPositionManager = APM_holder

    def _update_parameters(self, var_name, value):
        """
        Updates parameter values in the current instance and its associated InputFileManager.

        This method is used to update the parameters dictionary of the current instance and 
        its InputFileManager with new values based on the variable name.

        Parameters:
        var_name (str): The name of the parameter to be updated.
        value: The new value to be set for the parameter.
        """
        # Update parameter in current instance if var_name is recognized
        if var_name in self.parameters_data:
            self.parameters[var_name] = value

        # Update parameter in InputFileManager if var_name is recognized
        if var_name in self._InputFileManager.parameters_data:
            self._InputFileManager.parameters[var_name] = value

    def _handle_regex_matches(self, line_vec, line):
        """
        Handles the parsing of specific lines based on regular expression matches.

        This method is responsible for extracting and setting values like Fermi energy, number of ions, 
        POTCAR information, lattice vectors, etc., based on the content of a given line.

        Parameters:
        line_vec (list): The list of words in the current line.
        line (str): The current line being processed.
        """         
        if 'E-fermi' in line:
            # Extract and set Fermi energy
            self.E_fermi = float(line_vec[2])
        elif 'NIONS' in line:
            # Extract and set the number of ions
            self.NIONS = int(line_vec[11])
            self._AtomPositionManager[-1]._atomCount = int(line_vec[11])

        elif 'POTCAR' in line: 
            # Extract and set POTCAR information
            try:    
                if not line.split(':')[1] in self.POTCAR_full:
                    self.POTCAR_full.append(line.split(':')[1])
                if not line.split(':')[1].strip().split(' ')[1] in self.POTCAR:
                    self.POTCAR.append( line.split(':')[1].strip().split(' ')[1] )
            except: pass

        elif 'direct lattice vectors' in line: 
            self._AtomPositionManager[-1]._latticeVectors = np.array((map(float, lines[i + 1 + j].split()[3:])))
            
        # The following block seems incomplete and might need additional implementation
        elif 'total charge' in line and not 'charge-density' in line: 
            TC = self.NIONS+4
            total_charge = np.zeros((self.NIONS,4))
            TC_counter = 0 

    def readDETAILED(self, file_location: str = None) -> None:
        """
        Parses the output of a DFTB+ calculation and extracts relevant information.

        Parameters:
        - file_location (str): The path to the DFTB+ output file.

        Returns:
        - None: The extracted information is stored in the instance variables.
        """
        import re

        # Use the provided file location or the one stored in the instance
        file_location = file_location if file_location is not None else self.file_location

        # Read the file content
        with open(file_location, 'r') as f:
            lines = f.readlines()

        # Initialize data structures
        self.total_charge = None
        self.atomic_gross_charges = []
        self.atomic_net_populations = []
        self.atom_populations_up = []
        self.l_shell_populations_up = []
        self.orbital_populations_up = []
        self.atom_populations_down = []
        self.l_shell_populations_down = []
        self.orbital_populations_down = []
        self.spin_up_energies = {}
        self.spin_down_energies = {}
        self.total_energies = {}
        self.dipole_moment = {}

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if 'Total charge:' in line:
                # Extract total charge
                tokens = line.split()
                self.total_charge = float(tokens[-1])
                i += 1
            elif 'Atomic gross charges (e)' in line:
                # Read atomic gross charges
                i += 2  # Skip header lines
                while i < len(lines) and lines[i].strip():
                    tokens = lines[i].split()
                    if len(tokens) >= 2:
                        self.atomic_gross_charges.append({
                            'Atom': int(tokens[0]),
                            'Charge': float(tokens[1])
                        })
                    i += 1
            elif 'Atomic net (on-site) populations and hybridisation ratios' in line:
                # Read atomic net populations
                i += 2  # Skip header lines
                while i < len(lines) and lines[i].strip():
                    tokens = lines[i].split()
                    if len(tokens) >= 3:
                        self.atomic_net_populations.append({
                            'Atom': int(tokens[0]),
                            'Population': float(tokens[1]),
                            'Hybridisation': float(tokens[2])
                        })
                    i += 1
            elif 'Nr. of electrons (up):' in line:
                # Extract number of electrons (up)
                tokens = line.split()
                self.spin_up_energies['Nr_electrons_up'] = float(tokens[-1])
                i += 1
                # Read atom populations (up)
                if 'Atom populations (up)' in lines[i].strip():
                    i += 2  # Skip header lines
                    while i < len(lines) and lines[i].strip():
                        tokens = lines[i].split()
                        if len(tokens) >= 2:
                            self.atom_populations_up.append({
                                'Atom': int(tokens[0]),
                                'Population': float(tokens[1])
                            })
                        i += 1
                # Read l-shell populations (up)
                while i < len(lines) and 'l-shell populations (up)' not in lines[i]:
                    i += 1
                if i < len(lines):
                    i += 2  # Skip header lines
                    while i < len(lines) and lines[i].strip():
                        tokens = lines[i].split()
                        if len(tokens) >= 4:
                            self.l_shell_populations_up.append({
                                'Atom': int(tokens[0]),
                                'Shell': int(tokens[1]),
                                'l': int(tokens[2]),
                                'Population': float(tokens[3])
                            })
                        i += 1
                # Read orbital populations (up)
                while i < len(lines) and 'Orbital populations (up)' not in lines[i]:
                    i += 1
                if i < len(lines):
                    i += 2  # Skip header lines
                    while i < len(lines) and lines[i].strip():
                        tokens = lines[i].split()
                        if len(tokens) >= 6:
                            self.orbital_populations_up.append({
                                'Atom': int(tokens[0]),
                                'Shell': int(tokens[1]),
                                'l': int(tokens[2]),
                                'm': int(tokens[3]),
                                'Population': float(tokens[4]),
                                'Label': tokens[5]
                            })
                        i += 1
            elif 'Nr. of electrons (down):' in line:
                # Extract number of electrons (down)
                tokens = line.split()
                self.spin_down_energies['Nr_electrons_down'] = float(tokens[-1])
                i += 1
                # Read atom populations (down)
                if 'Atom populations (down)' in lines[i].strip():
                    i += 2  # Skip header lines
                    while i < len(lines) and lines[i].strip():
                        tokens = lines[i].split()
                        if len(tokens) >= 2:
                            self.atom_populations_down.append({
                                'Atom': int(tokens[0]),
                                'Population': float(tokens[1])
                            })
                        i += 1
                # Read l-shell populations (down)
                while i < len(lines) and 'l-shell populations (down)' not in lines[i]:
                    i += 1
                if i < len(lines):
                    i += 2  # Skip header lines
                    while i < len(lines) and lines[i].strip():
                        tokens = lines[i].split()
                        if len(tokens) >= 4:
                            self.l_shell_populations_down.append({
                                'Atom': int(tokens[0]),
                                'Shell': int(tokens[1]),
                                'l': int(tokens[2]),
                                'Population': float(tokens[3])
                            })
                        i += 1
                # Read orbital populations (down)
                while i < len(lines) and 'Orbital populations (down)' not in lines[i]:
                    i += 1
                if i < len(lines):
                    i += 2  # Skip header lines
                    while i < len(lines) and lines[i].strip():
                        tokens = lines[i].split()
                        if len(tokens) >= 6:
                            self.orbital_populations_down.append({
                                'Atom': int(tokens[0]),
                                'Shell': int(tokens[1]),
                                'l': int(tokens[2]),
                                'm': int(tokens[3]),
                                'Population': float(tokens[4]),
                                'Label': tokens[5]
                            })
                        i += 1
            elif 'Spin  up' in line:
                # Read spin up energies
                i += 1
                while i < len(lines) and lines[i].strip():
                    line = lines[i].strip()
                    if 'Fermi level:' in line:
                        tokens = line.split()
                        self.spin_up_energies['Fermi_level_H'] = float(tokens[2])
                        self.spin_up_energies['Fermi_level_eV'] = float(tokens[4].replace('eV', ''))
                    elif 'Band energy:' in line:
                        tokens = line.split()
                        self.spin_up_energies['Band_energy_H'] = float(tokens[2])
                        self.spin_up_energies['Band_energy_eV'] = float(tokens[4].replace('eV', ''))
                    elif 'Input / Output electrons (up):' in line:
                        tokens = line.split()
                        self.spin_up_energies['Input_electrons'] = float(tokens[4])
                        self.spin_up_energies['Output_electrons'] = float(tokens[5])
                    i += 1
            elif 'Spin  down' in line:
                # Read spin down energies
                i += 1
                while i < len(lines) and lines[i].strip():
                    line = lines[i].strip()
                    if 'Fermi level:' in line:
                        tokens = line.split()
                        self.spin_down_energies['Fermi_level_H'] = float(tokens[2])
                        self.spin_down_energies['Fermi_level_eV'] = float(tokens[4].replace('eV', ''))
                    elif 'Band energy:' in line:
                        tokens = line.split()
                        self.spin_down_energies['Band_energy_H'] = float(tokens[2])
                        self.spin_down_energies['Band_energy_eV'] = float(tokens[4].replace('eV', ''))
                    elif 'Input / Output electrons (down):' in line:
                        tokens = line.split()
                        self.spin_down_energies['Input_electrons'] = float(tokens[4])
                        self.spin_down_energies['Output_electrons'] = float(tokens[5])
                    i += 1
            elif 'Energy H0:' in line:
                # Read total energies
                tokens = line.split()
                self.total_energies['Energy_H0_H'] = float(tokens[2])
                self.total_energies['Energy_H0_eV'] = float(tokens[3].replace('eV', ''))
                i += 1
                while i < len(lines) and lines[i].strip():
                    line = lines[i].strip()
                    tokens = line.split()
                    if 'Energy SCC:' in line:
                        self.total_energies['Energy_SCC_H'] = float(tokens[2])
                        self.total_energies['Energy_SCC_eV'] = float(tokens[3].replace('eV', ''))
                    elif 'Energy SPIN:' in line:
                        self.total_energies['Energy_SPIN_H'] = float(tokens[2])
                        self.total_energies['Energy_SPIN_eV'] = float(tokens[3].replace('eV', ''))
                    elif 'Total Electronic energy:' in line:
                        self.total_energies['Total_electronic_energy_H'] = float(tokens[3])
                        self.total_energies['Total_electronic_energy_eV'] = float(tokens[4].replace('eV', ''))
                    elif 'Total energy:' in line:
                        self.total_energies['Total_energy_H'] = float(tokens[2])
                        self.total_energies['Total_energy_eV'] = float(tokens[3].replace('eV', ''))
                    i += 1
            elif 'Dipole moment:' in line:
                # Read dipole moment
                tokens = line.split()
                self.dipole_moment['x_au'] = float(tokens[1])
                self.dipole_moment['y_au'] = float(tokens[2])
                self.dipole_moment['z_au'] = float(tokens[3])
                i += 1
                if i < len(lines) and 'Dipole moment:' in lines[i]:
                    line = lines[i].strip()
                    tokens = line.split()
                    self.dipole_moment['x_debye'] = float(tokens[1])
                    self.dipole_moment['y_debye'] = float(tokens[2])
                    self.dipole_moment['z_debye'] = float(tokens[3])
                i += 1
            else:
                i += 1

