import os
import PIL
from pathlib import Path
from pillow_lut import load_cube_file


class LUT(object):
    def __init__(self, name):
        if name is None:
            self._name = "None"
            self._description = "None"
            self._lut_file_path = None
            return
        if os.path.exists(name) and os.path.isfile(name):
            p = Path(name)
            self._name = p.stem
            self._description = "from file {p.name}"
            self._lut_file_path = name
        else:
            self._name = name
            self._description = f"this is lut {self._name}"
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self._lut_file_path = os.path.join(base_dir, 'luts', f'{name}.cube')

    @property
    def Color3DLUT(self) -> PIL.ImageFilter.Color3DLUT:
        return load_cube_file(self._lut_file_path)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def __str__(self):
        return f"{self._name}:{self._description}"

def get_adjust_param_by_lut_name(lut_name, file_type):
    """
    亮度、对比对、饱和度
    """
    data = {
        'nc':       { 'ARW':(1.0, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
        'cn':       { 'ARW':(1.0, 1.0, 1.0), 'JPG':(0.8, 1.0, 1.0), },
        'cc':       { 'ARW':(1.0, 1.0, 1.0), 'JPG':(0.8, 1.0, 1.0), },
        'land':     { 'ARW':(1.5, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
        'lenox':    { 'ARW':(1.5, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
        'sea':      { 'ARW':(1.5, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
        'topaz':    { 'ARW':(1.5, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
        'azrael':   { 'ARW':(1.5, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
        'byers':    { 'ARW':(1.5, 1.0, 1.0), 'JPG':(1.0, 1.0, 1.0) },
    }
    try:
        return data[lut_name][file_type]
    except Exception as e:
        print(f"not adapter parameter for {lut_name} {file_type}")
        return (1.0, 1.0, 1.0)

def get_adjust_by_lut_name(file_name, lut_name):
    if file_name.split('.')[-1] == 'ARW':
        return get_adjust_param_by_lut_name(lut_name, 'ARW')
    else:
        return get_adjust_param_by_lut_name(lut_name, 'JPG')

def get_all_luts()->list:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    luts_dir = os.path.join(base_dir, 'luts')
    luts = []
    for f in Path(luts_dir).rglob('*.cube'):
        if f.is_file():
            luts.append(LUT(f.stem))
    return luts
