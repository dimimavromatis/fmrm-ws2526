from manim import *
import numpy as np
from scipy.stats import norm

class Part02(ThreeDScene):

    def construct(self):
        # -------------------------
        # Part 1: Waving Black-Scholes Call Surface (15s)
        # -------------------------

        K = 100
        T = 1
        r = 0.05
        sigma_base = 0.2
        sigma_amp = 0.1  # for the waving amplitude to create wave effect of the surface

        axes = ThreeDAxes(
            x_range=[50, 150, 20],
            y_range=[0, 1, 0.2],
            z_range=[0, 60, 10],
            x_length=7,
            y_length=4,
            z_length=6,
            axis_config={"include_numbers": True}
        )
        axes.shift(OUT * 1)
        axes_labels = axes.get_axis_labels(x_label="S(t)", y_label="t", z_label="C")
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES, distance=12)
        self.renderer.camera.frame_center = axes.get_center()
        title_black_scholes = Text("BSM European Call").to_edge(UP)
        self.add_fixed_in_frame_mobjects(title_black_scholes)
        self.play(FadeIn(title_black_scholes))
        self.add(axes, axes_labels)

        # Black-Scholes formula
        def call_price(S, t, sigma):
            tau = np.maximum(T - t, 1e-5)
            d1 = (np.log(S/K) + (r + 0.5*sigma**2)*tau)/(sigma*np.sqrt(tau))
            d2 = d1 - sigma*np.sqrt(tau)
            return S*norm.cdf(d1) - K*np.exp(-r*tau)*norm.cdf(d2)

        def surface_func(u, v, sigma):
            z = call_price(u, v, sigma)
            return axes.c2p(u, v, z)

        surface = Surface(
            lambda u, v: surface_func(u, v, sigma_base),
            u_range=[50, 150],
            v_range=[0, T],
            resolution=(15, 15),
            fill_opacity=0.8
        )
        surface.set_fill_by_value(axes=axes, colors=[BLUE, GREEN, YELLOW, RED], axis=2)
        self.play(Create(surface), run_time=3)

        sigma_text = always_redraw(
            lambda: Text(
                f"C = C(S, X, T, r, σ={sigma_base + sigma_amp * np.sin(2*np.pi*self.time/5):.3f})",
                font_size=28
            ).to_corner(DR)
        )
        self.add_fixed_in_frame_mobjects(sigma_text)

        def update_surface(mob, dt):
            sigma = sigma_base + sigma_amp * np.sin(2 * np.pi * self.time / 5)
            mob.become(
                Surface(
                    lambda u, v: surface_func(u, v, sigma),
                    u_range=[50, 150],
                    v_range=[0, T],
                    resolution=(15, 15),
                    fill_opacity=0.8
                )
            )
            mob.set_fill_by_value(axes=axes, colors=[BLUE, GREEN, YELLOW, RED], axis=2)

        surface.add_updater(update_surface)

        dot = Dot(color=ORANGE, radius=0.08)
        def update_dot(dot, dt):
            u = 50 + ((self.time * 20) % 100)
            v = (self.time * 0.1) % T
            sigma = sigma_base + sigma_amp * np.sin(2 * np.pi * self.time / 5)
            dot.move_to(surface_func(u, v, sigma))
        dot.add_updater(update_dot)
        self.add(dot)

        self.begin_ambient_camera_rotation(rate=TAU/20)

        self.wait(12)

        self.stop_ambient_camera_rotation()
        surface.remove_updater(update_surface)
        dot.remove_updater(update_dot)

        self.clear()

        #TODO: Need to restore camera here
        self.stop_ambient_camera_rotation()
        self.set_camera_orientation(phi=0, theta=-PI/2)
        self.camera.frame_center = ORIGIN

        # -------------------------
        # Greeks part/section
        # -------------------------
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2

        S = np.linspace(50, 150, 100)
        t_values = [0.05, 0.8]  # near expiry, far from expiry

        # -------------------------
        # Black-Scholes Greek functions
        # -------------------------
        def d1(S, t):
            tau = np.maximum(T - t, 1e-5)
            return (np.log(S / K) + (r + 0.5 * sigma ** 2) * tau) / (sigma * np.sqrt(tau))

        def delta_short(S, t):
            return -norm.cdf(d1(S, t))

        def gamma_short(S, t):
            return -norm.pdf(d1(S, t)) / (S * sigma * np.sqrt(np.maximum(T - t, 1e-5)))

        def vega_short(S, t):
            return -S * norm.pdf(d1(S, t)) * np.sqrt(np.maximum(T - t, 1e-5))

        greeks_short = [("Δ", delta_short), ("Γ", gamma_short), ("ν", vega_short)]
        colors = [BLUE, RED]
        labels_time = ["Far from expiry", "Near expiry"]

        x_offset = -4
        spacing = 4
        x_length = 3
        y_length = 2.5

        # -------------------------
        # Create axes separately
        # -------------------------

        # Delta axes
        y_vals_delta = []
        for t_val in t_values:
            y_vals_delta.extend([delta_short(s, t_val) for s in S])
        y_min_delta = min(y_vals_delta) * 1.1
        y_max_delta = max(y_vals_delta) * 1.1

        axes_delta = Axes(
            x_range=[50, 150, 20],
            y_range=[y_min_delta, y_max_delta, (y_max_delta - y_min_delta) / 5],
            x_length=x_length,
            y_length=y_length,
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(RIGHT * (0 * spacing + x_offset))
        axes_delta_labels = axes_delta.get_axis_labels(x_label="S", y_label=r"\Delta")
        y_label_delta = Text(r"\Delta")
        y_label_delta.next_to(axes_delta.y_axis.get_start(), DOWN, buff=0.2)

        # Gamma axes
        y_vals_gamma = []
        for t_val in t_values:
            y_vals_gamma.extend([gamma_short(s, t_val) for s in S])
        y_max_gamma = max(y_vals_gamma) * 1.1
        y_min_gamma = min(y_vals_gamma) * 1.1

        axes_gamma = Axes(
            x_range=[50, 150, 20],
            y_range=[y_min_gamma, y_max_gamma, (y_max_gamma - y_min_gamma) / 5],
            x_length=x_length,
            y_length=y_length,
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(RIGHT * (1 * spacing + x_offset))
        axes_gamma_labels = axes_gamma.get_axis_labels(x_label="S", y_label=r"\Gamma")

        # Vega axes
        y_vals_vega = []
        for t_val in t_values:
            y_vals_vega.extend([vega_short(s, t_val) for s in S])
        y_max_vega = max(y_vals_vega) * 1.1
        y_min_vega = min(y_vals_vega) * 1.1
        axes_vega = Axes(
            x_range=[50, 150, 20],
            y_range=[y_min_vega, y_max_vega, (y_max_vega - y_min_vega) / 5],
            x_length=x_length,
            y_length=y_length,
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(RIGHT * (2 * spacing + x_offset))
        axes_vega_labels = axes_vega.get_axis_labels(x_label="S", y_label=r"\nu")

        self.play(FadeIn(Text("Greeks").to_edge(UP)))
        self.wait(4)

        # Legend
        legend_items = VGroup()
        for t_val, color, t_label in zip(t_values, colors, labels_time):
            dot = Dot(color=color, radius=0.12)
            text = Text(t_label, font_size=20).next_to(dot, RIGHT, buff=0.1)
            legend_items.add(VGroup(dot, text))
        legend_items.arrange(DOWN, center=False).to_corner(UR)
        self.add(legend_items)

        # -------------------------
        # Display Delta axes
        # -------------------------
        title_delta = Text("Delta").next_to(axes_delta, UP)
        self.add(axes_delta, axes_delta_labels)
        for t_val, color, t_label in zip(t_values, colors, labels_time):
            points = [axes_delta.c2p(s, delta_short(s, t_val)) for s in S]
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_color(color)
            self.play(Create(curve), run_time=1.2)
        self.wait(1)

        # -------------------------
        # Display Gamma axes
        # -------------------------
        title_gamma = Text("Gamma").next_to(axes_gamma, UP)
        self.add(axes_gamma, axes_gamma_labels)
        for t_val, color, t_label in zip(t_values, colors, labels_time):
            points = [axes_gamma.c2p(s, gamma_short(s, t_val)) for s in S]
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_color(color)
            self.play(Create(curve), run_time=1.2)
        self.wait(4.5)

        # -------------------------
        # Display Vega axes
        # -------------------------
        title_vega = Text("Vega").next_to(axes_gamma, UP)
        self.add(axes_vega, axes_vega_labels)
        for t_val, color, t_label in zip(t_values, colors, labels_time):
            points = [axes_vega.c2p(s, vega_short(s, t_val)) for s in S]
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_color(color)
            self.play(Create(curve), run_time=1.2)

        self.wait(25)
