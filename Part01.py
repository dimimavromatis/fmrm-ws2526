from manim import *
from manim.utils.rate_functions import ease_out_cubic

class Part01(MovingCameraScene):

    def construct(self):

        """
        # Represents the formula of the exercise value
        title_call = Text("Exercise value of a European Call at T")
        title_call.to_edge(UP)

        self.add(title_call)

        payoff_call_formula = MathTex(
            r"C(T) = -\max(S(T) - X, 0)"
            r"\lim_{S(T)\to\infty} C(T) = -\infty",

        )

        payoff_call_formula.move_to(ORIGIN)

        self.play(
            Write(payoff_call_formula)
        )
        self.wait(2)

        self.play(
            FadeOut(payoff_call_formula, title_call)
        )

        # Represents of the payoff diagram of an european call
        # grid = NumberPlane()
        #self.play(Create(grid))

        #---- Payoff diagram coordinate system ----x
        X = 3 # strike price
        premium = 1
        x_min, x_max = 0, 20
        y_min, y_max = -20, 3

        payoff_axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[y_min, y_max, 5],
            x_length=10,
            y_length=7,
            tips=True,
            axis_config={"include_numbers": False}
        ).to_edge(ORIGIN, buff=1.5)

        payoff_label = payoff_axes.get_axis_labels(
            x_label="S(T)", y_label="Payoff"
        )

        minus_infinity = MathTex(r"-\infty").next_to(
            payoff_axes.c2p(0, payoff_axes.y_range[0]), DOWN, buff=0.2
        )

        payoff_function = payoff_axes.plot(
            lambda s: -max(s - X, 0),
            color=RED
        )

        payoff_dot = Dot(payoff_axes.i2gp(payoff_function.t_min, payoff_function), color=ORANGE)

        payoff_text = Text("Short Call Payoff", font_size=24).next_to(payoff_axes, ORIGIN)

        self.add(minus_infinity, payoff_function, payoff_dot, payoff_axes, payoff_label, payoff_text)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(payoff_dot))

        def update_curve_payoff(mob):
            mob.move_to(payoff_dot.get_center())

        self.camera.frame.add_updater(update_curve_payoff)
        self.play(
            MoveAlongPath(payoff_dot, payoff_function, rate_func=ease_out_cubic, run_time=5)
        )
        self.camera.frame.remove_updater(update_curve_payoff)
        self.play(Restore(self.camera.frame))
        self.wait(3)
        self.play(FadeOut(
            minus_infinity, payoff_axes, payoff_label, payoff_function, payoff_text, payoff_dot
        ))
        """
        X = 3
        premium = 1
        x_min, x_max = 0, 20
        y_min, y_max = -20, 3

        # --- 1. Title
        title_call_profit_loss = Text("Short Call Profit/Loss").to_edge(UP)
        # --- 5. Axes and function
        pl_axes = Axes(
            x_range=[x_min, x_max, 3],
            y_range=[y_min, y_max, 5],
            x_length=6,
            y_length=4,
            tips=True,
            axis_config={"include_numbers": False}
        ).to_edge(ORIGIN, buff=0.5)

        self.play(Write(title_call_profit_loss), Create(pl_axes))

        self.wait(0.2)
        self.play(FadeOut(title_call_profit_loss))
        self.play(pl_axes.animate.shift(DOWN))

        # --- 2. Formula
        pl_no_interest = MathTex(
            "PL(T) = C(0) - C(T) =", "C(0) - \max(0, S(T) - X)"
        )
        pl_no_interest.to_corner(UP, buff=0.5)

        self.play(Write(pl_no_interest[0]))
        self.play(Write(pl_no_interest[1]))

        pl_label = pl_axes.get_axis_labels(x_label="S(T)", y_label="PL(T)")
        self.play(Create(pl_label))

        framebox1 = SurroundingRectangle(pl_no_interest[1], buff=0.1)
        self.play(Create(framebox1))
        self.wait(1)

        pl_function = pl_axes.plot(lambda s: premium - max(s - X, 0), color=BLUE)

        self.play(Create(pl_function))

        # --- 3. Limit
        pl_lim = MathTex(r"\lim_{S(T)\to\infty} PL(T) = -\infty")
        pl_lim.next_to(pl_no_interest, DOWN, buff=0.2)
        self.play(Write(pl_lim))
        self.wait(1)

        # --- 4. Highlight parts
        framebox2 = SurroundingRectangle(pl_lim, buff=0.1)
        self.play(ReplacementTransform(framebox1, framebox2))
        self.wait(1)

        self.wait(1)

        # --- 6. Moving dot (first traversal with camera following)
        moving_dot = Dot(pl_axes.i2gp(pl_function.t_min, pl_function), color=ORANGE)
        dot_1 = Dot(pl_axes.i2gp(pl_function.t_min, pl_function))

        minus_infinity = MathTex(r"-\infty").next_to(
            pl_axes.c2p(0, pl_axes.y_range[0]), DOWN, buff=0.2
        )
        plus_infinity = MathTex(r"+\infty").next_to(
            pl_axes.c2p(pl_axes.x_range[1], 0), DOWN, buff=0.2
        )

        self.add(dot_1, moving_dot, minus_infinity, plus_infinity)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def follow_dot(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(follow_dot)
        self.play(MoveAlongPath(moving_dot, pl_function, rate_func=ease_out_cubic, run_time=5))
        self.camera.frame.remove_updater(follow_dot)

        # TODO: Camera needs to restore to normal
        self.play(Restore(self.camera.frame))
        self.wait(1)

        # --- 7. Second traversal (camera stays normal)
        moving_dot.move_to(pl_axes.i2gp(pl_function.t_min, pl_function))  # reset dot
        self.play(MoveAlongPath(moving_dot, pl_function, rate_func=ease_out_cubic, run_time=5))
        self.wait(1)

        call_axes_final = pl_axes.copy()  # copy the call axes
        call_function_final = pl_function.copy()
        call_label_final = pl_label.copy()
        title_call_final = Text("Short Call Profit/Loss").next_to(call_axes_final, UP)

        # --- 8. Done
        self.wait(4)
        self.clear()

        # ------------------------------------
        # Code for Short Put
        # ------------------------------------

        X = 3.0  # strike price
        premium = 1.0
        x_min, x_max = 0, 20
        y_min, y_max = -3, 3  # adjust for short put

        # --- 1. Title
        title_put_profit_loss = Text("Short Put Profit/Loss").to_edge(UP)

        # --- 5. Axes and function
        pl_axes = Axes(
            x_range=[x_min, x_max, 3],
            y_range=[y_min, y_max, 1],
            x_length=6,
            y_length=4,
            tips=True,
            axis_config={"include_numbers": False}
        ).to_edge(ORIGIN, buff=0.5)

        self.play(Write(title_put_profit_loss), Create(pl_axes))
        self.wait(0.2)
        self.play(FadeOut(title_put_profit_loss))
        self.play(pl_axes.animate.shift(DOWN))

        # --- 2. Formula
        pl_no_interest = MathTex(
            "PL(T) = P(0) - P(T) =", "P(0) - \max(0, X - S(T))"
        )
        pl_no_interest.to_corner(UP, buff=0.5)

        self.play(Write(pl_no_interest[0]))
        self.wait(0.5)
        self.play(Write(pl_no_interest[1]))

        pl_label = pl_axes.get_axis_labels(x_label="S(T)", y_label="PL(T)")
        self.play(Create(pl_label))

        framebox1 = SurroundingRectangle(pl_no_interest[1], buff=0.1)
        self.play(Create(framebox1))
        self.wait(1)

        # --- Plot function
        pl_function = pl_axes.plot(lambda s: premium - max(X - s, 0), color=YELLOW)
        self.play(Create(pl_function))

        # --- 3. Limit
        pl_lim = MathTex(r"\lim_{S(T)\to 0} PL(T) = P(0) - X")
        pl_lim.next_to(pl_no_interest, DOWN, buff=0.2)
        self.play(Write(pl_lim))
        self.wait(1)

        # --- 4. Highlight parts
        framebox2 = SurroundingRectangle(pl_lim, buff=0.1)
        self.play(ReplacementTransform(framebox1, framebox2))
        self.wait(1)

        # --- 6. Moving dot (first traversal with camera following)
        moving_dot = Dot(pl_axes.i2gp(pl_function.t_min, pl_function), color=GREEN)
        dot_1 = Dot(pl_axes.i2gp(pl_function.t_min, pl_function))

        minus_infinity = MathTex(r"-\infty").next_to(
            pl_axes.c2p(0, pl_axes.y_range[0]), DOWN, buff=0.2
        )
        plus_infinity = MathTex(r"+\infty").next_to(
            pl_axes.c2p(pl_axes.x_range[1], 0), DOWN, buff=0.2
        )

        self.add(dot_1, moving_dot, minus_infinity, plus_infinity)

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def follow_dot(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(follow_dot)
        self.play(MoveAlongPath(moving_dot, pl_function, rate_func=ease_out_cubic, run_time=5))
        self.camera.frame.remove_updater(follow_dot)

        self.play(Restore(self.camera.frame))
        self.wait(1)

        # --- 7. Second traversal (camera stays normal)
        moving_dot.move_to(pl_axes.i2gp(pl_function.t_min, pl_function))  # reset dot
        self.play(MoveAlongPath(moving_dot, pl_function, rate_func=ease_out_cubic, run_time=5))
        self.wait(4)

        # --- 8. Done
        self.clear()

        # ------------------------------------
        # Both graphs (Shows here both graphs from before next to each other)
        # ------------------------------------

        X = 3
        premium = 1
        x_min, x_max = 0, 20
        y_min_call, y_max_call = -20, 3

        call_axes = Axes(
            x_range=[x_min, x_max, 3],
            y_range=[y_min_call, y_max_call, 5],
            x_length=4.5,
            y_length=3,
            tips=True,
            axis_config={"include_numbers": False}
        ).shift(LEFT * 3.5)

        call_function = call_axes.plot(lambda s: premium - max(s - X, 0), color=BLUE)
        call_label = call_axes.get_axis_labels(x_label="S(T)", y_label="PL(T)")
        call_title = Text("Short Call", font_size=24).next_to(call_axes, DOWN)

        # Recreate Put graph components for right side
        y_min_put, y_max_put = -3, 3

        put_axes = Axes(
            x_range=[x_min, x_max, 3],
            y_range=[y_min_put, y_max_put, 1],
            x_length=4.5,
            y_length=3,
            tips=True,
            axis_config={"include_numbers": False}
        ).shift(RIGHT * 3.5)  # Position on the right

        put_function = put_axes.plot(lambda s: premium - max(X - s, 0), color=YELLOW)
        put_label = put_axes.get_axis_labels(x_label="S(T)", y_label="PL(T)")
        put_title = Text("Short Put", font_size=24).next_to(put_axes, DOWN)

        self.play(
            Create(call_axes),
            Create(call_function),
            Create(call_label),
            Write(call_title),
            Create(put_axes),
            Create(put_function),
            Create(put_label),
            Write(put_title))

        # --- Moving dots ---
        call_dot = Dot(call_axes.i2gp(call_function.t_min, call_function), color=ORANGE)
        put_dot = Dot(put_axes.i2gp(put_function.t_min, put_function), color=GREEN)

        self.add(call_dot, put_dot)

        # First traversal: Animate both dots along their functions simultaneously
        self.play(
            MoveAlongPath(call_dot, call_function, rate_func=ease_out_cubic, run_time=5),
            MoveAlongPath(put_dot, put_function, rate_func=ease_out_cubic, run_time=5)
        )

        # Second traversal: Reset dots and animate again
        call_dot.move_to(call_axes.i2gp(call_function.t_min, call_function))
        put_dot.move_to(put_axes.i2gp(put_function.t_min, put_function))

        self.play(
            MoveAlongPath(call_dot, call_function, rate_func=ease_out_cubic, run_time=5),
            MoveAlongPath(put_dot, put_function, rate_func=ease_out_cubic, run_time=5)
        )




