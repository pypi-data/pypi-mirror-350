from PhysicsOneA.dependencies import *
from PhysicsOneA.helpers import *

def spring_force(k, x, x0=0):
    """
    Calculates the spring force using Hooke's Law.

    F = -k * (x - x0)

    Parameters:
        k (float or Quantity): Spring constant [N/m]
        x (float or Quantity): Current position of the spring [m]
        x0 (float or Quantity, optional): Equilibrium/rest position [m]. Defaults to 0.

    Returns:
        float or Quantity: Spring force [N]
    """

    k = format_input(k)
    x = format_input(x)
    x0 = format_input(x0)
    return -k * (x - x0)

def kinetic_friction(mu_k, normal_force):
    """
    Calculates the kinetic friction force.

    f_k = μ_k * N

    Parameters:
        mu_k (float): Coefficient of kinetic friction (unitless)
        normal_force (float or Quantity): Normal force acting on the object [N]

    Returns:
        float or Quantity: Kinetic friction force [N]
    """

    mu_k = format_input(mu_k)
    normal_force = format_input(normal_force)
    return mu_k * normal_force

def static_friction_max(mu_s, normal_force):
    """
    Calculates the maximum possible static friction force.

    f_s ≤ μ_s * N

    Parameters:
        mu_s (float): Coefficient of static friction (unitless)
        normal_force (float or Quantity): Normal force acting on the object [N]

    Returns:
        float or Quantity: Maximum static friction force [N]
    """

    mu_s = format_input(mu_s)
    normal_force = format_input(normal_force)
    return mu_s * normal_force
def general_drag(b, v, n=1):
    """
    Calculates drag force using a general drag model.

    F_d = b * v^n

    Parameters:
        b (float): Drag coefficient (depends on system)
        v (float or Quantity): Velocity [m/s]
        n (int, optional): Power of velocity (1 for linear, 2 for quadratic drag). Defaults to 1.

    Returns:
        float or Quantity: Drag force [N]
    """

    b = format_input(b)
    v = format_input(v)
    return b * v**n

def drag_force(D, v):
    """
    Calculates the drag force based on quadratic drag.

    f = D * v^2

    Parameters:
        D (float): Drag coefficient [kg/m]
        v (float or Quantity): Velocity [m/s]

    Returns:
        float or Quantity: Drag force [N]
    """

    D = format_input(D)
    v = format_input(v)
    return D * v**2

def drag_coefficient(rho, C_D, A):
    """
    Calculates the drag coefficient D used in fluid drag force formulas.

    D = 1/2 * ρ * C_D * A

    Parameters:
        rho (float): Fluid density [kg/m³]
        C_D (float): Dimensionless drag coefficient
        A (float): Cross-sectional area of the object [m²]

    Returns:
        float: Effective drag coefficient D [kg/m]
    """

    rho = format_input(rho)
    C_D = format_input(C_D)
    A = format_input(A)
    return 0.5 * rho * C_D * A

def stokes_drag(radius, viscosity, velocity):
    """
    Calculates the drag force on a small spherical object in a viscous fluid.

    F_s = 6π * η * r * v

    Parameters:
        radius (float): Radius of the sphere [m]
        viscosity (float): Dynamic viscosity of the fluid [Pa·s or N·s/m²]
        velocity (float): Speed of the object [m/s]

    Returns:
        float: Stokes drag force [N]
    """

    eta = format_input(viscosity)
    r = format_input(radius)
    v = format_input(velocity)
    return 6 * np.pi * eta * r * v

def net_force(mass, acceleration):
    """
    Calculates the net force using Newton's Second Law.

    F = m * a

    Parameters:
        mass (float): Mass of the object [kg]
        acceleration (float): Acceleration of the object [m/s²]

    Returns:
        float: Net force [N]
    """

    m = format_input(mass)
    a = format_input(acceleration)
    return m * a

def net_force_from_velocity_change(mass, dv, dt):
    """
    Calculates net force based on change in velocity over time.

    F = m * (dv / dt)

    Parameters:
        mass (float): Mass of the object [kg]
        dv (float): Change in velocity [m/s]
        dt (float): Time interval [s]

    Returns:
        float: Net force [N]
    """

    m = format_input(mass)
    dv = format_input(dv)
    dt = format_input(dt)
    return m * (dv / dt)


def acceleration_of_two_blocks(F, mA, mB, g=gravity()):
    """
    Calculates the acceleration of two blocks being pulled as a system.

    a = (F - (mA + mB) * g) / (mA + mB)

    Parameters:
        F (float): Applied force [N]
        mA (float): Mass of block A [kg]
        mB (float): Mass of block B [kg]
        g (float, optional): Gravitational acceleration [m/s²]. Defaults to Earth's gravity.

    Returns:
        float: Acceleration of the system [m/s²]
    """

    F = format_input(F)
    mA = format_input(mA)
    mB = format_input(mB)
    g = format_input(g)
    total_mass = mA + mB
    return (F - total_mass * g) / total_mass

def tension_in_rope(mB, acceleration, g=gravity()):
    """
    Calculates the tension in a rope pulling a hanging mass.

    T = mB * (a + g)

    Parameters:
        mB (float): Mass of the hanging block [kg]
        acceleration (float): System acceleration [m/s²]
        g (float, optional): Gravitational acceleration [m/s²]

    Returns:
        float: Tension in the rope [N]
    """

    mB = format_input(mB)
    a = format_input(acceleration)
    g = format_input(g)
    return mB * (a + g)

def inclined_plane_acceleration(mass, force, theta_deg, g=gravity()):
    """
    Calculates acceleration of a block pushed up a frictionless incline.

    a = (F * cos(theta)) / m - g * sin(theta)

    Parameters:
        mass (float): Mass of the block [kg]
        force (float): Applied horizontal force [N]
        theta_deg (float): Incline angle [degrees]
        g (float, optional): Gravitational acceleration [m/s²]

    Returns:
        float: Acceleration up the incline [m/s²]
    """

    m = format_input(mass)
    F = format_input(force)
    theta = degree_to_radian(theta_deg)
    g = format_input(g)

    return (F * cos(theta)) / m - g * sin(theta)


def normal_force_on_incline(mass, force, theta_deg, g=gravity()):
    """
    Calculates the normal force on a block on a frictionless incline.

    N = m * g * cos(theta) + F * sin(theta)

    Parameters:
        mass (float): Mass of the block [kg]
        force (float): Applied horizontal force [N]
        theta_deg (float): Incline angle [degrees]
        g (float, optional): Gravitational acceleration [m/s²]

    Returns:
        float: Normal force [N]
    """

    m = format_input(mass)
    F = format_input(force)
    theta = degree_to_radian(theta_deg)
    g = format_input(g)

    return m * g * cos(theta) + F * sin(theta)


def three_block_acceleration(mA, mB, mC, force):
    """
    Calculates acceleration of a system of three connected blocks.

    a = F / (mA + mB + mC)

    Parameters:
        mA (float): Mass of block A [kg]
        mB (float): Mass of block B [kg]
        mC (float): Mass of block C [kg]
        force (float): Applied force [N]

    Returns:
        float: Acceleration of the system [m/s²]
    """

    mA = format_input(mA)
    mB = format_input(mB)
    mC = format_input(mC)
    F = format_input(force)

    total_mass = mA + mB + mC
    return F / total_mass


def tension_bc(mC, acceleration):
    """
    Calculates tension in the rope section between blocks B and C.

    Parameters:
        mC (float): Mass of block C [kg]
        acceleration (float): System acceleration [m/s²]

    Returns:
        float: Tension acting on block C [N]
    """

    mC = format_input(mC)
    a = format_input(acceleration)
    return mC * a


def tension_ab(mB, mC, acceleration):
    """
    Calculates tension between blocks A and B, pulling B and C.

    Parameters:
        mB (float): Mass of block B [kg]
        mC (float): Mass of block C [kg]
        acceleration (float): System acceleration [m/s²]

    Returns:
        float: Tension acting between A and B [N]
    """

    mB = format_input(mB)
    mC = format_input(mC)
    a = format_input(acceleration)
    return (mB + mC) * a

def unstretched_length_of_spring(mass, radius, period, spring_constant):
    """
    Calculates the unstretched length of a spring in uniform circular motion.

    L₀ = R - (m * v²) / (k * R), where v = 2πR / T

    Parameters:
        mass (float): Mass of the object attached to the spring [kg]
        radius (float): Radius of circular motion [m]
        period (float): Period of revolution [s]
        spring_constant (float): Spring constant k [N/m]

    Returns:
        float: Unstretched length of the spring [m]
    """

    m = format_input(mass)
    R = format_input(radius)
    T = format_input(period)
    k = format_input(spring_constant)

    v = (2 * np.pi * R) / T
    return R - (m * v**2) / (k * R)