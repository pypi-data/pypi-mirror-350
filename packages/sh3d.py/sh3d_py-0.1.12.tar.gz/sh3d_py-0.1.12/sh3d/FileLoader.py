import enum
from importlib.resources import files
from pathlib import Path
from types import TracebackType
from typing import Optional,  Union, Type
import zipfile
import xmltodict
import javaobj

from sh3d.AssetManager import AssetManager
from sh3d.model.Home import Home

@enum.unique
class HomeSource(enum.Enum):
    JAVAOBJ = 'JAVAOBJ'
    XML = 'XML'

class FileLoader:
    home_source: HomeSource
    def __init__(
            self,
            sh3d_path: Union[Path, str],
            resources_path: Optional[Union[Path, str]] = None,
            home_source: HomeSource = HomeSource.JAVAOBJ
    ):
        if isinstance(sh3d_path, str):
            sh3d_path = Path(sh3d_path)

        if isinstance(resources_path, str):
            resources_path = Path(resources_path)

        if not resources_path:
            # Load package provided resources
            resources_path = Path(str(files("sh3d").joinpath("resources")))

        self.asset_manager = AssetManager(resources_path)
        self.zip_file = zipfile.ZipFile(sh3d_path, 'r')  # pylint: disable=consider-using-with
        self.home_source = home_source

    @property
    def home(self) -> Home:
        self.asset_manager.load_assets(self.zip_file)
        return self._load_home()

    def _load_home(self) -> Home:
        if self.home_source == HomeSource.XML:
            data = xmltodict.parse(self.zip_file.read('Home.xml'))
            return Home.from_xml_dict(data.get('home'), self.asset_manager)

        data = javaobj.loads(self.zip_file.read('Home'))
        return Home.from_javaobj(data, self.asset_manager)

    def __enter__(self) -> 'FileLoader':
        return self

    def close(self) -> None:
        self.zip_file.close()

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.close()
