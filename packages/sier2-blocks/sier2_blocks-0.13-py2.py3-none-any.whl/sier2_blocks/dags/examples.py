# from ..blocks.io import LoadDataFrame, SaveDataFrame
# from ..blocks.view import SimpleTable, SimpleTableSelect, PerspectiveTable
# from ..blocks.holoviews import HvPoints, HvPointsSelect, HvHist
# from ..blocks.test_data import StaticDataFrame, FakerData
# from ..blocks.list_helper import StringToList, ListToCopyable

from sier2 import Connection
from sier2.panel import PanelDag
import panel as pn

# Blocks are imported inside dags so that users can run examples without all 
# of the modules imported.

def hv_points():
    """Load a dataframe from a file and display a Points chart."""
    
    from ..blocks.io import LoadDataFrame
    from ..blocks.holoviews import HvPointsSelect
    from ..blocks.view import SimpleTable
    
    ldf = LoadDataFrame(name='Load DataFrame')
    hps = HvPointsSelect(name='Plot Points')
    st = SimpleTable(name='View Selection')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Points')
    dag.connect(ldf, hps,
        Connection('out_df', 'in_df'),
    )
    dag.connect(hps, st,
        Connection('out_df', 'in_df'),
    )

    return dag

def hv_hist():
    """Load a dataframe from a file and display a Histogram."""
    
    from ..blocks.io import LoadDataFrame
    from ..blocks.holoviews import HvHist

    ldf = LoadDataFrame(name='Load DataFrame')
    hh = HvHist(name='Plot Histogram')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Histogram')
    dag.connect(ldf, hh,
        Connection('out_df', 'in_df'),
    )

    return dag

def table_view():
    """Load a dataframe from file and display in a panel table."""

    from ..blocks.io import LoadDataFrame
    from ..blocks.view import SimpleTable, SimpleTableSelect

    ldf = LoadDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    sel_st = SimpleTable(name='Selection')

    DOC = '''# Table viewer

    Load a dataframe from a file and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(ldf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag

def faker_view():
    """Load and display fake data."""

    from ..blocks.test_data import FakerData
    from ..blocks.view import SimpleTable

    fdf = FakerData(name='Fake Data')
    st = SimpleTable(name='Display')

    DOC = '''# Faker example

    Load and display fake data.
    '''

    dag = PanelDag(doc=DOC, title='Faker')
    dag.connect(fdf, st, Connection('out_data', 'in_df'))

    return dag

def static_view():
    """Load a static example dataframe and display in a table."""

    from ..blocks.test_data import StaticDataFrame
    from ..blocks.view import SimpleTable, SimpleTableSelect

    sdf = StaticDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    sel_st = SimpleTable(name='Selection')

    DOC = '''# Static table viewer

    Load a static example dataframe and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(sdf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag

def perspective_view():
    """Load a static example dataframe and display in an interactive view."""

    from ..blocks.io import LoadDataFrame
    from ..blocks.view import PerspectiveTable

    ldf = LoadDataFrame(name='Load DataFrame')
    pt = PerspectiveTable(name='View Table')

    DOC = '''# Perspective table viewer

    Load a dataframe and display the data as a table interactively.
    '''

    dag = PanelDag(doc=DOC, title='Perspective')
    dag.connect(ldf, pt, Connection('out_df', 'in_df'))

    return dag

def save_csv():
    """Load a dataframe from file and download."""

    from ..blocks.test_data import StaticDataFrame
    from ..blocks.view import SimpleTableSelect
    from ..blocks.io import SaveDataFrame
    
    sdf = StaticDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    edf = SaveDataFrame(name='Export')

    DOC = '''# Table viewer

    Load a dataframe from file and download.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(sdf, st, Connection('out_df', 'in_df'))
    dag.connect(st, edf, Connection('out_df', 'in_df'))

    return dag

def list_input_output():
    """Load a list froma delimited string, and return it with the option to change the delimiter"""

    from ..blocks.list_helper import StringToList, ListToCopyable
    
    stl = StringToList(name='String Input')
    ltc = ListToCopyable(name='Output String')

    DOC = """# List Input Output example"""

    dag = PanelDag(doc=DOC, title='List Example')
    dag.connect(stl, ltc, Connection('out_list', 'in_list'))

    return dag