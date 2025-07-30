import torch
from jutility import plotting, util, units
from juml.models.sequential import Sequential

def display_sequential(
    model:      Sequential,
    x:          torch.Tensor,
    printer:    (util.Printer | None)=None,
) -> tuple[torch.Tensor, util.Table]:
    util.hline()
    w = max(len(repr(m)) for m in model.layers)
    table = util.Table(
        util.Column("layer",    "r",    -w,     "Layer"),
        util.Column("shape",    "s",    -22,    "Output shape"),
        util.Column("t",        ".5fs", 10,     "Time"),
        printer=printer,
    )
    total_timer = util.Timer(verbose=False)
    layer_timer = util.Timer(verbose=False)
    display_layer(table, "Input", x, layer_timer)

    with layer_timer:
        x = model.embed.forward(x)
        display_layer(table, model.embed, x, layer_timer)
    for layer in model.layers:
        with layer_timer:
            x = layer.forward(x)
            display_layer(table, layer, x, layer_timer)
    with layer_timer:
        x = model.pool.forward(x)
        display_layer(table, model.pool, x, layer_timer)

    table.update(layer="Full model:")
    display_layer(table, model, x, total_timer)
    util.hline()
    return x, table

def display_layer(
    table:  util.Table,
    layer:  (torch.nn.Module | str),
    x:      torch.Tensor,
    timer:  util.Timer,
):
    table.update(layer=layer, shape=list(x.shape), t=timer.get_time_taken())

def num_params(layer: torch.nn.Module) -> int:
    return sum(
        int(p.numel())
        for p in layer.parameters()
        if  p.requires_grad
    )

def plot_sequential(
    model:      Sequential,
    x:          torch.Tensor,
    printer:    (util.Printer | None)=None,
) -> plotting.MultiPlot:
    _, table    = display_sequential(model, x, printer)
    t_data      = table.get_data("t")
    t_list      = t_data[1:]
    t_tot       = t_list[-1]
    t_max       = max(t_list[:-1])
    t_tot_label = "Total = %s"  % units.time_concise.format(t_tot)
    t_max_label = "Max = %s"    % units.time_concise.format(t_max)

    layer_list  = [model.embed, *model.layers, model.pool]
    np_list     = [num_params(m) for m in layer_list]
    n_tot_label = "Total = %s"  % units.metric.format(sum(np_list))
    n_max_label = "Max = %s"    % units.metric.format(max(np_list))

    name_list   = [type(m).__name__ for m in layer_list]
    x_plot      = list(range(len(name_list)))
    kwargs      = {
        "xticks":               x_plot,
        "xticklabels":          name_list,
        "rotate_xticklabels":   True,
        "xlabel":               "Layer",
    }
    return plotting.MultiPlot(
        plotting.Subplot(
            plotting.Bar(x_plot, t_list[:-1]),
            plotting.HLine(t_tot, c="k", ls="--", label=t_tot_label),
            plotting.HLine(t_max, c="r", ls="--", label=t_max_label),
            plotting.Legend(),
            **kwargs,
            ylim=[0, 1.1 * t_max],
            ylabel="Time (s)",
        ),
        plotting.Subplot(
            plotting.Bar(x_plot, np_list),
            plotting.HLine(sum(np_list), c="k", ls="--", label=n_tot_label),
            plotting.HLine(max(np_list), c="r", ls="--", label=n_max_label),
            plotting.Legend(),
            **kwargs,
            ylim=[0, 1.1 * max(np_list)],
            ylabel="# Parameters",
        ),
        title="%r\nInput shape = %s" % (model, list(x.shape)),
        figsize=[10, 6],
    )
