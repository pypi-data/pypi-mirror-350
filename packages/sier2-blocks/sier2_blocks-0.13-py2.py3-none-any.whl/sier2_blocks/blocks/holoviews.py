from sier2 import Block
import param

import panel as pn
import numpy as np

import holoviews as hv
hv.extension('bokeh', inline=True)

## TODO: Option to force plots to have equal axes sizes on initialisation.
## ^^ Not sure this is possible nicely within Bokeh. You can set data_aspect, but that
## has awkward effects with panel's stretch sizing.

class HvPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')
    
    x_sel = param.ObjectSelector()
    y_sel = param.ObjectSelector()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width', min_height=600)
        self.hv_pane.object=self._produce_plot

    @param.depends('in_df', 'x_sel', 'y_sel')
    def _produce_plot(self):
        if None not in (self.x_sel, self.y_sel):
            return hv.Points(self.in_df, kdims=[self.x_sel, self.y_sel])

        else:
            return hv.Points([])

    def execute(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        if len(plottable_cols)<2:
            pn.state.notifications.error(f'Error plotting. Could not find two columns with numeric data.', duration=10_000)
        else:
            self.param['x_sel'].objects = plottable_cols
            self.param['y_sel'].objects = plottable_cols
            self.x_sel = plottable_cols[0]
            self.y_sel = plottable_cols[1]

        self.out_df = self.in_df

    def __panel__(self):
        return pn.Column(
            pn.Row(
                self.param['x_sel'],
                self.param['y_sel']
            ),
            self.hv_pane
        )

class HvPointsSelect(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, block_pause_execution=True, *args, **kwargs):
        super().__init__(
            *args,
            block_pause_execution=block_pause_execution,
            continue_label='Continue With Selection',
            **kwargs,
        )
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width', min_height=600)
        self.selection = hv.streams.Selection1D()
        self.hv_pane.object=self._produce_plot

    x_sel = param.ObjectSelector()
    y_sel = param.ObjectSelector()
    
    @param.depends('in_df', 'x_sel', 'y_sel')
    def _produce_plot(self):
        if self.in_df is not None and self.x_sel is not None and self.y_sel is not None:
            scatter = hv.Points(self.in_df, kdims=[self.x_sel, self.y_sel])

        else:
            scatter = hv.Points([])

        scatter = scatter.opts(tools=['box_select'])
        self.selection.source = scatter
        return scatter

    def prepare(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        if len(plottable_cols)<2:
            pn.state.notifications.error(f'Error plotting. Could not find two columns with numeric data.', duration=10_000)
        else:
            self.param['x_sel'].objects = plottable_cols
            self.param['y_sel'].objects = plottable_cols
            self.x_sel = plottable_cols[0]
            self.y_sel = plottable_cols[1]

    def execute(self):
        self.out_df = self.in_df.loc[self.selection.index]

    def __panel__(self):
        return pn.Column(
            pn.Row(
                self.param['x_sel'],
                self.param['y_sel']
            ),
            self.hv_pane
        )

class HvHist(Block):
    """Produce a Histogram of input data."""

    # Define params
    #
    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    column = param.ObjectSelector()
    bins = param.Integer(100, bounds=(0, None))
    integer_bins = param.Boolean(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make a pane to hold the plot.
        #
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width', min_height=600)

        # Make a widget to control the bins parameter.
        # We need this so we can disable it when using integer bins.
        #
        self.bins_widget = pn.widgets.IntInput(name='Bins', start=0, value=self.bins)
        self.bins_widget.param.watch(lambda event: setattr(self, 'bins', event.new), 'value')

        # Set up the plot.
        #
        self.hv_pane.object=self._produce_plot
        
    
    @param.depends('in_df', 'column', 'bins', 'integer_bins')
    def _produce_plot(self):     

        # Disable the bin selection when using integer bins.
        #
        if self.integer_bins:
            self.bins_widget.disabled = True
        else:
            self.bins_widget.disabled = False
          
        if self.in_df is not None and self.column is not None :
            if self.integer_bins:
                col = self.in_df[self.column]
                self.bins = col.max() - col.min() + 1
                self.bins_widget.value = self.bins
                
                frequencies, edges = np.histogram(
                    col, 
                    np.arange(col.min()-0.5, col.max()+1.5, 1),
                )
            else:
                frequencies, edges = np.histogram(self.in_df[self.column], self.bins)

        else:
            frequencies, edges = [], []

        return hv.Histogram((edges, frequencies))        

    def execute(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        
        self.param['column'].objects = plottable_cols
        self.column = plottable_cols[0]

        self.out_df = self.in_df

    def __panel__(self):
        return pn.Column(
            pn.Row(
                self.param['column'],
                self.bins_widget,
                self.param['integer_bins'],
            ),
            self.hv_pane
        )