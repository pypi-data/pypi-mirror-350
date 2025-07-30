Sier2 Blocks
============

This library provides useful blocks for sier2.

A block is implemented as:

.. code-block:: python

    class MyBlock(Block):
        ...

The ``Block`` class inherits from ``param.Parameterized``, and uses parameters as described at https://param.holoviz.org/user_guide/Parameters.html.
There are three kinds of parameters:

    * Input parameters start with ``in_``. These parameters are set before a block is executed.
    * Output parameters start with ``out_``. The block sets these in its ``execute()`` method.
    * Block parameters start with ``block_``. These are reserved for use by blocks.

A typical block will have at least one input parameter, and an ``execute()`` method that is called when an input parameter value changes.

.. code-block:: python

    class MyBlock(Block):
        in_value = param.String(label='Input Value')
        out_upper = param.String(label='Output value)

        def execute(self):
            self.out_value = self.in_value.upper()
            print(f'New value is {self.out_value}')

The block parameter ``block_pause_execution`` allows a block to act as an "input" block, particularly when the block hsa a GUI interface. When set to True and dag execution reaches this block, the block's ``prepare()`` method is called, then the dag stops executing. This allows the user to interact with a user interface.

The dag is then restarted using ``dag.execute_after_input(input_block)`` (typically by a "Continue" button in the GUI.) When the dag is continued at this block, the block's ``execute()`` method is called, and dag execution continues.

Many blocks are optimised for use with Panel, and have a specified ``__panel__`` method. This should return a panel-interpretable object which is displayed within a card when used in a ``PanelDag``. If ``__panel__`` is not defined, the ``in_`` params will be used to automatically generate one.
