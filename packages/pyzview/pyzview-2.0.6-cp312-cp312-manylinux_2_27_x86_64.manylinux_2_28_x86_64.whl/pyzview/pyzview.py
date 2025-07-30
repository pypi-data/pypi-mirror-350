import pyzview.pyzview_inf
import numpy as np


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Pyzview(metaclass=Singleton):
    @staticmethod
    def _str2rgb(colorstr):
        if (
            isinstance(colorstr, list)
            or isinstance(colorstr, np.ndarray)
            or isinstance(colorstr, tuple)
        ) and len(colorstr) == 3:
            return colorstr
        if colorstr == "r":
            col = [255, 0, 0]
        elif colorstr == "g":
            col = [0, 255, 0]
        elif colorstr == "b":
            col = [0, 0, 255]
        elif colorstr == "c":
            col = [0, 255, 255]
        elif colorstr == "m":
            col = [255, 0, 255]
        elif colorstr == "y":
            col = [255, 255, 0]
        elif colorstr == "w":
            col = [255, 255, 255]
        elif colorstr == "k":
            col = [0, 0, 0]
        elif colorstr == "R":
            col = list(np.random.rand(3) * 255)
        else:
            raise RuntimeError("unknown color name")
        return col

    @staticmethod
    def xyz2xyzrgba(xyz, color, alpha):
        xyz_dim = xyz.shape[1]
        xyzrgba = np.c_[xyz, np.ones((xyz.shape[0], 7 - xyz_dim)) * 255]
        if color is not None:
            xyzrgba[:, 3:6] = Pyzview._str2rgb(color)
        if alpha is not None:
            xyzrgba[:, 6] = alpha
        return xyzrgba

    def connect(self):
        if self.zv is not None:
            return True
        try:
            self.zv = pyzview.pyzview_inf.interface()  # get interface
            return True
        except RuntimeError:
            raise RuntimeWarning("Could not connect to zview")
            self.zv = None
            return False

    def __init__(self):
        self.zv = None
        self.connect()

    def remove_shape(self, namehandle=""):
        self.zv.removeShape(namehandle)

    def plot_points(self, namehandle, xyz, color=None, alpha=None):
        if not self.connect():
            return False
        xyzrgba = self.xyz2xyzrgba(xyz, color, alpha)
        ok = self.zv.plot(namehandle, xyzrgba)
        return ok

    def plot_mesh(self, namehandle, xyz, indices, color=None, alpha=None):
        if not self.connect():
            return False
        xyzrgba = self.xyz2xyzrgba(xyz, color, alpha)
        ok = self.zv.plot(namehandle, xyzrgba, indices[:, 0:3])
        return ok

    def plot_edges(self, namehandle, xyz, indices, color=None, alpha=None):
        if not self.connect():
            return False
        xyzrgba = self.xyz2xyzrgba(xyz, color, alpha)
        ok = self.zv.plot(namehandle, xyzrgba, indices[:, 0:2])
        return ok

    def plot_marker(
        self, namehandle, shift, scale, rotation=np.eye(3), color=None, alpha=None
    ):
        xyz = (
            np.array(
                [
                    [0, 0, 0],
                    [-2 * scale, -scale / 2, -scale / 2],
                    [-2 * scale, scale / 2, -scale / 2],
                    [-2 * scale, 0, scale / 2],
                ]
            )
        ) @ rotation.T + shift
        f = np.array([[0, 3, 1], [1, 3, 2], [0, 2, 3], [0, 2, 1]])
        xyzrgba = self.xyz2xyzrgba(xyz, color, alpha)
        ok = self.zv.plot(namehandle, xyzrgba, f)
        return ok

    def plot_cuboid(
        self, namehandle, shift, scale, rotation=np.eye(3), color=None, alpha=None
    ):
        xyz = (
            np.array(
                [
                    [-1, -1, -1],
                    [1, -1, -1],
                    [1, 1, -1],
                    [-1, 1, -1],
                    [-1, -1, 1],
                    [1, -1, 1],
                    [1, 1, 1],
                    [-1, 1, 1],
                ]
            )
        ) * scale @ rotation.T + shift

        f = np.array(
            [
                [0, 3, 2],
                [0, 2, 1],
                [4, 5, 6],
                [4, 6, 7],
                [0, 4, 5],
                [0, 5, 1],
                [2, 3, 7],
                [2, 7, 6],
                [0, 3, 7],
                [0, 7, 4],
                [5, 6, 2],
                [5, 2, 1],
            ]
        )
        xyzrgba = self.xyz2xyzrgba(xyz, color=color, alpha=alpha)
        ok = self.zv.plot(namehandle, xyzrgba, f)
        return ok

    def plot_cuboid_edges(
        self, namehandle, shift, scale, rotation=np.eye(3), color=None, alpha=None
    ):
        xyz = (
            np.array(
                [
                    [-1, -1, -1],
                    [1, -1, -1],
                    [1, 1, -1],
                    [-1, 1, -1],
                    [-1, -1, 1],
                    [1, -1, 1],
                    [1, 1, 1],
                    [-1, 1, 1],
                ]
            )
        ) * scale @ rotation.T + shift

        e = np.array(
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 0],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 4],
                [0, 4],
                [1, 5],
                [2, 6],
                [3, 7],
            ]
        )
        xyzrgba = self.xyz2xyzrgba(xyz, color=color, alpha=alpha)
        ok = self.zv.plot(namehandle, xyzrgba, e)
        return ok
