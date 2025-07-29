import typing
from .utils import SingletonMeta as SingletonMeta
from Server.FlowManager import Flow as Flow

class MolstarAPI(metaclass=SingletonMeta):
    """
    API for interacting with Mol* visualizer inside Horus
    """
    @property
    def mvs(self):
        """
        The molviewspec library. Use it to build complex scenes
        """
    def addMolecule(self, filePath: str, label: typing.Optional[str] = None) -> None:
        """
        Adds the given Molecule file to Mol*

        :param filePath: The path to the molecule file
        :param label: The label for the molecule. Optional. Defaults to the filename
        """
    def loadTrajectory(self, topology: str, trajectory: str, label: typing.Optional[str] = None) -> None:
        """
        Adds the given trajectory file to Mol*

        :param topology: The path to the topology file
        :param trajectory: The path to the trajectory file
        :param label: The label for the trajectory. Optional. Defaults to the filename
        """
    def loadMVJS(self, mvjs: typing.Dict[str, typing.Any], replaceExisting: bool = False) -> None:
        """
        Loads a molviewspec session into Mol*

        :param mvjs: The molviewspec session to load as a dictionary
        (returned by the .get_state() method of molviewspec builder)
        :param replaceExisting: Whether to replace the existing session or not
        """
    def focusResidue(self, residue: int, structureLabel: typing.Optional[str] = None, chain: typing.Optional[str] = None, nearRadius: int = 5) -> None:
        """
        Focuses on the given residue

        :param residue: The sequence number of the residue to focus
        :param structureLabel: The label of the structure to focus
        :param chain: The chain ID of the residue to focus
        :param nearRadius: The radius around the residue to display nearby residues
        """
    def addSphere(self, x: float, y: float, z: float, radius: float, color: typing.Optional[str] = None, opacity: float = 1) -> None:
        """
        Adds a sphere to the scene.

        :param x: The x coordinate of the sphere in Angstroms
        :param y: The y coordinate of the sphere in Angstroms
        :param z: The z coordinate of the sphere in Angstroms
        :param radius: The radius of the sphere in Angstroms
        :param color: The color of the sphere as an RGB hex string (i.e. #0000FF)
        :param opacity: The opacity of the sphere (0.0 - 1.0)
        """
    def addBox(self, center: list[float], sides: typing.Optional[list[float]] = None, lineSize: float = 1, color: typing.Optional[str] = None, opacity: float = 1) -> None:
        """
        Adds a box to the scene.

        :param center: The x, y and z coordinates of the center of the box as a list of [x, y ,z]
        :param sides: The a, b and c lengths of the box as a list of [a, b ,c].
        Defaults to [1, 1, 1]
        :param lineSize: The width of the lines. Defaults to 1.
        :param color: The color of the box as an RGB hex string (i.e. #0000FF)
        Defaults to random color.
        :param opacity: The opacity of the box (0.0 - 1.0). Defaults to 1.
        """
    def setBackgroundColor(self, color: str) -> None:
        """
        Sets the background color of the scene

        :param color: The color to set the background to as an RGB hex string (i.e. #0000FF)
        """
    def setSpin(self, speed: float = 1) -> None:
        """
        Sets the spin of the molecule.

        :param speed: The rotation speed. Defaults to 1. To stop it, set the speed to 0
        """
    def reset(self) -> None:
        """
        Resets the visualizer
        """
