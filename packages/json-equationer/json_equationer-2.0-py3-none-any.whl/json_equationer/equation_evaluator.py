from sympy import symbols, Eq, solve, sympify
from pint import UnitRegistry
import re

ureg = UnitRegistry()

def parse_equation(equation_str, variables):
    """Replace variable names and standalone numbers with their magnitudes and formatted units."""
    def detect_and_format_units(equation_str):
        """Detect standalone numbers with units and format them correctly."""
        pattern = r"(\d+(\.\d+)?)\s*([a-zA-Z]+)"
        matches = re.findall(pattern, equation_str)
        # Explanation of regular expression parts
        # (\d+(\.\d+)?)
        #     \d+ → Matches one or more digits (e.g., "10", "100", "3").
        #     (\.\d+)? → Matches optional decimal values (e.g., "10.5", "3.14").
        #     This entire part captures numerical values, whether integers or decimals.
        # \s*
        #     Matches zero or more spaces between the number and the unit.
        #     Ensures flexibility in formatting (e.g., "10m" vs. "10 m").
        # ([a-zA-Z]+)
        #     Matches one or more alphabetical characters, capturing the unit symbol.
        #     Ensures that only valid unit names (e.g., "m", "s", "kg") are recognized.
        # Example Matches
        #     "10 m"   → ("10", "", "m")
        #     "3.5 kg" → ("3.5", ".5", "kg")
        #     "100s"   → ("100", "", "s")
        for match in matches:
            magnitude = match[0]  # Extract number
            unit = match[2]  # Extract unit
            try:
                quantity = ureg(f"{magnitude} {unit}")  # Convert to Pint quantity
                formatted_unit = str(quantity.units)
                equation_str = equation_str.replace(f"{magnitude} {unit}", f"({quantity.magnitude} * {formatted_unit})")
            except: #This comment is so that VS code pylint will not flag this line: pylint: disable=bare-except
                pass  # Ignore invalid unit conversions
        return equation_str


    # Sort variable names by length in descending order
    variables_sorted_by_name = sorted(variables.items(), key=lambda x: -len(x[0]))

    # Need to first replace the constants because they could be like "letter e"
    # and could mess up the string after the units are added in.
    # Also need to sort them by length and replace longer ones first because
    # we could have "Ea" and "a", for example.  
    for var_name, var_value in variables_sorted_by_name:  # Removed `.items()`
        if not hasattr(var_value, "magnitude"):  # For constants like "e" with no units  
            equation_str = equation_str.replace(var_name, str(var_value))  # Directly use plain values  

    # Replace variables with their magnitudes and units  
    for var_name, var_value in variables_sorted_by_name:  # Removed `.items()`
        if hasattr(var_value, "magnitude"):  # Ensure it has a magnitude attribute  
            magnitude = var_value.magnitude  
            unit = str(var_value.units)  
            equation_str = equation_str.replace(var_name, f"({magnitude} * {unit})")  

    # Detect and format standalone numbers with units, like "10 m"
    equation_str = detect_and_format_units(equation_str)
    return equation_str

def solve_equation(equation_string, independent_variables_values_and_units, dependent_variable):
    """
        Solve for the specified dependent variable in terms of multiple independent variables.
        # # Example usage
        # independent_variables_values_and_units = {
        #     "x": "2 m / s",
        #     "y": "3 meter"
        # }
        # equation_string = "x * t + y = 10 m"
        # solve_equation(equation_string, independent_variables_values_and_units, dependent_variable="t")
        # It will solve for the value of t. 
        # What is returned is a list of solutions.
        # if there is any "^" in the equation, it will be changed to **

    """
    # Convert string inputs into Pint quantities
    variables = {name: ureg(value) for name, value in independent_variables_values_and_units.items()}
    independent_variables = list(independent_variables_values_and_units.keys())
    # Explicitly define symbolic variables
    symbols_dict = {var: symbols(var) for var in independent_variables_values_and_units.keys()}
    for var in independent_variables:
        symbols_dict[var] = symbols(var)
    symbols_dict[dependent_variable] = symbols(dependent_variable)

    #change any "^" into "**"
    equation_string = equation_string.replace("^","**")
    # Split the equation into left-hand and right-hand sides
    lhs, rhs = equation_string.split("=")

    # Convert both sides to SymPy expressions
    lhs_sympy = sympify(parse_equation(lhs.strip(), variables), locals=symbols_dict, evaluate=False)
    rhs_sympy = sympify(parse_equation(rhs.strip(), variables), locals=symbols_dict, evaluate=False)

    # Create the equation object
    eq_sympy = Eq(lhs_sympy, rhs_sympy)
    # Solve for the dependent variable
    solutions = solve(eq_sympy, symbols_dict[dependent_variable])
    # Extract magnitude and unit separately from SymPy expressions
    separated_solutions = []
    for sol in solutions:
        magnitude, unit = sol.as_coeff_Mul()  # Works for ANY SymPy expression
        separated_solutions.append((magnitude, unit))

    # Format solutions properly with a space between the magnitude and unit
    formatted_solutions = [f"{mag} ({unit})" for mag, unit in separated_solutions]
    #print(f"Solutions for {dependent_variable} in terms of {independent_variables}: {formatted_solutions}")
    return formatted_solutions


def parse_equation_dict(equation_dict):
    def extract_value_units(entry):
        trimmed_entry = entry.strip()  # Remove leading/trailing whitespace
        split_entry = trimmed_entry.split(" ", 1)  # Split on the first space
        if len(split_entry) > 1:
            value = split_entry[0]
            units = split_entry[1] # Everything after the number
            return [value, units]
        else:
            return [float(split_entry[0]), None]  # Handle constants without units

    def extract_constants(constants_dict):
        return {
            name: extract_value_units(value)
            for name, value in constants_dict.items()
        }

    def extract_equation(equation_string):
        variables_list = re.findall(r"([A-Za-z]+)", equation_string)
        return {"equation_string": equation_string, "variables_list": variables_list}

    if 'graphical_dimensionality' in equation_dict:
        graphical_dimensionality = equation_dict['graphical_dimensionality']
    else:
        graphical_dimensionality = 2

    constants_extracted_dict = extract_constants(equation_dict["constants"])
    equation_extracted_dict = extract_equation(equation_dict["equation_string"])
    # x_match = re.match(r"([\w\d{}$/*_°α-ωΑ-Ω]+)\s*\(([\w\d{}$/*_°α-ωΑ-Ω]*)\)", equation_dict["x_variable"])
    # y_match = re.match(r"([\w\d{}$/*_°α-ωΑ-Ω]+)\s*\(([\w\d{}$/*_°α-ωΑ-Ω]*)\)", equation_dict["y_variable"])
    # x_match  = (x_match.group(1), x_match.group(2)) if x_match else (equation_dict["x_variable"], None)
    # y_match = (y_match.group(1), y_match.group(2)) if y_match else (equation_dict["y_variable"], None)
    x_match = extract_value_units(equation_dict["x_variable"])
    y_match = extract_value_units(equation_dict["y_variable"])
    if graphical_dimensionality == 3:
        z_match = extract_value_units(equation_dict["z_variable"])

    # Create dictionaries for extracted variables
    x_variable_extracted_dict = {"label": x_match[0], "units": x_match[1]}
    y_variable_extracted_dict = {"label": y_match[0], "units": y_match[1]}
    if graphical_dimensionality == 3:
        z_variable_extracted_dict = {"label": z_match[0], "units": z_match[1]}

    def prepare_independent_variables(constants_extracted_dict):
        independent_variables_dict = {
            name: f"{value} {units}" if units else f"{value}"
            for name, (value, units) in constants_extracted_dict.items()
        }
        return independent_variables_dict
    independent_variables_dict = prepare_independent_variables(constants_extracted_dict)

    if graphical_dimensionality == 2:
        return independent_variables_dict, constants_extracted_dict, equation_extracted_dict, x_variable_extracted_dict, y_variable_extracted_dict
    if graphical_dimensionality == 3:
        return independent_variables_dict, constants_extracted_dict, equation_extracted_dict, x_variable_extracted_dict, y_variable_extracted_dict, z_variable_extracted_dict

# equation_dict = {
#     'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
#     'x_variable': 'T (K)',  
#     'y_variable': 'k (s**(-1))',
#     'constants': {'Ea': '30000 (J)*(mol^(-1))', 'R': '8.314 (J)*(mol^(-1))*(K^(-1))' , 'A': '1E13 (s**-1)', 'e': '2.71828'},
#     'num_of_points': 10,
#     'x_range_default': [200, 500],
#     'x_range_limits' : [],
#     'points_spacing': 'Linear'
# }

# try:
#     result_extracted = parse_equation_dict(equation_dict)
#     print(result_extracted)
# except ValueError as e:
#     print(f"Error: {e}")


def generate_multiplicative_points(range_min, range_max, num_of_points=None, factor=None, reverse_scaling=False):
    """
    Generates a sequence of points using relative spacing within a normalized range.
    
    - Spacing between points changes multiplicatively (e.g., doubling means each interval doubles).
    - Returns range_min and range_max explicitly in all cases.
    - Works for negative values and cases where min is negative while max is positive.
    - If `reverse_scaling` is True, exponential scaling occurs from the max end instead.

    Parameters:
    - range_min (float): The starting value of the sequence.
    - range_max (float): The maximum limit for generated values.
    - num_of_points (int, optional): Desired number of points (excluding min/max).
    - factor (float, optional): Multiplication factor for spacing between successive values.
    - reverse_scaling (bool, optional): If True, spacing is applied in reverse direction.

    Returns:
    - List of generated points (standard Python floats).

    Raises:
    - ValueError: If neither num_of_points nor factor is provided.
    """

    # Define normalized bounds
    relative_min = 0
    relative_max = 1
    total_value_range = range_max - range_min  

    # Case 1: num_of_points is provided (factor may be provided too)
    if num_of_points is not None and num_of_points > 1:
        
        # Case 1a: Generate points using equal spacing in relative space
        equal_spacing_list = [relative_min]  # Start at normalized min
        equal_spacing_value = (relative_max - relative_min) / (num_of_points - 1)  # Normalized step size

        for step_index in range(1, num_of_points):
            equal_spacing_list.append(relative_min + step_index * equal_spacing_value)

        # Case 1b: Generate points using multiplication factor (if provided)
        factor_spacing_list = [relative_min]
        if factor is not None and factor > 0:
            relative_spacing = 0.01  # Start at 1% of the range (normalized units)
            current_position = relative_min

            while current_position + relative_spacing < relative_max:
                current_position += relative_spacing
                factor_spacing_list.append(current_position)
                relative_spacing *= factor  # Multiply spacing by factor

        # Compare list lengths explicitly and select the better approach
        if len(factor_spacing_list) > len(equal_spacing_list):
            normalized_points = factor_spacing_list
        else:
            normalized_points = equal_spacing_list

    # Case 2: Only factor is provided, generate points using the multiplication factor
    elif factor is not None and factor > 0:
        relative_spacing = 0.01  # Start at 1% of the range
        current_position = relative_min
        normalized_points = [relative_min]

        while current_position + relative_spacing < relative_max:
            current_position += relative_spacing
            normalized_points.append(current_position)
            relative_spacing *= factor  # Multiply spacing by factor

    # Case 3: Neither num_of_points nor factor is provided, compute equal spacing dynamically
    elif num_of_points is None and factor is None:
        equal_spacing_value = (relative_max - relative_min) / 9  # Default to 9 intermediate points
        normalized_points = [relative_min + step_index * equal_spacing_value for step_index in range(1, 9)]

    # Case 4: Invalid input case—neither num_of_points nor factor is properly set
    else:
        raise ValueError("Either num_of_points or factor must be provided.")

    # Ensure the last relative point is relative_max before scaling
    if normalized_points[-1] != relative_max:
        normalized_points.append(relative_max)

    # Scale normalized points back to the actual range
    if reverse_scaling:
        scaled_points = [range_max - ((relative_max - p) * total_value_range) for p in normalized_points]  # Reverse scaling adjustment
    else:
        scaled_points = [range_min + (p * total_value_range) for p in normalized_points]

    return scaled_points

# # Example usages
# print("line 224")
# print(generate_multiplicative_points(0, 100, num_of_points=10, factor=2))  # Default exponential scaling from min end
# print(generate_multiplicative_points(0, 100, num_of_points=10, factor=2, reverse_scaling=True))  # Exponential scaling from max end
# print(generate_multiplicative_points(1, 100, num_of_points=10, factor=1.3)) # Compares num_of_points vs factor, chooses whichever makes more points
# print(generate_multiplicative_points(1, 100, num_of_points=10))            # Computes factor dynamically
# print(generate_multiplicative_points(1, 100, factor=2))                    # Uses factor normally
# print(generate_multiplicative_points(1, 100))                               # Uses step_factor for default 10 points with 8 intermediate values
# print("line 228")


# # Example usages with reverse scaling
# print("line 240")
# print(generate_multiplicative_points(-50, 100, num_of_points=10, factor=2))  # Case 1b: Uses spacing factor with num_of_points
# print(generate_multiplicative_points(-50, 100, num_of_points=10, factor=2, reverse_scaling=True))  # Reverse scaling version
# print(generate_multiplicative_points(-100, -10, num_of_points=5, factor=1.5)) # Case 1b: Works with negatives
# print(generate_multiplicative_points(-25, 75, num_of_points=7))               # Case 1a: Computes spacing dynamically
# print(generate_multiplicative_points(-10, 50, factor=1.3))                    # Case 2: Uses factor-based spacing
# print(generate_multiplicative_points(-30, 30))                                # Case 3: Uses default intermediate spacing

def generate_points_by_spacing(num_of_points=10, range_min=0, range_max=1, points_spacing="linear"):
    """
    Generates a sequence of points based on the specified spacing method.
    
    Supported spacing types:
    - "linear": Evenly spaced values between range_min and range_max.
    - "logarithmic": Logarithmically spaced values.
    - "exponential": Exponentially increasing values.
    - A real number > 0: Used as a multiplication factor to generate values.
    
    Parameters:
    - num_of_points (int): The number of points to generate. Default is 10.
    - range_min (float): The starting value of the sequence. Default is 1.
    - range_max (float): The maximum limit for generated values. Default is 100.
    - points_spacing (str or float): Defines the spacing method or multiplication factor.
    
    Returns:
    - List of generated points.
    
    Raises:
    - ValueError: If an unsupported spacing type is provided.
    """
    import numpy as np  # Ensure numpy is imported
    spacing_type = str(points_spacing).lower() if isinstance(points_spacing, str) else None
    points_list = None
    if num_of_points == None:
        num_of_points = 10
    if range_min == None:
        range_min = 0
    if range_max == None:
        range_max = 1
    if str(spacing_type).lower() == "none":
        spacing_type = "linear"
    if spacing_type == "":
        spacing_type = "linear"
    if spacing_type.lower() == "linear":
        points_list = np.linspace(range_min, range_max, num_of_points).tolist()
    elif spacing_type.lower() == "logarithmic":
        points_list = np.logspace(np.log10(range_min), np.log10(range_max), num_of_points).tolist()
    elif spacing_type.lower() == "exponential":
        points_list = (range_min * np.exp(np.linspace(0, np.log(range_max/range_min), num_of_points))).tolist()
    elif isinstance(points_spacing, (int, float)) and points_spacing > 0:
        points_list = generate_multiplicative_points(range_min, range_max, points_spacing, num_of_points)
    else:
        raise ValueError(f"Unsupported spacing type: {points_spacing}")

    return points_list


# # Example usage demonstrating different spacing types:
# print(generate_points_by_spacing(num_of_points=10, range_min=1, range_max=100, points_spacing="linear"))         # Linear spacing
# print(generate_points_by_spacing(num_of_points=10, range_min=1, range_max=100, points_spacing="logarithmic"))    # Logarithmic spacing
# print(generate_points_by_spacing(num_of_points=10, range_min=1, range_max=100, points_spacing="exponential"))    # Exponential spacing
# print(generate_points_by_spacing(num_of_points=10, range_min=1, range_max=100, points_spacing=2))               # Multiplicative factor spacing


def generate_points_from_range_dict(range_dict, variable_name="x"):
    """
    Extracts the necessary range and parameters from range_dict and generates a sequence of points.
    In practice, the range_dict can be a full equation_dict with extra fields that will not be used.

    The function follows these rules:
    1. If '{variable_name}_range_limits' is provided as a list of two numbers, it is used as the range.
    2. Otherwise, '{variable_name}_range_default' is used as the range.
    3. Calls generate_points_by_spacing() to generate the appropriate sequence based on num_of_points and points_spacing.

    Parameters:
    - range_dict (dict): Dictionary containing equation details, including range limits, num_of_points, and spacing type.
    - variable_name (str, optional): Name of the variable to determine the range settings. Defaults to 'x'.

    Returns:
    - List of generated points.
    """
    range_default_key = f"{variable_name}_range_default"
    range_limits_key = f"{variable_name}_range_limits"

    # Assigning range. 
    # Start with default values
    if range_dict.get(range_default_key):  # get prevents crashing if the field is not present.
        range_min, range_max = range_dict[range_default_key]

    # If '{variable_name}_range_limits' is provided, update values only if they narrow the range
    if range_dict.get(range_limits_key):
        limit_min, limit_max = range_dict[range_limits_key]
        # Apply limits only if they tighten the range
        if limit_min is not None and limit_min > range_min:
            range_min = limit_min
        if limit_max is not None and limit_max < range_max:
            range_max = limit_max

    # Ensure at least one valid limit exists
    if range_min is None or range_max is None:
        raise ValueError(f"At least one min and one max must be specified between {variable_name}_range_default and {variable_name}_range_limits.")

    list_of_points = generate_points_by_spacing(
        num_of_points=range_dict['num_of_points'],
        range_min=range_min,
        range_max=range_max,
        points_spacing=range_dict['points_spacing']
    )
    # Generate points using the specified spacing method
    return list_of_points


## Start of Portion of code for parsing out tagged ustom units and returning them ##

def return_custom_units_markup(units_string, custom_units_list):
    """puts markup around custom units with '<' and '>' """
    sorted_custom_units_list = sorted(custom_units_list, key=len, reverse=True)
    #the units should be sorted from longest to shortest if not already sorted that way.
    for custom_unit in sorted_custom_units_list:
        units_string = units_string.replace(custom_unit, '<'+custom_unit+'>')
    return units_string

def extract_tagged_strings(text):
    """Extracts tags surrounded by <> from a given string. Used for custom units.
       returns them as a list sorted from longest to shortest"""
    list_of_tags = re.findall(r'<(.*?)>', text)
    set_of_tags = set(list_of_tags)
    sorted_tags = sorted(set_of_tags, key=len, reverse=True)
    return sorted_tags

##End of Portion of code for parsing out tagged ustom units and returning them ##



#This function is to convert things like (1/bar) to (bar)**(-1)
#It was written by copilot and refined by further prompting of copilot by testing.
#The depth is because the function works iteratively and then stops when finished.
def convert_inverse_units(expression, depth=100):
    # Patterns to match valid reciprocals while ignoring multiplied units, so (1/bar)*bar should be  handled correctly.
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

#This support function is just for code readability.
#It returnts two strings in a list, split at the first delimiter.
def split_at_first_delimiter(string, delimter=" "):
    return string.split(delimter, 1)

#This function takes an equation dict (see examples) and returns the x_points, y_points, and x_units and y_units.
#If there is more than one solution (like in a circle, for example) all solutions should be returned.
#The function is slow. I have checked what happens if "vectorize" is used on the x_point loop (which is the main work)
#and the function time didn't change. So the functions it calls must be where the slow portion is.
#I have not timed the individual functions to find and diagnose the slow step(s) to make them more efficient.
#Although there is lots of conversion between different object types to support the units format flexiblity that this function has,
#I would still expect the optimzed code to be an order of magnitude faster. So it may be worth finding the slow steps.
#One possibility might be to use "re.compile()"
def evaluate_equation_dict(equation_dict):
    #First a block of code to extract the x_points needed
    # Extract each dictionary key as a local variable
    equation_string = equation_dict['equation_string']
    if 'graphical_dimensionality' in equation_dict:
        graphical_dimensionality = equation_dict['graphical_dimensionality']
        graphical_dimensionality_added = False
    else: #assume graphical_dimensionality is 2 if one is not provided.
        equation_dict['graphical_dimensionality'] = 2
        graphical_dimensionality_added = True
        graphical_dimensionality = 2
        
    # We don't need the below variables, because they are in the equation_dict.
    # x_variable = equation_dict['x_variable']
    # y_variable = equation_dict['y_variable']
    # constants = equation_dict['constants']
    # reverse_scaling = equation_dict['reverse_scaling']
    x_points = generate_points_from_range_dict(range_dict = equation_dict, variable_name='x')
    if graphical_dimensionality == 3: #for graphical_dimensionality of 3, the y_points are also an independent_variable to generate.
        y_points = generate_points_from_range_dict(range_dict = equation_dict, variable_name='y')

    #Now get the various variables etc.
    if graphical_dimensionality == 2:
        independent_variables_dict, constants_extracted_dict, equation_extracted_dict, x_variable_extracted_dict, y_variable_extracted_dict = parse_equation_dict(equation_dict=equation_dict)
        constants_extracted_dict, equation_extracted_dict #These will not be used. The rest of this comment is to avoid a vs code pylint flag. # pylint: disable=unused-variable, disable=pointless-statement
    elif graphical_dimensionality == 3:
        independent_variables_dict, constants_extracted_dict, equation_extracted_dict, x_variable_extracted_dict, y_variable_extracted_dict, z_variable_extracted_dict = parse_equation_dict(equation_dict=equation_dict)
        constants_extracted_dict, equation_extracted_dict #These will not be used. The rest of this comment is to avoid a vs code pylint flag. # pylint: disable=unused-variable, disable=pointless-statement
    else:
        raise ValueError("Error: graphical_dimensionality not received and/or not evaluatable by current code.")

    #Start of block to check for any custom units and add them to the ureg if necessary.
    custom_units_list = []
    for constant_entry_key in independent_variables_dict.keys():
        independent_variables_string = independent_variables_dict[constant_entry_key]
        custom_units_extracted = extract_tagged_strings(independent_variables_string)
        for custom_unit in custom_units_extracted: #this will be skipped if the list is empty.
            ureg.define(f"{custom_unit} = [custom]") #use "[custom]" to create a custom unit in the pint module.
        custom_units_list.extend(custom_units_extracted)
      
    #now also check for the x_variable_extracted_dict 
    custom_units_extracted = extract_tagged_strings(x_variable_extracted_dict["units"])
    for custom_unit in custom_units_extracted: #this will be skipped if the list is empty.
        ureg.define(f"{custom_unit} = [custom]") #use "[custom]" to create a custom unit in the pint module.
    custom_units_list.extend(custom_units_extracted)

    #now also check for the y_variable_extracted_dict (technically not needed)
    custom_units_extracted = extract_tagged_strings(y_variable_extracted_dict["units"])
    for custom_unit in custom_units_extracted: #this will be skipped if the list is empty.
        ureg.define(f"{custom_unit} = [custom]") #use "[custom]" to create a custom unit in the pint module.
    custom_units_list.extend(custom_units_extracted)

    if graphical_dimensionality == 3:
        #now also check for the z_variable_extracted_dict (technically not needed)
        custom_units_extracted = extract_tagged_strings(z_variable_extracted_dict["units"])
        for custom_unit in custom_units_extracted: #this will be skipped if the list is empty.
            ureg.define(f"{custom_unit} = [custom]") #use "[custom]" to create a custom unit in the pint module.
        custom_units_list.extend(custom_units_extracted)

    #now also check for the equation_string
    custom_units_extracted = extract_tagged_strings(equation_string)
    for custom_unit in custom_units_extracted: #this will be skipped if the list is empty.
        ureg.define(f"{custom_unit} = [custom]") #use "[custom]" to create a custom unit in the pint module.
    custom_units_list.extend(custom_units_extracted)        
    
    #now sort from longest to shortest, since we will have to put them back in that way later.
    custom_units_list = sorted(custom_units_list, key=len, reverse=True)
    #End of block to check for any custom units and add them to the ureg if necessary.

    #For graphical_dimensionality of 2, The full list of independent variables includes the x_variable and the independent_variables. 
    independent_variables = list(independent_variables_dict.keys())#.append(x_variable_extracted_dict['label'])
    independent_variables.append(x_variable_extracted_dict['label'])
    if graphical_dimensionality == 3: #for graphical_dimensionality of 3, the y_variable is also an independent variable.
        independent_variables.append(y_variable_extracted_dict['label'])

    #Now define the dependent variable:
    if graphical_dimensionality == 2:
        dependent_variable = y_variable_extracted_dict["label"]
    elif graphical_dimensionality == 3:
        dependent_variable = z_variable_extracted_dict["label"]
    else:
        raise ValueError("Error: graphical_dimensionality not received and/or not evaluatable by current code.")
    solved_coordinates_list = [] #These are x,y pairs or x,y,z triplets. can't just keep y_points, because there could be more than one solution.
    y_units = ''#just initializing.
    dependent_variable_units = '' #just initializing.

    if graphical_dimensionality == 2:
        input_points_list = x_points #currently a list of points [1,2,3]
        #nested_x_points = [[x] for x in input_points_list] #this way could have  [ [x1],[x2],...]
    elif graphical_dimensionality == 3:
        import itertools
        input_points_list = list(itertools.product(x_points, y_points))  #[ [x1,y1], [x1,y2] ]        
    else:
        raise ValueError("Error: graphical_dimensionality not received and/or not evaluatable by current code.")

    for current_point in input_points_list:
        #For each point, need to call the "solve_equation" equation (or a vectorized version of it).
        #This is the form that the variables need to take
        # # Example usage
        # independent_variables_values_and_units = {
        #     "x": "2 m / s",
        #     "y": "3 meter"
        # }
        # We also need to define the independent variables and dependent variables.
        if graphical_dimensionality == 2:
            independent_variables_dict[x_variable_extracted_dict["label"]] = str(current_point) + " " + x_variable_extracted_dict["units"]
        if graphical_dimensionality == 3:
            independent_variables_dict[x_variable_extracted_dict["label"]] = str(current_point[0]) + " " + x_variable_extracted_dict["units"]
            independent_variables_dict[y_variable_extracted_dict["label"]] = str(current_point[1]) + " " + y_variable_extracted_dict["units"]
        #if graphical_dimensionality is 2D, dependent_variable_solutions is y_solutions. 
        #if graphical_dimensionality is 3D, dependent_variable_solutions is z_solutions. 
        dependent_variable_solutions = solve_equation(equation_string, independent_variables_values_and_units=independent_variables_dict, dependent_variable=dependent_variable)
        if dependent_variable_solutions:
            for dependent_variable_point_with_units in dependent_variable_solutions:
                if graphical_dimensionality == 2:
                    y_point = float(dependent_variable_point_with_units.split(" ", 1)[0]) #the 1 splits only at first space.
                    solved_coordinates_list.append([current_point, y_point])
                    if dependent_variable_units == '': #only extract units the first time.
                        y_units = dependent_variable_point_with_units.split(" ", 1)[1] #the 1 splits only at first space.
                if graphical_dimensionality == 3:
                    z_point = float(dependent_variable_point_with_units.split(" ", 1)[0]) #the 1 splits only at first space.
                    solved_coordinates_list.append([current_point[0],current_point[1], z_point])
                    if dependent_variable_units == '': #only extract units the first time.
                        z_units = dependent_variable_point_with_units.split(" ", 1)[1] #the 1 splits only at first space.
                
    #now need to convert the x_y_pairs.
    # Separating x and y points
    if graphical_dimensionality == 2:
        x_points, y_points = zip(*solved_coordinates_list)
    elif graphical_dimensionality == 3:
        x_points, y_points, z_points = zip(*solved_coordinates_list)

    # Convert tuples to lists
    x_points = list(x_points)
    y_points = list(y_points)
    if graphical_dimensionality == 3:
        z_points = list(z_points)
  
    #Some lines to ensure units are appropriate format before doing any inverse units conversions.
    if graphical_dimensionality == 2:
        x_units = x_variable_extracted_dict["units"]
        if "(" not in x_units:
            x_units = "(" + x_units + ")"
        if "(" not in y_units:
            y_units = "(" + y_units + ")"

    if graphical_dimensionality == 3:
        x_units = x_variable_extracted_dict["units"]
        y_units = y_variable_extracted_dict["units"]
        if "(" not in x_units:
            x_units = "(" + x_units + ")"
        if "(" not in y_units:
            y_units = "(" + y_units + ")"
        if "(" not in z_units:
            z_units = "(" + z_units + ")"

    y_units = convert_inverse_units(y_units)
    x_units = convert_inverse_units(x_units)
    if graphical_dimensionality == 3:
        z_units = convert_inverse_units(z_units)

    #Put back any custom units tags, only needed for dependent variable.
    if graphical_dimensionality == 2:
        y_units = return_custom_units_markup(y_units, custom_units_list)
    if graphical_dimensionality == 3:
        z_units = return_custom_units_markup(z_units, custom_units_list)

    #Fill the dictionary that will be returned.
    evaluated_dict = {}
    evaluated_dict['graphical_dimensionality'] = graphical_dimensionality
    evaluated_dict['x_units'] = x_units
    evaluated_dict['y_units'] = y_units
    evaluated_dict['x_points'] = x_points
    evaluated_dict['y_points'] = y_points
    if graphical_dimensionality == 3:
        z_units = return_custom_units_markup(z_units, custom_units_list)
        evaluated_dict['z_units'] = z_units
        evaluated_dict['z_points'] = z_points
    if graphical_dimensionality_added == True: #undo adding graphical_dimensionality if it was added by this function.
        equation_dict.pop("graphical_dimensionality")
    return evaluated_dict

if __name__ == "__main__":
    #Here is a 2D example:
    example_equation_dict = {
        'equation_string': 'k = A*(e**((-Ea)/(R*T)))',
        'x_variable': 'T (K)',  
        'y_variable': 'k (s**(-1))',
        'constants': {'Ea': '30000 (J)*(mol^(-1))', 'R': '8.314 (J)*(mol^(-1))*(K^(-1))' , 'A': '1*10^13 (s^-1)', 'e': '2.71828'},
        'num_of_points': 10,
        'x_range_default': [200, 500],
        'x_range_limits' : [],
        'x_points_specified' : [],
        'points_spacing': 'Linear',
        'reverse_scaling' : False
    }

    example_evaluated_dict = evaluate_equation_dict(example_equation_dict)
    print(example_evaluated_dict)

    #Here is a 3D example.
    example_equation_dict = {
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

    example_evaluated_dict = evaluate_equation_dict(example_equation_dict)
    print(example_evaluated_dict)

