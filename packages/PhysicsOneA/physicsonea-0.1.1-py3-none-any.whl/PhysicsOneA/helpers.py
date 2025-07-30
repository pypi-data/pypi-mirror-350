from PhysicsOneA.dependencies import *

def format_input(inp: Union[float, int, UFloat]) -> UFloat:
    if isinstance(inp, UFloat):
        return inp
    elif isinstance(inp, (int, float)):
        return ufloat(inp, 0)
    else:
        raise TypeError(f"Unsupported input type: {type(inp)}")


def speed_converter(value, from_unit='m/s', to_unit='km/h'):
   """
   Convert between km/s, m/h, m/s and km/h.

   Default (no args): m/s to km/h
   
   Parameters:
   value: numeric value to convert
   from_unit: 'm/s' or 'km/h' 
   to_unit: 'm/s' or 'km/h'
   
   Returns: converted value
   """
   if from_unit == to_unit:
       return value
   
   if from_unit == 'm/s' and to_unit == 'km/h':
       return value * 3.6
   elif from_unit == 'km/h' and to_unit == 'm/s':
       return value / 3.6
   else:
       raise ValueError("Units must be 'm/s' or 'km/h'")
   
def gravity(decimalPoints=2):
    return round(9.816012123456, decimalPoints)

def radian_to_degree(angle_rad):
    return degrees(angle_rad)

def degree_to_radian(angle_deg):
    """Convert degrees to radians using umath-compatible value"""
    return format_input(angle_deg) * (format_input(np.pi) / 180)


def calculate_from_angle(angle_deg: float):
    """
    Calculates sin, cos, and tan from a given angle in degrees.
    Uses uncertainties.umath to propagate uncertainty.
    """
    angle_rad = degree_to_radian(angle_deg)

    sin_val = sin(angle_rad)
    cos_val = cos(angle_rad)
    try:
        tan_val = tan(angle_rad)
    except Exception:
        tan_val = None

    print(f"\n--- Results for angle {angle_deg}° ---")
    print(f"sin({angle_deg}) = {sin_val:.4f}")
    print(f"cos({angle_deg}) = {cos_val:.4f}")
    if isclose(nominal_value(cos_val), 0.0, abs_tol=1e-10):
        print("tan is undefined (cos ≈ 0)")
    else:
        print(f"tan({angle_deg}) = {tan_val:.4f}")


def calculate_from_sides(a=None, b=None, c=None):
    """
    Calculates sin, cos, and tan based on known sides of a right triangle.
    Works with uncertain values via the 'uncertainties' module.
    """
    if a is not None:
        a = format_input(a)
    if b is not None:
        b = format_input(b)
    if c is not None:
        c = format_input(c)

    if c is None and a is not None and b is not None:
        c = sqrt(a**2 + b**2)

    if c is None:
        print("Insufficient sides provided.")
        return

    print("\n--- Results from triangle sides ---")
    if a is not None:
        sin_val = a / c
        print(f"sin(v) = {sin_val:.4f}")
    if b is not None:
        cos_val = b / c
        print(f"cos(v) = {cos_val:.4f}")
    if a is not None and b is not None:
        tan_val = a / b
        print(f"tan(v) = {tan_val:.4f}")