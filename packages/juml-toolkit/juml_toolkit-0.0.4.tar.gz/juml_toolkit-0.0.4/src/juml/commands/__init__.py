from juml.commands.base import Command
from juml.commands.train import Train
from juml.commands.sweep import Sweep
from juml.commands.sweep2d import Sweep2d
from juml.commands.profile import Profile
from juml.commands.plot_confusion_matrix import PlotConfusionMatrix
from juml.commands.plot_1d_regression import Plot1dRegression
from juml.commands.plot_sequential import PlotSequential
from juml.commands.compare_sweeps import CompareSweeps

def get_all() -> list[type[Command]]:
    return [
        Train,
        Sweep,
        Sweep2d,
        Profile,
        PlotConfusionMatrix,
        Plot1dRegression,
        PlotSequential,
        CompareSweeps,
    ]
