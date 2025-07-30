import param
import pandas as pd
import panel as pn
from sier2 import Block


class SimpleTable(Block):
    """ Simple Table Viewer

    Make a tabulator to display an input table.
    """
    
    pn.extension('tabulator')
    
    in_df = param.DataFrame(doc='Input pandas dataframe')
    in_tabulator_kwargs = param.Dict(doc='Keyword arguments passed to the tabulator display', default=dict())
    
    out_df = param.DataFrame(doc='Output pandas dataframe', default=pd.DataFrame())

    def execute(self):
        self.out_df = self.in_df

    def __panel__(self):
        # Build a dictionary of arguments for the tabulator.
        # These defaults will be overriden by in_tabulator_kwargs.
        #
        display_dict = {
            'type': pn.widgets.Tabulator, 
            'page_size':20, 
            'pagination':'local', 
            'name':'DataFrame',
        }
        display_dict.update(self.in_tabulator_kwargs)
        return pn.Param(
            self,
            parameters=['out_df'],
            widgets={'out_df': display_dict}
        )

class SimpleTableSelect(Block):
    """ Simple Table Selection

    Make a tabulator to display an input table.
    Pass on selections as an output.
    """
    
    pn.extension('tabulator')
    
    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, continue_label='Continue With Selection', **kwargs)
        self.tabulator = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    def prepare(self):
        if self.in_df is not None:
            self.tabulator.value = self.in_df
        else:
            self.tabulator.value = pd.DataFrame()

    def execute(self):
        self.out_df = self.tabulator.selected_dataframe

    def __panel__(self):
        return self.tabulator

class PerspectiveTable(Block):
    """Perspective Table Viewer

    Display a table in an interactive viewer.
    """
    
    pn.extension('perspective')
    
    in_df = param.DataFrame(doc='Input pandas dataframe')
    in_columns_config = param.Dict(doc='Config to pass to Perspective, a dictionary of {column:config}')
    
    out_df = param.DataFrame(doc='Output pandas dataframe', default=pd.DataFrame())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perspective = pn.Row()

    def execute(self):
        self.out_df = self.in_df
        self.perspective.clear()
        
        self.perspective.append(pn.pane.Perspective(
            self.in_df, 
            # theme='pro-dark', 
            sizing_mode='stretch_both', 
            min_height=720, 
            columns_config=self.in_columns_config,
            editable=False,
        ))
        
    def __panel__(self):
        return self.perspective

class MultiPerspectiveTable(Block):
    """View tables
    
    Takes a dictionary of {name: dataframe} and displays them each in a tab containing a Perspective view.
    """
    
    pn.extension('perspective')
    in_data = param.Dict(doc='Tables to view')
    in_columns_config = param.Dict(doc='Config to pass to Perspective, a dictionary of {column:config}')
    
    table_tabs = pn.Tabs()

    @param.depends('in_data', watch=True)
    def _on_data_update(self):
        self.table_tabs.clear()

        for name, data in self.in_data.items():
            data_view = pn.pane.Perspective(
                data, 
                theme='solarized-dark', 
                sizing_mode='stretch_both', 
                min_height=720, 
                columns_config=self.in_columns_config,
            )
            self.table_tabs.append((name, data_view))

    def __panel__(self):
        return self.table_tabs