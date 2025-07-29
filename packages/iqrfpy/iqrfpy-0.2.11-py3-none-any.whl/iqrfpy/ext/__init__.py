"""IQRFPY extensions module.

Supported extensions are automatically loaded if installed.
"""

import importlib.util

extensions = [
    'iqd_diagnostics',
    'mqtt_transport'
]

for ext in extensions:
    ext_module = f'iqrfpy.ext.{ext}'
    installed = importlib.util.find_spec(ext_module) is not None
    if installed:
        importlib.import_module(ext_module)

del ext, ext_module, installed
