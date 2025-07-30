# sh3d.py

Python library for reading Sweet Home 3D file format (*.sh3d). Internally sh3d is just another zip archive with JavaObject dump (as Home) and XML dump (as Home.xml) and attached files, this library supports reading them all and provides corresponding python objects representing sh3d data.

## Install

```bash
pip install sh3d.py
```

## Usage

### Loading full data from Home JavaObject dump

```python
from sh3d.FileLoader import FileLoader, HomeSource


# Default is parsion of JavaObject Home
with FileLoader('myHome.sh3d') as file_loader:
    
    # Dump home, ~all models are dataclasses so you will actually see full readable dump
    print(file_loader.home)

# Load home from Home.xml instead
with FileLoader('myHome.sh3d', home_source=HomeSource.XML) as file_loader:
    
    # Dump home, ~all models are dataclasses so you will actually see full readable dump
    print(file_loader.home)  # Home object
```

## Home object structure

```python
class Home:
    name: str 
    version: int
    wall_height: float
    levels: List[Level]  # Implemented, represents list of Home plan levels
    furniture: List[HomePieceOfFurniture]  # Implemented, represents list of furniture including doors and windows as HomeDoorOrWindow object that is child of HomePieceOfFurniture
    rooms: List[Room]  # Implemented, represents list of rooms
    walls: List[Wall]  # Implemented, represents list of walls
    dimension_lines: List[DimensionLine]  # Implemented, represents list of dimension lines (measurements)
    labels: List[Label] # Implemented, represents list of labels (texts)
    polylines: List[Polyline]  # Implemented, represents list of polylines 
    background_image: BackgroundImage # Implemented, represents background image
    environment: HomeEnvironment  # Implemented, represents home environment / config
    compass: Compass  # Implemented
    
```









