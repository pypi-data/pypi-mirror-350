import unitpy
import unitpy.definitions
import unitpy.definitions.entry

print(unitpy.U("kg/m"))


print(unitpy.U("(((kg)/m))/s"))

units1 = unitpy.U("(((kg)/m))/s")
units2 = unitpy.U("(((g)/m))/s")
unitsRatio = units1/units2
print(unitsRatio)

print(units2)
units1multiplied =1*unitpy.U("(((kg)/m))/s")
print("line 14")
ratioWithUnits = units1multiplied.to("(((g)/m))/s")
print(ratioWithUnits)
print(str(ratioWithUnits).split(' '))

units1 = unitpy.Q("1 (((kg)/m))/s")
units2 = unitpy.Q("1 (((g)/m))/s")
print("line 22", units2.base_unit)
unitsRatio = units1/units2
print("line 23")
print(unitsRatio)



print(units2)
units1multiplied =1*unitpy.U("(((kg)/m))*(s**-1)")
print("line 14")
ratioWithUnits = units1multiplied.to("(((g)/m))/s")
print(ratioWithUnits)
print(str(ratioWithUnits).split(' '))
print(units1multiplied.base_unit)

units5 = unitpy.Q("1 (((g)/m))/s")
print(units5.base_unit)


def convert_inverse_units(expression, depth=100):
    import re
    # Patterns to match valid reciprocals while ignoring multiplied units
    patterns = [r"1/\((1/.*?)\)", r"1/([a-zA-Z]+)"]
    
    for _ in range(depth):
        new_expression = expression
        for pattern in patterns:
            new_expression = re.sub(pattern, r"(\1)**(-1)", new_expression)
        
        # Stop early if no more changes are made
        if new_expression == expression:
            break
        expression = new_expression
    return expression


expression_original = "1/(1/bar)"
expression_altered = convert_inverse_units(expression_original)
units6 = unitpy.Q('1*'+expression_altered)
print(units6.unit)

from unitpy import U, Unit
import unitpy
newunit = unitpy.Unit("meter")
from unitpy.definitions.entry import Entry
# new_entry = Entry("frog", "frog", "frog", 1.0)
# unitpy.ledger.add_unit(new_entry)
def add_custom_unit_to_unitpy(unit_string):
    import unitpy
    from unitpy.definitions.entry import Entry
    #need to put an entry into "bases" because the BaseSet class will pull from that dictionary.
    unitpy.definitions.unit_base.bases[unit_string] = unitpy.definitions.unit_base.BaseUnit(label=unit_string, abbr=unit_string,dimension=unitpy.definitions.dimensions.dimensions["amount_of_substance"])
    #Then need to make a BaseSet object to put in. Confusingly, we *do not* put a BaseUnit object into the base_unit argument, below. 
    #We use "mole" to avoid conflicting with any other existing units.
    base_unit =unitpy.definitions.unit_base.BaseSet(mole = 1)
    #base_unit = unitpy.definitions.unit_base.BaseUnit(label=unit_string, abbr=unit_string,dimension=unitpy.definitions.dimensions.dimensions["amount_of_substance"])
    new_entry = Entry(label = unit_string, abbr = unit_string, base_unit = base_unit, multiplier= 1)
    #only add the entry if it is missing. A duplicate entry would cause crashing later.
    if not unitpy.ledger.get_entry(new_entry):
        unitpy.ledger.add_unit(new_entry) #implied return is here. No return needed.

add_custom_unit_to_unitpy("frog")
#TODO: now know one way how to add custom units to unitpy.
#Cannot put "<>" inside unitpy, but could filter those out, and then put them back. Would need to make a list of unique entries with <> because there could be more than one.

another_test = "1/bar/(1/bar)*bar*frog"
another_test =  convert_inverse_units(another_test)
print("line 65", another_test)
units7 = unitpy.U(another_test)
print("line 66", units7)
print("line 86", 1*units7)
print(unitpy.ledger.get_entry("frog"))
units_string_1 = 'm*frog'
print("line 87",  1*unitpy.U(units_string_1))




print("line 94")

units_string_2 = 'm*frog'

units_string_1_multiplied = 1*unitpy.U(units_string_1 )
units_string_1_multiplied.to(units_string_2)


print(units2)
units1multiplied =1*unitpy.U("(((kg)/m))/s")
print("line 85")
string2 = "(((g)/m))*1/s"
string2 = convert_inverse_units(string2)
print(string2)
ratioWithUnits = units1multiplied.to(string2)
print(ratioWithUnits)
print(str(ratioWithUnits).split(' '))


#micrometer symbol, "μ" will result in error, also typing out "microm" will result in error, but "micrometer" works
units1 = unitpy.U("(((kg)/mm))/s")
#units2 = unitpy.U("(((g)/μm))/s")
#units2 = unitpy.U("(((g)/microm))/s")
units2 = unitpy.U("(((g)/micrometer))/s")
