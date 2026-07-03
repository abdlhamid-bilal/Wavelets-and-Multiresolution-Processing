from manim import *
import numpy as np
from scipy.interpolate import interp1d

np.random.seed(42)
N_points = 256
t_arr = np.linspace(-5, 5, N_points)
t_mapped = (t_arr + 5) / 10 

trend = np.sin(4 * np.pi * t_mapped) 
noise = 0.2 * np.sin(70 * np.pi * t_mapped) 

jump = np.zeros_like(t_arr)
mid_idx = N_points // 2
jump[mid_idx : mid_idx + 5] = 2.0

original_signal = trend + noise + jump

f_interp = interp1d(t_arr, original_signal, bounds_error=False, fill_value=0.0)

def f(x): 
    return f_interp(x)

def phi(x): 
    return np.exp(-np.pi * x**2) 

def psi(x): 
    return (1 - 2 * np.pi * x**2) * np.exp(-np.pi * x**2) 

def phi_jk(x, j, k): 
    return (2**(j / 2)) * phi((2**j) * x - k)

def psi_jk(x, j, k): 
    return (2**(j / 2)) * psi((2**j) * x - k)

class SignalReconstruction(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        left_axes = Axes(x_range=[-5, 5, 1], y_range=[-2, 4, 1], x_length=5.5, y_length=4, axis_config={"color": BLACK})
        right_axes = Axes(x_range=[-5, 5, 1], y_range=[-2, 4, 1], x_length=5.5, y_length=4, axis_config={"color": BLACK})

        VGroup(left_axes, right_axes).arrange(RIGHT, buff=1.0).move_to(ORIGIN)

        f_graph = left_axes.plot(f, color=BLUE, stroke_width=1.5)
        f_label = MathTex("f(x)", font_size=36, color=BLUE).next_to(f_graph, UP, buff=0.2).shift(LEFT * 1.5)
        
        self.play(Create(left_axes), Create(right_axes))
        self.play(Create(f_graph), Write(f_label))
        self.wait(1)

        x_plot = np.linspace(-5, 5, 10000) 
        x_int = np.linspace(-6, 6, 20000)  
        dx = x_int[1] - x_int[0]
        f_int = f(x_int)

        label_pos = right_axes.get_top() + UP * 0.7

        APPROX_COLOR = "#B8860B"  # dark goldenrod
        DETAIL_COLOR = "#8B0000"  # dark red

        k_values = list(range(-5, 6))  # k = -5 to 5

        # ============================
        # PHASE 1: APPROXIMATION
        # ============================

        # Precompute all approximation terms
        approx_coeffs = {}
        for k in k_values:
            approx_coeffs[k] = np.sum(f_int * phi_jk(x_int, 0, k)) * dx

        # Show initial approximation label with k=-12
        def make_approx_label(k_val):
            return MathTex(
                r"\text{Approximation: }",
                r"\sum_{k=" + str(k_val) + r"}^{5}",
                r"c_{0}(" + str(k_val) + r")",
                r"\cdot",
                r"\varphi_{0," + str(k_val) + r"}(x)",
                font_size=28,
                color=APPROX_COLOR,
            ).move_to(label_pos)

        approx_label = make_approx_label(-5)
        self.play(FadeIn(approx_label, shift=DOWN), run_time=0.8)
        self.wait(0.5)

        running_approx = np.zeros_like(x_plot)
        sum_graph = None

        for idx, k in enumerate(k_values):
            c_k = approx_coeffs[k]
            term = c_k * phi_jk(x_plot, 0, k)

            # Update the label to show current k
            new_label = make_approx_label(k)
            self.play(Transform(approx_label, new_label), run_time=0.3)

            # Show the individual term briefly
            term_graph = right_axes.plot_line_graph(
                x_plot, term,
                add_vertex_dots=False, line_color="#006400", stroke_width=2
            )
            self.play(FadeIn(term_graph), run_time=0.3)

            # Merge: add term to running sum
            running_approx = running_approx + term
            new_sum = right_axes.plot_line_graph(
                x_plot, running_approx,
                add_vertex_dots=False, line_color=APPROX_COLOR, stroke_width=2
            )

            if sum_graph is None:
                self.play(ReplacementTransform(term_graph, new_sum), run_time=0.6)
            else:
                self.play(
                    FadeOut(term_graph),
                    ReplacementTransform(sum_graph, new_sum),
                    run_time=0.6,
                )
            sum_graph = new_sum

        # Pause after approximation is done
        self.wait(1.5)

        # Transform approximation graph to black "running total"
        current_sum_array = running_approx.copy()
        black_sum = right_axes.plot_line_graph(
            x_plot, current_sum_array,
            add_vertex_dots=False, line_color=BLACK, stroke_width=2
        )
        self.play(
            ReplacementTransform(sum_graph, black_sum),
            FadeOut(approx_label),
            run_time=1,
        )
        sum_graph = black_sum
        self.wait(1.0)

        # ============================
        # PHASE 2: DETAILS
        # ============================

        colors_j = ["#8B0000", "#004D40", "#4A0080"]  # dark red, dark teal, dark purple

        for j in range(3):  # j = 0, 1, 2
            col = colors_j[j]

            # Precompute all detail terms for this j
            detail_coeffs = {}
            for k in k_values:
                detail_coeffs[k] = np.sum(f_int * psi_jk(x_int, j, k)) * dx

            def make_detail_label(j_val, k_val):
                return MathTex(
                    r"\text{Details: }",
                    r"\sum_{j=" + str(j_val) + r"}^{2}",
                    r"\sum_{k=" + str(k_val) + r"}^{5}",
                    r"d_{" + str(j_val) + r"}(" + str(k_val) + r")",
                    r"\cdot",
                    r"\psi_{" + str(j_val) + r"," + str(k_val) + r"}(x)",
                    font_size=28,
                    color=col,
                ).move_to(label_pos)

            detail_label = make_detail_label(j, -5)
            self.play(FadeIn(detail_label, shift=DOWN), run_time=0.8)
            self.wait(0.5)

            running_detail = np.zeros_like(x_plot)
            detail_graph = None

            for idx, k in enumerate(k_values):
                d_k = detail_coeffs[k]
                term = d_k * psi_jk(x_plot, j, k)

                # Update label with current k
                new_dlabel = make_detail_label(j, k)
                self.play(Transform(detail_label, new_dlabel), run_time=0.3)

                # Show individual term
                term_graph = right_axes.plot_line_graph(
                    x_plot, term,
                    add_vertex_dots=False, line_color="#006400", stroke_width=2
                )
                self.play(FadeIn(term_graph), run_time=0.3)

                # Merge into running detail sum
                running_detail = running_detail + term
                new_detail = right_axes.plot_line_graph(
                    x_plot, running_detail,
                    add_vertex_dots=False, line_color=col, stroke_width=2
                )

                if detail_graph is None:
                    self.play(ReplacementTransform(term_graph, new_detail), run_time=0.6)
                else:
                    self.play(
                        FadeOut(term_graph),
                        ReplacementTransform(detail_graph, new_detail),
                        run_time=0.6,
                    )
                detail_graph = new_detail

            # All k done for this j – merge detail into total sum
            self.wait(1.0)

            current_sum_array = current_sum_array + running_detail
            new_sum = right_axes.plot_line_graph(
                x_plot, current_sum_array,
                add_vertex_dots=False, line_color=BLACK, stroke_width=2
            )
            self.play(
                ReplacementTransform(VGroup(sum_graph, detail_graph), new_sum),
                FadeOut(detail_label),
                run_time=1.5,
            )
            sum_graph = new_sum

            # Pause between j levels
            self.wait(1.5)

        # Final: show perfect reconstruction
        perfect_graph = right_axes.plot_line_graph(
            x_plot, f(x_plot),
            add_vertex_dots=False, line_color=BLUE, stroke_width=3
        )

        self.play(ReplacementTransform(sum_graph, perfect_graph), run_time=2)
        self.wait(2)