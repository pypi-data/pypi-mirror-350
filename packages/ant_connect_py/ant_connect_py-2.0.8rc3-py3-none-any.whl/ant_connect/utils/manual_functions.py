""" 
This module serves as a location to manually add functions/methods to
the auto generated models in models.py. 

If you are not familiar with the principle for this package, please 
check out the readme. 

how-to write manual functions/methods:
* check out the available models in `models.py`;
* if there are desired functions/methods, that are not in `models.py`, 
    you can specify them in this module;
* the name of the object should be the same as the object in `models.py`, 
    followed by 'Custom'. Example: 'TableCustom', 'RecordCustom', etc.;
* before manually writing your function/method you should check if the 
    object already exists in this module;

what:
all classes in this module will be automatically inherited by the 
corresponding model in `models.py` during models.py auto-generation. 
Users will be able to use the methods via the model in `models.py`.
"""

from dataclasses import dataclass


# Examples -->
# @dataclass
# class LicenseCustom:
#     """ Example of a manually created class for the License model. """
#     def hello_world(cls, ) -> None:
#         """ Example of a manually created method for the License model. """
#         print("Hello World")

# @dataclass
# class ColumnCustom:
#     """ Example of a manually created class for the Column model. """
#     def hello_world(cls, ) -> None:
#         """ Example of a manually created method for the Column model. """
#         print("Hello World")
# <-- Examples
