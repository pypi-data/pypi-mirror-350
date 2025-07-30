from jutility import plotting, cli

class PlotType:
    @classmethod
    def plot(cls, mp: plotting.MultiPlot, name: str, output_dir: str):
        raise NotImplementedError()

    @classmethod
    def get_cli_arg(cls):
        return cli.ObjectChoice(
            "plot_type",
            cli.ObjectArg(Png),
            cli.ObjectArg(Pdf),
            cli.ObjectArg(Show),
            default="Png",
            is_kwarg=True,
        )

class Png(PlotType):
    @classmethod
    def plot(cls, mp: plotting.MultiPlot, name: str, output_dir: str):
        mp.save(name, output_dir)

class Pdf(PlotType):
    @classmethod
    def plot(cls, mp: plotting.MultiPlot, name: str, output_dir: str):
        plotting.set_latex_params(use_times=True)
        mp.save(name, output_dir, pdf=True)

class Show(PlotType):
    @classmethod
    def plot(cls, mp: plotting.MultiPlot, name: str, output_dir: str):
        mp.save(name, output_dir, close=False)
        mp.show()
