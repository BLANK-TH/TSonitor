Buttons
========
STonitor has a button configuration YAML file. This can be used to create aliases/nicknames for button names or button
IDs in Jailbreak logs, it can also be used to specify that you wish for that button to be ignored in JB log parsing
(for things like button griefs), this is mostly used for safe buttons to lower the amount of false positives (like cells
opening or buttons similar to that). You can find the file in ``data/buttons.yaml`` in STonitor's directory. There are
already some default values filled in.

The file itself is split into two large categories: ``normal`` and ``regex``. Normal allows you to specify individual
button names or IDs to configure them, and is pretty simple to use. Regex allows you to use RegEx(p) to specify groups
of button names, Regex is fairly advanced and it's not recommended you use it unless you know what you're doing.

Each configuration regardless of if it's normal mode or regex mode has two parameters (``ignore`` and ``alias``).
A simple example using normal button names is the following:

.. code-block::

    celldoors:
      ignore: true
      alias: Cell Button

The ``ignore`` value in each configuration can be either ``true`` or ``false``. ``true`` means that that button will be
ignored in detection operations (such as button grief detection). ``false`` means that it will still be detected (this
is the default value).

The ``alias`` value is to specify an alias for that specific button. In the example above, ``celldoors`` will be
replaced with ``Cell Button`` when it's shown in STonitor's output. ``null`` means the name will be unchanged (this
is the default value)

If you're inexperienced with YAML, it's recommend you add single quotes to the start and end of each value, to avoid
you accidentally using formatting characters (``ignore`` and ``alias`` are fine, no need to add quotes around them).
``true``, ``false``, and ``null`` should not be surrounded with quotes either as
they are not literals (unless you want the name of a button to be ``null`` for some reason, then surround it with
quotes in that case). The above example would become:

.. code-block::

    'celldoors':
      ignore: true
      alias: 'Cell Button'

Both ``ignore`` and ``alias`` must be present even if they're not being used.
If you do not fill in one of the required arguments, it will be created with default values. For ``ignore``, the default
is ``false``, for ``alias``, the default is ``null``.

Normal
-------
Normal mode is easy, specify the button name that shows in logs (as shown above, ``celldoors`` is the button name in
that example). If you want to use a Button ID, use the format ``'#id here'``, for example: ``'#12345'``. Note that
**using single quotes IS A MUST** in this case, as *#* is a formatting character in YAML. Here are examples for both
methods (ignore and alias are random values in both examples):

Button Name
^^^^^^^^^^^^^

.. code-block::

    'celldoors':
      ignore: true
      alias: 'Cell Button'

Button ID
^^^^^^^^^^

.. code-block::

    '#123456':
      ignore: false
      alias: 'Some random button'

Regex
-------
.. warning:: Do not use Regex unless you know exactly what you're doing

STonitor uses re.fullmatch with the Regex and button name (you can't use Regex for Button IDs), this means that the
Regex must fully match the button name, not just contain a match to the Regex. If you want it to just need to contain
the Regex, add ``.*`` to the start and end of the regex. It's recommended to use `Regex101 <https://regex101.com>`_ to
build your Regex and test if it works properly (make sure to set the flavor to Python).

To use Regex, simply put the regex where Button Name and Button ID would be in normal mode. For example:

.. code-block::

    'piano_key_\ws?':
      ignore: true
      alias: Piano Key
