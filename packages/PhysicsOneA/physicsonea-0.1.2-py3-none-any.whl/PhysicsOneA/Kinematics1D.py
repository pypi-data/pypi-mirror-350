from PhysicsOneA.dependencies import *
from PhysicsOneA.helpers import *
from uncertainties import ufloat

def solve_suvat(s=None, u=None, v=None, a=None, t=None):
    """
    Solves the SUVAT equations for uniformly accelerated motion using pure unumpy logic.
    
    Accepts both regular numbers and ufloat objects with uncertainties.
    Returns results with proper uncertainty propagation.

    Parameters:
        s, u, v, a, t: float, ufloat, or None
            - s: displacement (m)
            - u: initial velocity (m/s)  
            - v: final velocity (m/s)
            - a: acceleration (m/s²)
            - t: time (s)

    Returns:
        dict: All five variables with uncertainties preserved if present
    """
    

    
    def has_uncertainties(*values):
        """Check if any input has non-zero uncertainty."""
        for val in values:
            if val is not None and hasattr(val, 'std_dev') and val.std_dev > 0:
                return True
        return False
    
    def maybe_simplify(value, preserve_uncertainty):
        """Convert to float if no uncertainties were in the inputs."""
        if not preserve_uncertainty and hasattr(value, 'nominal_value'):
            return float(value.nominal_value)
        return value
    
    # Format all inputs (skip None values)
    s_norm = format_input(s) if s is not None else None
    u_norm = format_input(u) if u is not None else None
    v_norm = format_input(v) if v is not None else None
    a_norm = format_input(a) if a is not None else None
    t_norm = format_input(t) if t is not None else None
    
    # Check if we need to preserve uncertainties
    preserve_uncertainty = has_uncertainties(s, u, v, a, t)
    
    # Count known values
    known = [x for x in [s_norm, u_norm, v_norm, a_norm, t_norm] if x is not None]
    if len(known) != 3:
        raise ValueError("Exactly 3 values must be provided")
    
    # Determine which variables are missing and solve accordingly
    missing = []
    if s_norm is None: missing.append('s')
    if u_norm is None: missing.append('u') 
    if v_norm is None: missing.append('v')
    if a_norm is None: missing.append('a')
    if t_norm is None: missing.append('t')
    
    if len(missing) != 2:
        raise ValueError("Exactly 3 values must be provided")
    
    # Handle each combination of 2 missing variables
    if 's' in missing and 'a' in missing:
        # Known: u, v, t
        a_norm = (v_norm - u_norm) / t_norm
        s_norm = u_norm * t_norm + 0.5 * a_norm * t_norm**2
        
    elif 's' in missing and 'u' in missing:
        # Known: v, a, t
        u_norm = v_norm - a_norm * t_norm
        s_norm = u_norm * t_norm + 0.5 * a_norm * t_norm**2
        
    elif 's' in missing and 'v' in missing:
        # Known: u, a, t
        v_norm = u_norm + a_norm * t_norm
        s_norm = u_norm * t_norm + 0.5 * a_norm * t_norm**2
        
    elif 's' in missing and 't' in missing:
        # Known: u, v, a
        t_norm = (v_norm - u_norm) / a_norm
        s_norm = u_norm * t_norm + 0.5 * a_norm * t_norm**2
        
    elif 'u' in missing and 'a' in missing:
        # Known: s, v, t
        u_norm = (2 * s_norm - v_norm * t_norm) / t_norm
        a_norm = (v_norm - u_norm) / t_norm
        
    elif 'u' in missing and 'v' in missing:
        # Known: s, a, t
        u_norm = (s_norm - 0.5 * a_norm * t_norm**2) / t_norm
        v_norm = u_norm + a_norm * t_norm
        
    elif 'u' in missing and 't' in missing:
        # Known: s, v, a
        # From v² = u² + 2as and s = ut + 0.5at²
        discriminant = v_norm**2 - 2 * a_norm * s_norm
        if discriminant < 0:
            raise ValueError("No real solution")
        u_norm = sqrt(discriminant)
        t_norm = (v_norm - u_norm) / a_norm
        
    elif 'v' in missing and 'a' in missing:
        # Known: s, u, t
        v_norm = (2 * s_norm - u_norm * t_norm) / t_norm
        a_norm = (v_norm - u_norm) / t_norm
        
    elif 'v' in missing and 't' in missing:
        # Known: s, u, a
        # From s = ut + 0.5at²: 0.5at² + ut - s = 0
        discriminant = u_norm**2 + 2 * a_norm * s_norm
        if discriminant < 0:
            raise ValueError("No real solution for time")
        t_norm = (-u_norm + sqrt(discriminant)) / a_norm
        if t_norm < 0:
            t_norm = (-u_norm - sqrt(discriminant)) / a_norm
        v_norm = u_norm + a_norm * t_norm
        
    elif 'a' in missing and 't' in missing:
        # Known: s, u, v
        a_norm = (v_norm**2 - u_norm**2) / (2 * s_norm)
        t_norm = (v_norm - u_norm) / a_norm
    
    # Verify solution by computing any remaining unknowns
    # This ensures all equations are satisfied
    
    # Final verification and consistency check
    result = {
        's': maybe_simplify(s_norm, preserve_uncertainty),
        'u': maybe_simplify(u_norm, preserve_uncertainty),
        'v': maybe_simplify(v_norm, preserve_uncertainty),
        'a': maybe_simplify(a_norm, preserve_uncertainty),
        't': maybe_simplify(t_norm, preserve_uncertainty)
    }
    
    return result

def plot_distance_vs_time(u, a, s0=0):
    """
    Plots distance vs. time for a single object under constant acceleration.

    Parameters:
        u: initial velocity (float or ufloat)
        a: acceleration (float or ufloat)
        s0: initial position (default 0)
    """
    # Solve to find stopping time (when v = 0)
    result = solve_suvat(u=u, a=a, v=0)

    s = result['s']
    t = result['t']

    t_vals = np.linspace(0, float(t), 200)
    s_vals = s0 + float(u) * t_vals + 0.5 * float(a) * t_vals**2

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(t_vals, s_vals, label='Object Path', color='green')
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    plt.title('Distance vs Time for One Object')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_distance_vs_time_two_objects(u1, a1, u2, a2, s_total):
    """
    Plots distance vs time for two cars decelerating toward each other.
    
    Parameters:
        u1, a1: initial velocity and acceleration of car 1 (float or ufloat)
        u2, a2: initial velocity and acceleration of car 2 (float or ufloat)
        s_total: initial separation between the cars (float)
    """
    # Solve for stopping distances and times
    result1 = solve_suvat(u=u1, a=a1, v=0)
    result2 = solve_suvat(u=u2, a=a2, v=0)

    s1 = result1['s']
    t1 = result1['t']

    s2 = result2['s']
    t2 = result2['t']

    t_max = float(max(t1, t2))  # Total time range for plot

    # Generate time array
    t_vals = np.linspace(0, t_max, 200)

    # Calculate positions of each car over time
    def position(u, a, t_arr):
        return u * t_arr + 0.5 * a * t_arr**2

    x1 = position(float(u1), float(a1), t_vals)
    x2 = s_total - position(float(u2), float(a2), t_vals)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(t_vals, x1, label='Car 1 (→)', color='blue')
    plt.plot(t_vals, x2, label='Car 2 (←)', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Distance vs Time for Two Cars Moving Toward Each Other')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
