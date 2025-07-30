from pathlib import Path
from sh3d.FileLoader import FileLoader, HomeSource
from sh3d.model.Home import Home


def test_can_init(sh3d_path: Path) -> None:
    with FileLoader(sh3d_path) as file_loader:
        assert isinstance(file_loader.home, Home)

def test_can_init_path_str(sh3d_path: Path) -> None:
    with FileLoader(str(sh3d_path)) as file_loader:
        assert isinstance(file_loader.home, Home)

def test_can_init_custom_resources(sh3d_path: Path, resources_path: Path) -> None:
    with FileLoader(sh3d_path, resources_path) as file_loader:
        assert isinstance(file_loader.home, Home)

def test_can_init_custom_resources_str(sh3d_path: Path, resources_path: Path) -> None:
    with FileLoader(sh3d_path, str(resources_path)) as file_loader:
        assert isinstance(file_loader.home, Home)

def test_can_init_xml(sh3d_path: Path) -> None:
    with FileLoader(sh3d_path, home_source=HomeSource.XML) as file_loader:
        assert isinstance(file_loader.home, Home)