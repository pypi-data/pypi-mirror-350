from PhysicsOneA.dependencies import *
from PhysicsOneA.helpers import *

class Vector:
    def __init__(self, vec: Union[list, 'Vector']):
        if isinstance(vec, Vector):
            self.vec = vec.getVector()
        elif isinstance(vec, list):
            # Convert list to a unumpy array with uncertainties
            self.vec = np.array(vec)
        else:
            raise TypeError("vec must be a list or a Vector instance")

    def getVector(self):
        return self.vec

    def length(self):
        return sqrt(sum(self.vec**2))

    def __str__(self):
        return f"Vector: {self.vec}\nLength: {self.length()}"

class Time:
    def __init__(self,_from: Union[float,UFloat], _to: Union[float,UFloat]):
        self.period = [format_input(_from),format_input(_to)]
    
    def delta_time(self):
        return self.period[1]-self.period[0]

class VectorPair:
    def __init__(self, vec1: Union[list, Vector], vec2: Union[list, Vector]):
        if not isinstance(vec1, (list, Vector)) or not isinstance(vec2, (list, Vector)):
            raise TypeError("vec1 and vec2 must be lists or Vector instances")
        
        self.vec1 = np.array(vec1) if isinstance(vec1, list) else vec1.getVector()
        self.vec2 = np.array(vec2) if isinstance(vec2, list) else vec2.getVector()
    
    def getPair(self):
        return (Vector(self.vec1.tolist()).getVector(), Vector(self.vec2.tolist()).getVector())

    def getVector(self, index=None):
        if index == 0:
            return Vector(self.vec1.tolist()).getVector()
        elif index == 1:
            return Vector(self.vec2.tolist()).getVector()
        else:
            raise ValueError("Index must be 0 or 1")

    def displacement(self):
        return self.vec2 - self.vec1

    def direction_angle(self):
        """
        Calculates the direction angle (α) in degrees between two vectors
        using the arctangent of the displacement's y and x components.

        This angle represents the orientation of the displacement vector 
        from the first vector to the second in 2D space.
        """
        disp = self.displacement()

        if len(disp) < 2:
            raise IndexError("Vectors must have at least two dimensions for angle calculation.")

        Vx = disp[0]
        Vy = disp[1]

        # atan2 handles x=0 case internally, with correct quadrant
        angle_rad = atan2(Vy, Vx)

        return degrees(angle_rad)

    def __str__(self):
        pair = self.getPair()
        return f"Vector Pair:\n  First: {pair[0]}\n  Second: {pair[1]}"

class Projectile:
    def __init__(self, *,
                 v0=None, theta=None,
                 v0x=None, v0y=None,
                 vector=None,
                 vector_pair=None,
                 time_of_flight=None,
                 max_height=None,
                 range_=None,
                 impact_height=None,
                 initial_point=None,
                 target_point=None,
                 apex_point=None,
                 start=None,
                 end=None,
                 y0=0, g=gravity()):
        """
        Initializes a projectile motion object.

        Automatically computes v0, theta, v0x, v0y.

        Supported input combinations:
        1. v0 and theta
        2. v0x and v0y
        3. vector (velocity vector)
        4. vector_pair (displacement vector)
        5. theta and time_of_flight
        6. max_height, range_, and impact_height
        7. max_height and range_
        8. range_ and time_of_flight
        9. initial_point and target_point
        10. range_ and impact_height
        11. apex_point
        12. start, end, and max_height
        """

        self.y0 = format_input(y0)
        self.g = format_input(g)

        if vector is not None:
            vec = vector.getVector()
            self.v0x, self.v0y = vec[0], vec[1]
            self.v0 = sqrt(self.v0x**2 + self.v0y**2)
            self.theta = atan2(self.v0y, self.v0x)

        elif vector_pair is not None:
            disp = vector_pair.displacement()
            self.v0x, self.v0y = disp[0], disp[1]
            self.v0 = sqrt(self.v0x**2 + self.v0y**2)
            self.theta = atan2(self.v0y, self.v0x)

        elif v0 is not None and theta is not None:
            self.v0 = format_input(v0)
            self.theta = format_input(theta)
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)

        elif v0x is not None and v0y is not None:
            self.v0x = format_input(v0x)
            self.v0y = format_input(v0y)
            self.v0 = sqrt(self.v0x**2 + self.v0y**2)
            self.theta = atan2(self.v0y, self.v0x)

        elif theta is not None and time_of_flight is not None:
            self.theta = format_input(theta)
            t = format_input(time_of_flight)
            numerator = 0.5 * self.g * t**2 - self.y0
            denominator = t * sin(self.theta)
            self.v0 = numerator / denominator
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)

        # ✅ NEW: Best match for diver problem (y0, max_height, impact_height, and range)
        elif max_height is not None and range_ is not None and impact_height is not None:
            h = format_input(max_height)
            r = format_input(range_)
            yf = format_input(impact_height)
            dy_up = h - self.y0
            dy_down = h - yf

            # Step 1: vertical velocity from y0 to max height
            self.v0y = sqrt(2 * self.g * dy_up)

            # Step 2: time up and time down
            t_up = self.v0y / self.g
            t_down = sqrt(2 * dy_down / self.g)

            # Step 3: total flight time
            T = t_up + t_down

            # Step 4: horizontal velocity
            self.v0x = r / T

            # Step 5: total speed and angle
            self.v0 = sqrt(self.v0x**2 + self.v0y**2)
            self.theta = atan2(self.v0y, self.v0x)

        elif max_height is not None and range_ is not None:
            h = format_input(max_height)
            r = format_input(range_)
            best_theta = None
            min_error = float('inf')
            for deg in range(500, 860):  # 5.00° to 8.59°
                th = (deg / 100) * (format_input(np.pi) / 180)
                lhs = h / r
                rhs = (sin(th)**2) / (2 * sin(2 * th))
                err = abs(lhs - rhs)
                if err < min_error:
                    best_theta = th
                    min_error = err
            self.theta = best_theta
            self.v0 = sqrt((2 * self.g * h) / (sin(self.theta)**2))
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)

        elif range_ is not None and time_of_flight is not None:
            r = format_input(range_)
            t = format_input(time_of_flight)
            self.v0x = r / t
            self.v0y = (self.g * t) / 2
            self.v0 = sqrt(self.v0x**2 + self.v0y**2)
            self.theta = atan2(self.v0y, self.v0x)

        elif initial_point is not None and target_point is not None:
            dx = format_input(target_point[0] - initial_point[0])
            dy = format_input(target_point[1] - initial_point[1])
            self.theta = atan2(dy, dx)
            self.v0 = sqrt((self.g * dx**2) / (2 * cos(self.theta)**2 * (dx * tan(self.theta) - dy)))
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)

        elif range_ is not None and impact_height is not None:
            r = format_input(range_)
            h = format_input(impact_height)
            best_theta = None
            min_error = float('inf')
            for deg in range(5, 86):
                th = deg * (format_input(np.pi) / 180)
                try:
                    v0 = sqrt((self.g * r**2) / (2 * cos(th)**2 * (r * tan(th) + self.y0 - h)))
                    y_calc = self.y0 + tan(th) * r - (self.g * r**2) / (2 * v0**2 * cos(th)**2)
                    err = abs(y_calc - h)
                    if err < min_error:
                        best_theta, best_v0 = th, v0
                        min_error = err
                except:
                    continue
            self.theta = best_theta
            self.v0 = best_v0
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)

        elif apex_point is not None:
            h = format_input(apex_point[1] - self.y0)
            x_half = format_input(apex_point[0])
            self.theta = atan2(h, x_half)
            self.v0 = sqrt((2 * self.g * h) / (sin(self.theta)**2))
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)

        elif start is not None and end is not None and max_height is not None:
            dx = format_input(end[0] - start[0])
            h = format_input(max_height - start[1])
            self.theta = atan2(h, dx / 2)
            self.v0 = sqrt((2 * self.g * h) / (sin(self.theta)**2))
            self.v0x = self.v0 * cos(self.theta)
            self.v0y = self.v0 * sin(self.theta)
            self.y0 = format_input(start[1])

        else:
            raise ValueError("You must provide a valid input combination to initialize the projectile.")



    def __str__(self):
        return (
            f"--- Projectile Info ---\n"
            f"Initial speed (v0): {self.v0:.4f} m/s\n"
            f"Launch angle (theta): {radian_to_degree(self.theta):.2f}°\n"
            f"Horizontal velocity (v0x): {self.v0x:.4f} m/s\n"
            f"Vertical velocity (v0y): {self.v0y:.4f} m/s\n"
            f"Initial height (y0): {self.y0:.4f} m\n"
            f"Gravity (g): {self.g:.4f} m/s²\n"
            f"\n--- Derived Quantities ---\n"
            f"Time of flight (flat): {self.time_of_flight():.4f} s\n"
            f"Time of flight (realistic): {self.time_of_flight_full():.4f} s\n"
            f"Maximum height: {self.max_height():.4f} m\n"
            f"Range: {self.range():.4f} m"
        )

    def time_of_flight(self):
        return (2 * self.v0y) / self.g


    def time_of_flight_full(self):
        """
        Solves 0 = y0 + v0y * t - 0.5 * g * t²
        Returns the positive root.
        """
        a = -0.5 * self.g
        b = self.v0y
        c = self.y0
        discriminant = b**2 - 4 * a * c

        if nominal_value(discriminant) < 0:
            raise ValueError("Projectile never reaches ground level")

        t1 = (-b + sqrt(discriminant)) / (2 * a)
        t2 = (-b - sqrt(discriminant)) / (2 * a)
        return max(t1, t2)


    def max_height(self):
        return self.y0 + (self.v0y ** 2) / (2 * self.g)


    def range(self):
        return (self.v0 ** 2) * sin(2 * self.theta) / self.g


    def position(self, t, allow_outside=False):
        """
        Returns the position (x, y) of the projectile at time t.

        Parameters:
            t (float): Time in seconds
            allow_outside (bool): If False, raise error if t is outside flight time

        Returns:
            tuple: (x, y) in meters

        Raises:
            ValueError: If t is outside [0, time_of_flight_full()] and allow_outside is False
        """
        t = format_input(t)
        t_max = self.time_of_flight_full()
        if not allow_outside and (nominal_value(t) < 0 or nominal_value(t) > nominal_value(t_max)):
            raise ValueError(f"Time {t} s is outside of projectile's flight time [0, {t_max:.2f}]")

        x = self.v0x * t
        y = self.y0 + self.v0y * t - 0.5 * self.g * t ** 2
        return (x, y)


    def velocity(self, t):
        t = format_input(t)
        vx = self.v0x
        vy = self.v0y - self.g * t
        return (vx, vy)


    def trajectory_y(self, x):
        """Calculates y as a function of x (without time)."""
        x = format_input(x)
        return self.y0 + tan(self.theta) * x - (self.g / (2 * self.v0 ** 2 * cos(self.theta) ** 2)) * x ** 2
    
    # -- Plotting the trajectory --
    def plot_trajectory(self, steps=100):
        t_max = self.time_of_flight()
        times = [i * nominal_value(t_max) / steps for i in range(steps + 1)]
        xs = [nominal_value(self.position(t)[0]) for t in times]
        ys = [nominal_value(self.position(t)[1]) for t in times]

        plt.plot(xs, ys)
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("Projectile Trajectory")
        plt.grid()
        plt.show()

    # -- Plotting y(t) --
    def plot_y_over_time(self, steps=100):
        t_max = self.time_of_flight_full()
        times = [i * nominal_value(t_max) / steps for i in range(steps + 1)]
        ys = [nominal_value(self.position(t)[1]) for t in times]

        plt.plot(times, ys)
        plt.xlabel("Time (s)")
        plt.ylabel("Height y(t) (m)")
        plt.title("Projectile Height Over Time")
        plt.grid()
        plt.show()

    # -- Plotting x(t) --
    def plot_x_over_time(self, steps=100):
        t_max = self.time_of_flight_full()
        times = [i * nominal_value(t_max) / steps for i in range(steps + 1)]
        xs = [nominal_value(self.position(t)[0]) for t in times]

        plt.plot(times, xs)
        plt.xlabel("Time (s)")
        plt.ylabel("Horizontal Distance x(t) (m)")
        plt.title("Projectile Horizontal Position Over Time")
        plt.grid()
        plt.show()

    # -- Plotting velocity components --
    def plot_velocity_over_time(self, steps=100):
        t_max = self.time_of_flight_full()
        times = [i * nominal_value(t_max) / steps for i in range(steps + 1)]
        vxs = [nominal_value(self.velocity(t)[0]) for t in times]
        vys = [nominal_value(self.velocity(t)[1]) for t in times]

        plt.plot(times, vxs, label="vx(t)")
        plt.plot(times, vys, label="vy(t)")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        plt.title("Projectile Velocity Components Over Time")
        plt.legend()
        plt.grid()
        plt.show()

    # -- Return initial velocity vector --
    def get_initial_vector(self):
        return Vector([self.v0x, self.v0y])

    # Position as a function of time (horizontal)
    def x(self, t):
        """
        Returns the horizontal position x(t) in meters at time t (seconds).
        """
        return self.v0x * t

    # Position as a function of time (vertical)
    def y(self, t):
        """
        Returns the vertical position y(t) in meters at time t (seconds), accounting for gravity.
        """
        return self.v0y * t - 0.5 * self.g * t**2 + self.y0

    # Horizontal velocity (constant)
    def vx(self, t):
        """
        Returns the horizontal velocity vx(t) in m/s, which is constant.
        """
        return self.v0x

    # Vertical velocity as a function of time
    def vy(self, t):
        """
        Returns the vertical velocity vy(t) in m/s at time t (seconds), decreasing due to gravity.
        """
        return self.v0y - self.g * t

    # Squared vertical velocity at a given height
    def vy_squared(self, y):
        """
        Returns vy² at a given vertical position y (meters), using energy conservation.
        """
        return self.v0y**2 - 2 * self.g * (y - self.y0)

    # Total speed squared at a given height
    def v_total_squared(self, y):
        """
        Returns total velocity squared v² at a given height y (meters), without using time.
        """
        return self.v0**2 - 2 * self.g * (y - self.y0)

    # Vertical position as a function of horizontal position
    def y_from_x(self, x):
        """
        Returns the vertical position y as a function of horizontal position x (meters).
        This is the trajectory equation y(x) for projectile motion.
        """
        return self.y0 + tan(self.theta) * x - (self.g / (2 * self.v0**2 * cos(self.theta)**2)) * x**2

class CircularMotion:
    def __init__(self, *, r=None, T=None, v=None, v_func=None):
        """
        Circular motion handler.

        Parameters:
            r (float or sympy expression): The radius of the circular path [in meters].
            T (float or sympy expression): The period — the time it takes to complete one full revolution [in seconds].
            v (float or sympy expression): The tangential (linear) velocity of the object [in meters per second].
            v_func (sympy expression): A symbolic expression representing the velocity as a function of time, v(t).
                                       Required to compute tangential acceleration a_T = d|v|/dt.

        You can provide the following combinations:

        - r and T: Used to compute the tangential velocity using the formula:
              v = (2πr) / T

        - v and r: Used to compute the centripetal acceleration using the formula:
              a_c = v² / r

        - v_func: A function of time, used to compute the tangential acceleration:
              a_T = d|v(t)| / dt

        Notes:
            - If only r and T are given, v is computed automatically.
            - If v is given directly, it will be used instead of computing it from r and T.
            - You can leave v_func out unless you're specifically modeling acceleration with time-varying speed.

            v_func example:
            def velocity_func(t):
                return ufloat(3 + 0.5 * t, 0.1)  # velocity in m/s with uncertainty
        """
        self.r = format_input(r) if r is not None else None
        self.T = format_input(T) if T is not None else None
        self.v = format_input(v) if v is not None else None
        self.v_func = v_func

        if self.v is None:
            if self.r is not None and self.T is not None:
                self.v = (2 * format_input(np.pi) * self.r) / self.T
            elif self.r is None:
                raise ValueError("Cannot compute velocity: radius (r) is missing.")
            elif self.T is None:
                raise ValueError("Cannot compute velocity: period (T) is missing.")


    def velocity(self):
        """
        Returns the tangential velocity of the object.

        Formula:
            v = (2πr) / T

        Returns:
            float or UFloat: The velocity v [meters/second, m/s]

        Raises:
            ValueError: If neither v nor both r and T are provided.

        Notes:
            - r is the radius of the circular path [m]
            - T is the period of revolution [s]
        """
        if self.v is not None:
            return self.v
        elif self.r is not None and self.T is not None:
            return (2 * format_input(np.pi) * self.r) / self.T
        else:
            raise ValueError("Missing values: Provide either v, or both r and T.")

    def centripetal_acceleration(self):
        """
        Returns the centripetal acceleration acting on the object.

        Formula:
            a_c = v² / r

        Returns:
            float or UFloat: The centripetal acceleration a_c [m/s²]

        Raises:
            ValueError: If radius r is not provided.

        Notes:
            - v is the tangential velocity [m/s]
            - r is the radius of the circular path [m]
        """
        if self.r is None:
            raise ValueError("Radius r is required to compute centripetal acceleration.")
        v = self.velocity()
        return (v ** 2) / self.r

    def tangential_acceleration(self, t: float, dt: float = 1e-5):
        """
        Returns the tangential acceleration at time t using numerical differentiation.

        Formula:
            a_T = d|v(t)| / dt ≈ (|v(t + dt)| - |v(t)|) / dt

        Parameters:
            t (float): Time at which to evaluate acceleration [s]
            dt (float): Small time step for numerical differentiation [s]

        Returns:
            float or UFloat: Tangential acceleration a_T [m/s²]

        Raises:
            ValueError: If no time-dependent velocity function v(t) is provided.

        Notes:
            - v_func must be a callable returning float or UFloat.
            - Absolute value is used to compute the magnitude of tangential acceleration.
        """
        if self.v_func is None:
            raise ValueError("A time-dependent velocity function v(t) is required for tangential acceleration.")

        v1 = abs(self.v_func(t))
        v2 = abs(self.v_func(t + dt))
        return (v2 - v1) / dt


    def __str__(self):
        def fmt(val, unit):
            try:
                return f"{val.n:.5f} ± {val.s:.5f} {unit}"
            except Exception:
                return "?"

        try:
            v_val = self.velocity()
            v_str = "v = " + fmt(v_val, "m/s")
        except Exception:
            v_str = "v = ?"

        try:
            ac_val = self.centripetal_acceleration()
            ac_str = "centripetal acceleration = " + fmt(ac_val, "m/s²")
        except Exception:
            ac_str = "centripetal acceleration = ?"

        if self.v_func is not None:
            try:
                at_val = self.tangential_acceleration(t=1.0)
                at_str = "tangential acceleration = " + fmt(at_val, "m/s²")
            except Exception:
                at_str = "tangential acceleration = ?"
        else:
            at_str = "tangential acceleration = N/A"

        try:
            T_crit = self.critical_period_for_weightlessness()
            T_crit_hours = T_crit / 3600
            crit_str = (
                f"Critical period for weightlessness: {T_crit.n:.2f} ± {T_crit.s:.2f} seconds "
                f"(~{T_crit_hours.n:.2f} ± {T_crit_hours.s:.2f} hours)"
            )
        except Exception:
            crit_str = "Critical period for weightlessness: ?"

        r_str = fmt(self.r, "m") if self.r is not None else "?"
        T_str = fmt(self.T, "s") if self.T is not None else "?"

        return (
            "--- Circular Motion ---\n"
            f"Radius r: {r_str}\n"
            f"Period T: {T_str}\n"
            f"{v_str}\n"
            f"{ac_str}\n"
            f"{at_str}\n"
            f"{crit_str}"
        )



    
    def critical_period_for_weightlessness(self, g=format_input(gravity())):
        """
        Computes the critical period T [s] at which the centripetal acceleration equals g.

        This is the period at which a person at the equator (or other radius r) would feel weightless,
        due to the required centripetal force matching gravitational acceleration.

        Formula:
            T = sqrt((4 * π² * r) / g)

        Parameters:
            g (float or UFloat): Gravitational acceleration [m/s²]. Default is 9.8.

        Returns:
            float or UFloat: The critical period T in seconds.

        Raises:
            ValueError: If radius r is not provided.
        """
        if self.r is None:
            raise ValueError("Radius r is required to compute the critical period.")
        
        return sqrt((4 * format_input(np.pi)**2 * self.r) / g)
def ensure_vector(v) -> np.ndarray:
    """
    Ensures the input is a NumPy array of UFloat values.
    """
    if isinstance(v, (list, tuple, np.ndarray)):
        v_array = np.array(v, dtype=object)
        return np.array([format_input(x) for x in v_array])
    elif isinstance(v, np.ndarray):
        return v
    else:
        raise TypeError("Expected a list, tuple, or ndarray.")
class RelativeMotion:
    def __init__(self, *,
                 v_ps_prime=None, v_sprime_s=None,
                 a_ps_prime=None, a_sprime_s=None,
                 velocity_vectors=None,
                 acceleration_vectors=None):
        """
        Initializes a relative motion system.

        You may specify relative velocity and/or acceleration using either:
            1. Named arguments:
                - v_ps_prime: Velocity of point P relative to frame S′ [Vector or list of floats]
                - v_sprime_s: Velocity of frame S′ relative to frame S [Vector or list of floats]
                - a_ps_prime: Acceleration of point P relative to frame S′ [Vector or list of floats]
                - a_sprime_s: Acceleration of frame S′ relative to frame S [Vector or list of floats]

            OR

            2. Tuple inputs:
                - velocity_vectors=(v_ps_prime, v_sprime_s)
                - acceleration_vectors=(a_ps_prime, a_sprime_s)

        The resulting object allows you to compute:
            - v_PS = v_PS′ + v_S′S
            - a_PS = a_PS′ + a_S′S
        """

        # Handle velocity input
        if velocity_vectors:
            self.v_ps_prime = ensure_vector(velocity_vectors[0])
            self.v_sprime_s = ensure_vector(velocity_vectors[1])
        else:
            self.v_ps_prime = ensure_vector(v_ps_prime) if v_ps_prime is not None else None
            self.v_sprime_s = ensure_vector(v_sprime_s) if v_sprime_s is not None else None

        # Handle acceleration input
        if acceleration_vectors:
            self.a_ps_prime = ensure_vector(acceleration_vectors[0])
            self.a_sprime_s = ensure_vector(acceleration_vectors[1])
        else:
            self.a_ps_prime = ensure_vector(a_ps_prime) if a_ps_prime is not None else None
            self.a_sprime_s = ensure_vector(a_sprime_s) if a_sprime_s is not None else None

    @property
    def v_ps(self):
        if self.v_ps_prime is not None and self.v_sprime_s is not None:
            return self.v_ps_prime + self.v_sprime_s
        return None

    @property
    def a_ps(self):
        if self.a_ps_prime is not None and self.a_sprime_s is not None:
            return self.a_ps_prime + self.a_sprime_s
        return None

    def relative_velocity(self) -> np.ndarray:
        """
        Calculates the velocity of point P relative to frame S.

        Formula:
            v_PS = v_PS′ + v_S′S

        Returns:
            numpy.ndarray: Resulting relative velocity vector [m/s] with uncertainties

        Raises:
            ValueError: If required velocity vectors are missing.
        """
        if self.v_ps_prime is None or self.v_sprime_s is None:
            raise ValueError("Both v_ps_prime and v_sprime_s must be provided.")

        return self.v_ps_prime + self.v_sprime_s


    def relative_acceleration(self) -> np.ndarray:
        """
        Calculates the acceleration of point P relative to frame S.

        Formula:
            a_PS = a_PS′ + a_S′S

        Returns:
            numpy.ndarray: Resulting relative acceleration vector [m/s²] with uncertainties

        Raises:
            ValueError: If required acceleration vectors are missing.
        """
        if self.a_ps_prime is None or self.a_sprime_s is None:
            raise ValueError("Both a_ps_prime and a_sprime_s must be provided.")

        return self.a_ps_prime + self.a_sprime_s
    
    def _magnitude(self, vec: np.ndarray) -> UFloat:
            """
            Returns the magnitude (Euclidean norm) of a 2D vector with uncertainties.
            """
            return sqrt(vec[0]**2 + vec[1]**2)

    def _angle(self, vec: np.ndarray) -> UFloat:
        """
        Returns the direction (angle in degrees) of a 2D vector with uncertainties.
        Measured from the x-axis (standard polar coordinate convention).
        """
        return degrees(atan2(vec[1], vec[0]))

    def velocity_magnitude(self) -> UFloat:
        return self._magnitude(self.relative_velocity())

    def velocity_angle(self) -> UFloat:
        return self._angle(self.relative_velocity())

    def acceleration_magnitude(self) -> UFloat:
        return self._magnitude(self.relative_acceleration())

    def acceleration_angle(self) -> UFloat:
        return self._angle(self.relative_acceleration())

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the relative motion configuration,
        including computed relative velocity and acceleration with magnitude and direction,
        and human-readable descriptions of each variable.
        """
        def format_vec(name, vec):
            return f"{name} = [{', '.join(str(v) for v in vec)}]"

        lines = ["--- Relative Motion ---", ""]

        # Velocity section
        if self.v_ps_prime is not None and self.v_sprime_s is not None:
            v_result = self.relative_velocity()
            lines += [
                "Velocity Vectors:",
                "  v_PS′  = velocity of point P relative to frame S′",
                format_vec("  v_PS′", self.v_ps_prime),
                "  v_S′S = velocity of frame S′ relative to frame S",
                format_vec("  v_S′S", self.v_sprime_s),
                "  => v_PS = velocity of point P relative to frame S",
                format_vec("  v_PS", v_result),
                f"  ||v_PS|| = {self.velocity_magnitude()} m/s",
                f"  Angle(v_PS) = {self.velocity_angle()}°",
                ""
            ]
        else:
            lines.append("Velocity data incomplete.\n")

        # Acceleration section
        if self.a_ps_prime is not None and self.a_sprime_s is not None:
            a_result = self.relative_acceleration()
            lines += [
                "Acceleration Vectors:",
                "  a_PS′  = acceleration of point P relative to frame S′",
                format_vec("  a_PS′", self.a_ps_prime),
                "  a_S′S = acceleration of frame S′ relative to frame S",
                format_vec("  a_S′S", self.a_sprime_s),
                "  => a_PS = acceleration of point P relative to frame S",
                format_vec("  a_PS", a_result),
                f"  ||a_PS|| = {self.acceleration_magnitude()} m/s²",
                f"  Angle(a_PS) = {self.acceleration_angle()}°",
                ""
            ]
        else:
            lines.append("Acceleration data incomplete.\n")

        return "\n".join(lines)