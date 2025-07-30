#

# Various blocks that produce input data, useful for testing dags.
#

import param

import pandas as pd
import panel as pn

from sier2 import Block

from faker import Faker


class StaticDataFrame(Block):
    """ Import static data frame for testing dags.

    """

    out_df = param.DataFrame()

    def execute(self):
        self.out_df = pd.DataFrame(data = {
            "calories": [420, 380, 390, None],
            "duration": [50, 40, 45, None],
            "Latitude": [0, 45, 70, None],
            "Longitude": [15, 30, 60, None],
            "Name": ['a', 'b', 'c', None],
        })

class FakerData(Block):
    """ Generate realistic fake data of various types.
    
    """

    in_data_type = param.ObjectSelector(default='name')
    in_output_type = param.ObjectSelector(
        default='dataframe', 
        objects=['dataframe', 'list']
    )
    in_output_length = param.Integer(default=100)
    
    out_data = param.ClassSelector(class_=(pd.DataFrame, list))

    def __init__(self, block_pause_execution=True, *args, **kwargs):
        super().__init__(
            block_pause_execution=block_pause_execution,
            continue_label='Generate fake data',
            *args, **kwargs,
        )
        self.fake = Faker()

        # The fake object can generate all sorts of things for us.
        # We can get a list of all the options from the attributes.
        #
        self.param['in_data_type'].objects = [
            opt for opt in dir(self.fake) if not opt.startswith('_') and not opt.endswith('_')
        ]

    def execute(self):
        gen = getattr(self.fake, self.in_data_type)
        data = [gen() for _ in range(self.in_output_length)]

        if self.in_output_type == 'dataframe':
            self.out_data = pd.DataFrame({self.in_data_type: data})

        else:
            self.out_data = data




