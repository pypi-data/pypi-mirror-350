try:
    from .structural_file_readers.CIF import CIF
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.CIF: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.PDB import PDB
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.PDB: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.POSCAR import POSCAR
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.POSCAR: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.XYZ import XYZ
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.XYZ: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.SI import SI
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.SI: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.ASE import ASE
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.ASE: {str(e)}\n")
    del sys
    
try:
    from .structural_file_readers.AIMS import AIMS
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.AIMS: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.GEN import GEN
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.GEN: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.DUMP import DUMP
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.DUMP: {str(e)}\n")
    del sys

try:
    from .structural_file_readers.LAMMPS import LAMMPS
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.IO.structure_handling_tools.structural_file_readers.LAMMPS: {str(e)}\n")
    del sys

class AtomPositionLoader(POSCAR, CIF,  XYZ, SI, PDB, ASE, AIMS, GEN, DUMP, LAMMPS):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        POSCAR.__init__(self, name=name, file_location=file_location)
        CIF.__init__(self, name=name, file_location=file_location)
        
        XYZ.__init__(self, name=name, file_location=file_location)
        SI.__init__(self, name=name, file_location=file_location)
        PDB.__init__(self, name=name, file_location=file_location)
        ASE.__init__(self, name=name, file_location=file_location)
        AIMS.__init__(self, name=name, file_location=file_location)
        GEN.__init__(self, name=name, file_location=file_location)

        self._comment = None
        self._atomCount = None  # N total number of atoms

        self.export_dict = {
                            'CIF': 'export_as_AIMS',
                            'POSCAR': 'export_as_POSCAR',
                            'XYZ': 'export_as_XYZ',
                            'SI': 'export_as_SI',
                            'PDB': 'export_as_PDB',
                            'ASE': 'export_as_ASE',
                            'AIMS': 'export_as_AIMS',
                            'GEN': 'export_as_GEN',
                            'DUMP': 'export_as_DUMP',
                            'LAMMPS': 'export_as_LAMMPS',
                            }

        self.import_dict = {
                            'CIF': 'read_AIMS',
                            'POSCAR': 'read_POSCAR',
                            'XYZ': 'read_XYZ',
                            'SI': 'read_SI',
                            'PDB': 'read_PDB',
                            'ASE': 'read_ASE',
                            'AIMS': 'read_AIMS',
                            'GEN': 'read_GEN',
                            'DUMP': 'read_DUMP',
                            'LAMMPS': 'read_LAMMPS',
                            }

                            
    def read(self, source:str='VASP', file_location:str=None):
        metodo = getattr(self, self.import_dict[source.upper()], None)
        if callable(metodo):
            metodo(file_location)
        else:
            print(f"Metodo '{self.import_dict[source.upper()]}' no encontrado.")
            print(f"Read type {source} FAIL")

    def export(self, source:str='VASP', file_location:str=None):
        metodo = getattr(self, self.export_dict[source.upper()], None)
        if callable(metodo):
            metodo(file_location)
        else:
            print(f"Metodo '{self.export_dict[source.upper()]}' no encontrado.")
            print(f"Export type {source} FAIL")
  
'''
a = AtomPositionLoader('/home/akaris/Documents/code/Physics/VASP/v6.2/files/dataset/CoFeNiOOH_jingzhu/bulk_NiFe/POSCAR')
a.read_POSCAR()
#print(AtomPositionLoader.__mro__)
'''