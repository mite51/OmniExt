import carb
import omni.ext
import omni.ui as ui
from pathlib import Path

# omni.kit.pipapi extension is required
import omni.kit.pipapi
_pip_packages = [
    ["torch"],
    ["torchvision"],
    ["opencv-python"],
    ["pyglet", "2.0.15"],
    #["huggingface-hub[torch]","0.23.2"],
]

for _pip_package in _pip_packages:
    if len(_pip_package) == 2:
        carb.log_error(f"pipapi.install {_pip_package[0]} version={_pip_package[1]}")
        omni.kit.pipapi.install(package=_pip_package[0], version={_pip_package[1]})
    else:
        carb.log_error(f"pipapi.install {_pip_package[0]}")
        omni.kit.pipapi.install(package=_pip_package[0])          


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[wylie] some_public_function was called with x: ", x)
    return x ** x


ICON_PATH = Path(__file__).parent.parent.joinpath("icons")
LABEL_PADDING = 120

def _create_path_combo(name, paths):
    with ui.HStack():
        ui.Label(name, name="label", width=LABEL_PADDING)
        with ui.ZStack():
            ui.StringField(name="models").model.set_value(paths)
            with ui.HStack():
                ui.Spacer()
                ui.Circle(width=10, height=20, style={"background_color": 0xFF555555})
        ui.ComboBox(0, paths, paths, name="path", width=0, height=0, arrow_only=True)
        ui.Spacer(width=5)
        ui.Image("resources/icons/folder.png", width=15)
        ui.Spacer(width=5)
        ui.Image("resources/icons/find.png", width=15)
        _create_control_state(2)

def _create_control_state(state=0):
    control_type = [
        f"{ICON_PATH}/Expression.svg",
        f"{ICON_PATH}/Mute Channel.svg",
        f"{ICON_PATH}/mixed properties.svg",
        f"{ICON_PATH}/Default value.svg",
        f"{ICON_PATH}/Changed value.svg",
        f"{ICON_PATH}/Animation Curve.svg",
        f"{ICON_PATH}/Animation Key.svg",
    ]

    if state == 0:
        ui.Circle(name="transform", width=20, radius=3.5, size_policy=ui.CircleSizePolicy.FIXED)
    else:
        with ui.VStack(width=0):
            ui.Spacer()
            ui.Image(control_type[state - 1], width=20, height=12)
            ui.Spacer()        

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
#class WylieExtension(omni.ext.IExt):
class wylie(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        carb.log_warn("[wylie] startup")

        self._count = 0

        self._window = ui.Window("My Window", width=600, height=300)
        with self._window.frame:
            with ui.VStack():#style={"Button": {"height":ui.Length(10), "background_color": ui.color("#097e00")}}):
                self._label = ui.Label("Dust3r", height=32)
                #ui.Label(f"{dir(torch)}", height=32)
                                
                def on_click():
                    import torch
                    import torchvision
                    import cv2
                    import pyglet
                    import huggingface_hub
                    import dust3r.dust3r

                    version_number = torch.__version__.split("+")[0]
                    cuda_is_available = torch.cuda.is_available()
                    print(f"*** torch version = {version_number} {cuda_is_available}")
                    #print(dir(torchvision))
                    #print(dir(cv2))
                    #print(dir(pyglet))
                    #print(dir(huggingface_hub))
                    


                def on_reset():
                    pass

                with ui.VStack(height=24):    
                    _create_path_combo("Texture Path", "omni:/Project/cool_texture.png")
                ui.Button("Add", clicked_fn=on_click, height=32)
                ui.Button("Reset", clicked_fn=on_reset, height=32)


    def on_shutdown(self):
        carb.log_warn("[wylie] shutdown")



"""
from pxr import Sdf
stage = omni.usd.get_context().get_stage()
#print(dir(Sdf.ValueTypeNames))
prim = stage.DefinePrim("/PointCloud/pointData/pointcloud_2", "Points")
attr = prim.CreateAttribute("points", Sdf.ValueTypeNames.Float3Array)
value = []
for i in range(100):
	value.append((0,0,i * 0.02))
	attr.Set(value )

"""