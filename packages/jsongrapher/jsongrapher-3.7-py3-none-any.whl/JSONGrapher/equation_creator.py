import re
import json

try:
    from json_equationer.equation_evaluator import evaluate_equation_dict
except ImportError:
    try:
        from .equation_evaluator import evaluate_equation_dict
    except ImportError:
        from equation_evaluator import evaluate_equation_dict


class Equation:
    """
    A class to manage mathematical equations with units and to evaluate them.
    Provides utilities for evaluating, formatting, exporting, and printing.
   
    Initialization:
    - Normally, should be initialized as a blank dict object like example_Arrhenius = Equation().
    - Defaults to an empty equation with predefined structure.
    - Accepts an optional dictionary (`initial_dict`) to prepopulate the equation dictionary.

    Example structure:
    ```
    custom_dict = {
        'equation_string': "k = A * (e ** (-Ea / (R * T)))",
        'x_variable': "T (K)",
        'y_variable': "k (s**-1)",
        'constants': {"Ea": "30000 J/mol", "R": "8.314 J/(mol*K)", "A": "1*10**13 (s**-1)", "e": "2.71828"},
        'num_of_points': 10,
        'x_range_default': [200, 500],
        'x_range_limits': [None, 600],
        'points_spacing': "Linear"
        'graphical_dimensionality': 2
    }

    #The reason we use 'graphical_dimensionality' rather than 'dimensionality' is that mathematicians define the dimensionality in terms of independent variables.
    #But here, we are usually expecting users who are concerned with 2D or 3D graphing.

    equation_instance = Equation(initial_dict=custom_dict)
    ```
    """

    def __init__(self, initial_dict=None):
        """Initialize an empty equation dictionary."""
        if initial_dict==None:
            initial_dict = {}
        self.equation_dict = {
            'equation_string': '',
            'x_variable': '',  
            'y_variable': '',
            'constants': {},
            'num_of_points': None,  # Expected: Integer, defines the minimum number of points to be calculated for the range.
            'x_range_default': [0, 1],  # Default to [0,1] instead of an empty list.
            'x_range_limits': [None, None],  # Allows None for either limit.
            'x_points_specified': [],
            'points_spacing': '',
            'reverse_scaling': False,
        }

        # If a dictionary is provided, update the default values
        if len(initial_dict)>0:
            if isinstance(initial_dict, dict):
                self.equation_dict.update(initial_dict)
            else:
                raise TypeError("initial_dict must be a dictionary.")

    def validate_unit(self, value):
        """Ensure that the value is either a pure number or contains a unit."""
        unit_pattern = re.compile(r"^\d+(\.\d+)?(.*)?$")
        if not unit_pattern.match(value):
            raise ValueError(f"Invalid format: '{value}'. Expected a numeric value, optionally followed by a unit.")

    def add_constants(self, constants):
        """Add constants to the equation dictionary, supporting both single and multiple additions."""
        if isinstance(constants, dict):  # Single constant case
            for name, value in constants.items():
                self.validate_unit(value)
                self.equation_dict['constants'][name] = value
        elif isinstance(constants, list):  # Multiple constants case
            for constant_dict in constants:
                if isinstance(constant_dict, dict):
                    for name, value in constant_dict.items():
                        self.validate_unit(value)
                        self.equation_dict['constants'][name] = value
                else:
                    raise ValueError("Each item in the list must be a dictionary containing a constant name-value pair.")
        else:
            raise TypeError("Expected a dictionary for one constant or a list of dictionaries for multiple constants.")

    def set_x_variable(self, x_variable):
        """
        Set the x-variable in the equation dictionary.
        Expected format: A descriptive string including the variable name and its unit.
        Example: "T (K)" for temperature in Kelvin.
        """
        self.equation_dict["x_variable"] = x_variable

    def set_y_variable(self, y_variable):
        """
        Set the y-variable in the equation dictionary.
        Expected format: A descriptive string including the variable name and its unit.
        Example: "k (s**-1)" for a rate constant with inverse seconds as the unit.
        """
        self.equation_dict["y_variable"] = y_variable

    def set_z_variable(self, z_variable):
        """
        Set the z-variable in the equation dictionary.
        Expected format: A descriptive string including the variable name and its unit.
        Example: "E (J)" for energy with joules as the unit.
        """
        self.equation_dict["z_variable"] = z_variable

    def set_x_range_default(self, x_range):
        """
        Set the default x range.
        Expected format: A list of two numeric values representing the range boundaries.
        Example: set_x_range([200, 500]) for temperatures between 200K and 500K.
        """
        if not (isinstance(x_range, list) and len(x_range) == 2 and all(isinstance(i, (int, float)) for i in x_range)):
            raise ValueError("x_range must be a list of two numeric values.")
        self.equation_dict['x_range_default'] = x_range

    def set_x_range_limits(self, x_limits):
        """
        Set the hard limits for x values.
        Expected format: A list of two values (numeric or None) defining absolute boundaries.
        Example: set_x_range_limits([100, 600]) to prevent x values outside this range.
        Example: set_x_range_limits([None, 500]) allows an open lower limit.
        """
        if not (isinstance(x_limits, list) and len(x_limits) == 2):
            raise ValueError("x_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in x_limits):
            raise ValueError("Elements in x_limits must be numeric or None.")
        self.equation_dict['x_range_limits'] = x_limits

    def set_y_range_default(self, y_range):
        """
        Set the default y range.
        Expected format: A list of two numeric values representing the range boundaries.
        Example: set_y_range([0, 100]) for a percentage scale.
        """
        if not (isinstance(y_range, list) and len(y_range) == 2 and all(isinstance(i, (int, float)) for i in y_range)):
            raise ValueError("y_range must be a list of two numeric values.")
        self.equation_dict['y_range_default'] = y_range

    def set_y_range_limits(self, y_limits):
        """
        Set the hard limits for y values.
        Expected format: A list of two values (numeric or None) defining absolute boundaries.
        Example: set_y_range_limits([None, 50]) allows an open lower limit but restricts the upper limit.
        """
        if not (isinstance(y_limits, list) and len(y_limits) == 2):
            raise ValueError("y_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in y_limits):
            raise ValueError("Elements in y_limits must be numeric or None.")
        self.equation_dict['y_range_limits'] = y_limits

    def set_z_range_default(self, z_range):
        """
        Set the default z range.
        Expected format: A list of two numeric values representing the range boundaries.
        Example: set_z_range([0, 5000]) for energy values in Joules.
        """
        if not (isinstance(z_range, list) and len(z_range) == 2 and all(isinstance(i, (int, float)) for i in z_range)):
            raise ValueError("z_range must be a list of two numeric values.")
        self.equation_dict['z_range_default'] = z_range

    def set_z_range_limits(self, z_limits):
        """
        Set the hard limits for z values.
        Expected format: A list of two values (numeric or None) defining absolute boundaries.
        Example: set_z_range_limits([100, None]) allows an open upper limit but restricts the lower boundary.
        """
        if not (isinstance(z_limits, list) and len(z_limits) == 2):
            raise ValueError("z_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in z_limits):
            raise ValueError("Elements in z_limits must be numeric or None.")
        self.equation_dict['z_range_limits'] = z_limits

    def get_z_matrix(self, x_points=None, y_points=None, z_points=None, return_as_list=False):
        """
        Constructs a Z matrix mapping unique (x, y) values to corresponding z values.

        Parameters:
        - x_points (list): List of x coordinates.
        - y_points (list): List of y coordinates.
        - z_points (list): List of z values.
        - return_as_list (bool, optional): Whether to return the matrix as a list. Defaults to False (returns NumPy array).

        Returns:
        - z_matrix (2D list or numpy array): Matrix of z values.
        - unique_x (list): Sorted unique x values.
        - unique_y (list): Sorted unique y values.
        """
        if x_points == None:
            x_points = self.equation_dict['x_points']
        if y_points == None:
            y_points = self.equation_dict['y_points']
        if z_points == None:
            z_points = self.equation_dict['z_points']

        import numpy as np
        # Get unique x and y values
        unique_x = sorted(set(x_points))
        unique_y = sorted(set(y_points))

        # Create an empty matrix filled with NaNs
        z_matrix = np.full((len(unique_x), len(unique_y)), np.nan)

        # Map z values to corresponding x, y indices
        for x, y, z in zip(x_points, y_points, z_points):
            x_idx = unique_x.index(x)
            y_idx = unique_y.index(y)
            z_matrix[x_idx, y_idx] = z

        # Convert to a list if requested
        if return_as_list:
            z_matrix = z_matrix.tolist()

        return z_matrix

    



    def set_num_of_points(self, num_points):
        """
        Set the number of calculation points.
        Expected format: Integer, specifies the number of discrete points for calculations.
        Example: set_num_of_points(10) for ten data points.
        """
        if not isinstance(num_points, int) or num_points <= 0:
            raise ValueError("Number of points must be a positive integer.")
        self.equation_dict["num_of_points"] = num_points

    def set_equation(self, equation_string):
        """Modify the equation string."""
        self.equation_dict['equation_string'] = equation_string

    def get_equation_dict(self):
        """Return the complete equation dictionary."""
        return self.equation_dict
    
    def evaluate_equation(self, remove_equation_fields= False, verbose=False):
        evaluated_dict = evaluate_equation_dict(self.equation_dict, verbose=verbose) #this function is from the evaluator module
        if "graphical_dimensionality" in evaluated_dict:
            graphical_dimensionality = evaluated_dict["graphical_dimensionality"]
        else:
            graphical_dimensionality = 2
        self.equation_dict["x_units"] = evaluated_dict["x_units"]
        self.equation_dict["y_units"] = evaluated_dict["y_units"]
        self.equation_dict["x_points"] = evaluated_dict["x_points"]
        self.equation_dict["y_points"] = evaluated_dict["y_points"]
        if graphical_dimensionality == 3:
            self.equation_dict["z_points"] = evaluated_dict["z_points"]
        if remove_equation_fields == True:
            #we'll just make a fresh dictionary for simplicity, in this case.
            equation_dict = {}
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
            if graphical_dimensionality == 3:
                equation_dict["z_units"] = self.equation_dict["z_units"]
                equation_dict["z_points"] = self.equation_dict["z_points"] 
                print("line 223", equation_dict["z_points"])
            self.equation_dict = equation_dict
        return self.equation_dict

    def print_equation_dict(self, pretty_print=True, evaluate_equation = True, remove_equation_fields = False):
        equation_dict = self.equation_dict #populate a variable internal to this function.
        #if evaluate_equation is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if evaluate_equation == True:
            evaluated_dict = self.evaluate_equation(remove_equation_fields = remove_equation_fields) #For this function, we don't want to remove equation fields from the object, just the export.
            equation_dict = evaluated_dict
        if remove_equation_fields == True:
            equation_dict = {}
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
        if pretty_print == False:
            print(equation_dict)
        if pretty_print == True:
            equation_json_string = json.dumps(equation_dict, indent=4)
            print(equation_json_string)

    def export_to_json_file(self, filename, evaluate_equation = True, remove_equation_fields= False):
        """
        writes the json to a file
        returns the json as a dictionary.
        update_and_validate function will clean for plotly. One can alternatively only validate.
        optionally simulates all series that have a simulate field (does so by default)
        optionally removes simulate filed from all series that have a simulate field (does not do so by default)
        optionally removes hints before export and return.
        """
        equation_dict = self.equation_dict #populate a variable internal to this function.
        #if evaluate_equation is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if evaluate_equation == True:
            evaluated_dict = self.evaluate_equation(remove_equation_fields = remove_equation_fields) #For this function, we don't want to remove equation fields from the object, just the export.
            equation_dict = evaluated_dict
        if remove_equation_fields == True:
            equation_dict = {}
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
        # filepath: Optional, filename with path to save the JSON file.       
        if len(filename) > 0: #this means we will be writing to file.
            # Check if the filename has an extension and append `.json` if not
            if '.json' not in filename.lower():
                filename += ".json"
            #Write to file using UTF-8 encoding.
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(equation_dict, f, indent=4)
        return equation_dict



if __name__ == "__main__":
    # Create an instance of Equation
    example_Arrhenius = Equation()
    example_Arrhenius.set_equation("k = A * (e ** (-Ea / (R * T)))")
    example_Arrhenius.set_x_variable("T (K)")  # Temperature in Kelvin
    example_Arrhenius.set_y_variable("k (s**-1)")  # Rate constant in inverse seconds

    # Add a constants one at a time, or through a list.
    example_Arrhenius.add_constants({"Ea": "30000 J/mol"})  
    example_Arrhenius.add_constants([
        {"R": "8.314 J/(mol*K)"},
        {"A": "1*10**13 (s**-1)"},
        {"e": "2.71828"}  # No unit required
    ])

    # Optinally, set minimum number of points and limits for calculations.
    example_Arrhenius.set_num_of_points(10)
    example_Arrhenius.set_x_range_default([200, 500])
    example_Arrhenius.set_x_range_limits([None, 600])  

    # Define additional properties.
    example_Arrhenius.equation_dict["points_spacing"] = "Linear"

    # Retrieve and display the equation dictionary
    example_equation_dict = example_Arrhenius.get_equation_dict()
    print(example_equation_dict)

    example_Arrhenius.evaluate_equation()
    example_Arrhenius.print_equation_dict()


    #Now for a 3D example.
    example_Arrhenius_3D_dict = {
        'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
        'graphical_dimensionality' : 3,
        'x_variable': 'T (K)',  
        'y_variable': 'Ea (J)*(mol^(-1))',
        'z_variable': 'k (s**(-1))', 
        'constants': {'R': '8.314 (J)*(mol^(-1))*(K^(-1))' , 'A': '1*10^13 (s^-1)', 'e': '2.71828'},
        'num_of_points': 10,
        'x_range_default': [200, 500],
        'x_range_limits' : [],
        'y_range_default': [30000, 50000],
        'y_range_limits' : [],
        'x_points_specified' : [],
        'points_spacing': 'Linear',
        'reverse_scaling' : False
    }

    example_Arrhenius_3D_equation = Equation(initial_dict=example_Arrhenius_3D_dict)
    evaluated_output = example_Arrhenius_3D_equation.evaluate_equation()
    #print(evaluated_output)
    #print(example_Arrhenius_3D_equation.get_z_matrix(return_as_list=True))
