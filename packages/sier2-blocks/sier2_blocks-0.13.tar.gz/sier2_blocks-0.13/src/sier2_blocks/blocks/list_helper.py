from sier2 import Block
import panel as pn
import param
import time

DELIMITERS = {
    'comma': ',',
    'newline': '\n',
    'tab': '\t',
    'comma and newline': ',\n',
    'space': ' ',
    '\" OR \" (query syntax)': ' OR ',
}

class StringToList(Block):
    """Take a string containing a list of delimited values and pass them as a python list.
    
    This is a common pattern to get data into a python list object for iteration."""

    in_str = param.String(doc='Input string to be split.', default='')
    in_delimiter = param.ObjectSelector(doc='Delimiter', objects=list(DELIMITERS.keys()), default=list(DELIMITERS.keys())[0])
    out_list = param.List(doc='A list of string elements.', item_type=str)

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, **kwargs)
        
    def execute(self):
        # We need a small sleep in here.
        # The TextAreaInput widget has two params, input_value, and value.
        # input_value updates live as the user changes things, value is propagated only when they click away.
        # If we do not sleep, it's possible that value hasn't had the chance to update yet if the user
        # has gone straight from the text input to clicking on the button.
        #
        time.sleep(1)
        
        delimiter = DELIMITERS[self.in_delimiter]
        self.out_list = self.in_str.split(delimiter)

    def __panel__(self):
        return pn.Param(
            self,
            parameters=[
                'in_str',
                'in_delimiter',
            ],
            widgets={
                'in_str': {
                    'type': pn.widgets.TextAreaInput,
                    'name': 'Input text',
                },
                'in_delimiter': {
                    'name': 'List delimiter',
                },
            },
        )#self.panel_view

class ListToCopyable(Block):
    """Join a python list with a specified delimiter.
    The resulting string is displayed for the user to copy or verify.
    This block has no outputs"""

    in_list = param.List(doc='Input list to join', item_type=str)
    in_delimiter = param.ObjectSelector(doc='Delimiter for output', objects=list(DELIMITERS.keys()), default=list(DELIMITERS.keys())[0])

    def execute(self):
        # print(self.in_list)
        pass

    @param.depends('in_delimiter', 'in_list')
    def _build_string(self):
        return pn.pane.Str(
            # Join based on delimiter and escape for html formatting.
            DELIMITERS[self.in_delimiter].join(self.in_list).replace('<','&lt').replace('>','&gt')
        )

    def __panel__(self):
        return pn.Column(
            pn.Param(
                self,
                parameters=[
                    'in_delimiter',
                ],
                widgets={
                    'in_delimiter': {
                        'name': 'Delimiter to use for output',
                    },
                },
            ),
            self._build_string,
        )