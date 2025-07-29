from PhysicsOneA.dependencies import *

def solve_suvat(s=None, u=None, v=None, a=None, t=None):
    """
    Solves the SUVAT equations for uniformly accelerated motion using symbolic computation (SymPy).

    SUVAT equations relate the following five variables in uniformly accelerated motion:
        - s: displacement
        - u: initial velocity
        - v: final velocity
        - a: acceleration
        - t: time

    You must provide **exactly three known values**, and the function will compute the remaining two.

    Parameters:
        s (float or None): Displacement (in meters). Optional.
        u (float or None): Initial velocity (in m/s). Optional.
        v (float or None): Final velocity (in m/s). Optional.
        a (float or None): Acceleration (in m/s²). Optional.
        t (float or None): Time (in seconds). Optional.

    Returns:
        dict: A dictionary containing all five variables {'s': float, 'u': float, 'v': float, 'a': float, 't': float},
              with computed values filled in for the ones that were originally unspecified.

    Raises:
        ValueError: If not exactly three values are provided.
        ValueError: If the system of equations cannot be solved (e.g., inconsistent or unsolvable values).

    Notes:
        - This function uses three standard SUVAT equations:
            1. v = u + at
            2. s = ut + (1/2)at²
            3. v² = u² + 2as
        - The function uses SymPy to solve these equations symbolically.
        - If multiple solutions exist (e.g., time t could be positive or negative), the function selects the positive value if applicable.
        - All returned values are converted to floats.

    Example:
        >>> solve_suvat(u=0, a=2, t=3)
        {'s': 9.0, 'u': 0.0, 'v': 6.0, 'a': 2.0, 't': 3.0}
    """
    # Define symbols
    s_sym, u_sym, v_sym, a_sym, t_sym = symbols('s u v a t', real=True)
    
    # Count known values
    known = [x for x in [s, u, v, a, t] if x is not None]
    if len(known) != 3:
        raise ValueError("Exactly 3 values must be provided")
    
    # SUVAT equations
    eq1 = Eq(v_sym, u_sym + a_sym * t_sym)  # v = u + at
    eq2 = Eq(s_sym, u_sym * t_sym + a_sym * t_sym**2 / 2)  # s = ut + ½at²
    eq3 = Eq(v_sym**2, u_sym**2 + 2 * a_sym * s_sym)  # v² = u² + 2as
    
    equations = [eq1, eq2, eq3]
    variables = [s_sym, u_sym, v_sym, a_sym, t_sym]
    
    # Substitute known values
    substitutions = {}
    if s is not None: substitutions[s_sym] = s
    if u is not None: substitutions[u_sym] = u
    if v is not None: substitutions[v_sym] = v
    if a is not None: substitutions[a_sym] = a
    if t is not None: substitutions[t_sym] = t
    
    # Apply substitutions to equations
    eqs_substituted = [eq.subs(substitutions) for eq in equations]
    
    # Find unknown variables
    unknowns = [var for var in variables if var not in substitutions]
    
    # Solve the system
    try:
        solutions = solve(eqs_substituted, unknowns, dict=True)
        
        if not solutions:
            raise ValueError("No solution found for given values")
        
        # Take first solution (handle multiple solutions by choosing positive time if applicable)
        solution = solutions[0]
        if len(solutions) > 1 and t_sym in unknowns:
            # Choose positive time solution
            for sol in solutions:
                if t_sym in sol and sol[t_sym] >= 0:
                    solution = sol
                    break
        
        # Build result dictionary
        result = {}
        result['s'] = float(solution.get(s_sym, s))
        result['u'] = float(solution.get(u_sym, u))
        result['v'] = float(solution.get(v_sym, v))
        result['a'] = float(solution.get(a_sym, a))
        result['t'] = float(solution.get(t_sym, t))
        
        return result
        
    except Exception as e:
        raise ValueError(f"Could not solve equations: {e}")
