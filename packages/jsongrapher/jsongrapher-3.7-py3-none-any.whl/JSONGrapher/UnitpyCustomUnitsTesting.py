import unitpy
import re
from unitpy.definitions.entry import Entry

def add_custom_unit(unit_string):
    # Need to put an entry into "bases" because the BaseSet class will pull from that dictionary.
    unitpy.definitions.unit_base.bases[unit_string] = unitpy.definitions.unit_base.BaseUnit(
        label=unit_string, abbr=unit_string, dimension=unitpy.definitions.dimensions.dimensions["amount_of_substance"]
    )
    
    # Then need to make a BaseSet object to put in. Confusingly, we *do not* put a BaseUnit object into the base_unit argument, below. 
    # We use "mole" to avoid conflicting with any other existing units.
    base_unit = unitpy.definitions.unit_base.BaseSet(mole=1)
    
    new_entry = Entry(label=unit_string, abbr=unit_string, base_unit=base_unit, multiplier=1)
    
    # Only add the entry if it is missing. A duplicate entry would cause crashing later.
    if 'frog' not in unitpy.ledger._lookup:
        unitpy.ledger.add_unit(new_entry)  # Implied return is here. No return needed.

add_custom_unit("frog")
add_custom_unit("frog")

units_string_1 = 'm*frog'
units_string_2 = 'm*frog'
units_string_1_multiplied = 1*unitpy.U(units_string_1 )
print("line 25", type(units_string_1_multiplied))
units_string_1_multiplied.to(units_string_2)
