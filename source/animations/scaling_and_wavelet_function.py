from manim import *
import numpy as np
from scipy.interpolate import interp1d

# --- Signal Definition (Trend + Noise + Jump) ---
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

# Interpolation des diskreten Signals für stetige Manim-Auswertung
f_interp = interp1d(t_arr, original_signal, bounds_error=False, fill_value=0.0)

def f(x): 
    return f_interp(x)

# --- Wavelet Definition (Mexican Hat & Gaussian Scaling) ---
def phi(x): 
    return np.exp(-np.pi * x**2) 

def psi(x): 
    return (1 - 2 * np.pi * x**2) * np.exp(-np.pi * x**2) 

def phi_jk(x, j, k): 
    return (2**(j / 2)) * phi((2**j) * x - k)

def psi_jk(x, j, k): 
    return (2**(j / 2)) * psi((2**j) * x - k)

X_INT = np.linspace(-5, 5, 1000)
DX = X_INT[1] - X_INT[0]


# ==========================================
# ANIMATION 1: (3 Axes)
# ==========================================
class ScalingFunction(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        j = 0  
        k_tracker = ValueTracker(-4)

        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.8, x_length=8.5, axis_config={"color": BLACK})
        axes_mid = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.8, x_length=8.5, axis_config={"color": BLACK})
        axes_bot = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.8, x_length=8.5, axis_config={"color": BLACK})

        VGroup(axes_top, axes_mid, axes_bot).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        top_label = Tex(r"Signal $f(x)$ \& Scaling function $\varphi_{0,k}(x)$", font_size=28, color=BLACK).next_to(axes_top, UP, buff=0.1, aligned_edge=LEFT)
        mid_label = Tex(r"Inner product: $\langle f, \varphi_{0,k} \rangle$", font_size=28, color=BLACK).next_to(axes_mid, UP, buff=0.1, aligned_edge=LEFT)
        bot_label = Tex(r"$c_0(k)$", font_size=28, color=BLACK).next_to(axes_bot, UP, buff=0.1, aligned_edge=LEFT)

        signal_graph = axes_top.plot(f, color=BLUE)
        self.play(
            Create(VGroup(axes_top, axes_mid, axes_bot)),
            Write(VGroup(top_label, mid_label, bot_label)),
            Create(signal_graph)
        )

        j_label = MathTex(r"j_0 = 0 \text{ (fixed)}", font_size=36, color=BLACK).to_corner(UL)
        k_label = always_redraw(lambda: MathTex(f"k = {int(round(k_tracker.get_value()))}", font_size=36, color=BLACK).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        def product_func(x, k): return f(x) * phi_jk(x, j, k)

        scaling_color = "#D4AF37"
        scaling_graph = always_redraw(lambda: axes_top.plot(lambda x: phi_jk(x, j, k_tracker.get_value()), color=scaling_color))
        product_graph = always_redraw(lambda: axes_mid.plot(lambda x: product_func(x, k_tracker.get_value()), color=GREEN))
        shaded_area = always_redraw(lambda: axes_mid.get_area(product_graph, x_range=[-5, 5], color=GREEN).set_opacity(0.5))

        self.add(scaling_graph, product_graph, shaded_area)

        k_start, k_end = -4, 4
        discrete_k_vals = list(range(k_start, k_end + 1))
        c_k_vals = []
        for k_val in discrete_k_vals:
            y_vals = f(X_INT) * phi_jk(X_INT, j, k_val)
            c_k_vals.append(np.sum(y_vals) * DX)

        stems = VGroup()
        dot_color = RED
        for k_val, c_k in zip(discrete_k_vals, c_k_vals):
            k_pos = k_val / (2**j)
            stem = Line(axes_bot.c2p(k_pos, 0), axes_bot.c2p(k_pos, c_k), color=dot_color)
            dot = Dot(axes_bot.c2p(k_pos, c_k), color=dot_color, radius=0.06)
            group = VGroup(stem, dot)
            group.k_val = k_val
            group.set_opacity(0)
            stems.add(group)

        def create_stem_updater(stems_vgroup):
            def update_stems(vgroup):
                current_k = k_tracker.get_value()
                for group in vgroup:
                    if current_k >= group.k_val - 0.01:
                        group.set_opacity(1)
                    else:
                        group.set_opacity(0)
            return update_stems

        updater = create_stem_updater(stems)
        stems.add_updater(updater)
        self.add(stems)

        self.wait(0.2)
        num_k = len(discrete_k_vals)
        step_time = max(0.05, 3.0 / num_k)
        wait_time = max(0.02, 1.5 / num_k)

        for k_val in discrete_k_vals[1:]:
            self.play(k_tracker.animate.set_value(k_val), run_time=step_time)
            self.wait(wait_time)

        self.wait(0.5)
        stems.remove_updater(updater)

        new_bot_label = MathTex(
            r"\sum_{k} c_{0}(k) \cdot \varphi_{0,k}(x)",
            font_size=28,
            color=BLACK
        ).move_to(bot_label, aligned_edge=LEFT)
        self.play(Transform(bot_label, new_bot_label))

        def reconstructed_signal_func(x, c_vals=c_k_vals, k_vals=discrete_k_vals):
            val = 0
            for k_v, c_k in zip(k_vals, c_vals):
                val += c_k * phi_jk(x, j, k_v)
            return val

        reconstructed_graph = axes_bot.plot(reconstructed_signal_func, color=YELLOW)

        self.play(
            FadeOut(stems),
            FadeIn(reconstructed_graph),
            run_time=1.0
        )
        self.wait(2)


# ==========================================
# ANIMATION 2: (5 Axes: 3 Scales)
# ==========================================
class WaveletFunction(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        j_tracker = ValueTracker(0)
        k_tracker = ValueTracker(-4)

        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.1, x_length=8.5, axis_config={"color": BLACK})
        axes_mid = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.1, x_length=8.5, axis_config={"color": BLACK})
        axes_bot0 = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.1, x_length=8.5, axis_config={"color": BLACK})
        axes_bot1 = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.1, x_length=8.5, axis_config={"color": BLACK})
        axes_bot2 = Axes(x_range=[-5, 5, 1], y_range=[-2, 3, 1], y_length=1.1, x_length=8.5, axis_config={"color": BLACK})

        VGroup(axes_top, axes_mid, axes_bot0, axes_bot1, axes_bot2).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        top_label = always_redraw(
            lambda: Tex(
            r"Signal $f(x)$ \& Wavelet function $\psi_{%d,k}(x)$"
            % int(round(j_tracker.get_value())),
            font_size=24,
            color=BLACK,
        ).next_to(axes_top, UP, buff=0.08, aligned_edge=LEFT)
        )
        mid_label = Tex(r"Inner product: $\langle f, \psi_{j,k} \rangle$", font_size=24, color=BLACK).next_to(axes_mid, UP, buff=0.08, aligned_edge=LEFT)
        bot0_label = Tex(r"$d_0(k)$", font_size=24, color=BLACK).next_to(axes_bot0, UP, buff=0.08, aligned_edge=LEFT)
        bot1_label = Tex(r"$d_1(k)$", font_size=24, color=BLACK).next_to(axes_bot1, UP, buff=0.08, aligned_edge=LEFT)
        bot2_label = Tex(r"$d_2(k)$", font_size=24, color=BLACK).next_to(axes_bot2, UP, buff=0.08, aligned_edge=LEFT)

        signal_graph = axes_top.plot(f, color=BLUE)
        self.play(
            Create(VGroup(axes_top, axes_mid, axes_bot0, axes_bot1, axes_bot2)), 
            Write(VGroup(top_label, mid_label, bot0_label, bot1_label, bot2_label)), 
            Create(signal_graph)
        )

        j_label = always_redraw(lambda: MathTex(f"j = {int(round(j_tracker.get_value(), 0))}", font_size=28, color=BLACK).to_corner(UL))
        k_label = always_redraw(lambda: MathTex(f"k = {int(round(k_tracker.get_value()))}", font_size=28, color=BLACK).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        def product(x, j, k): return f(x) * psi_jk(x, j, k)

        wavelet_graph = always_redraw(lambda: axes_top.plot(lambda x: psi_jk(x, j_tracker.get_value(), k_tracker.get_value()), color=ORANGE))
        product_graph = always_redraw(lambda: axes_mid.plot(lambda x: product(x, j_tracker.get_value(), k_tracker.get_value()), color=GREEN))
        shaded_area = always_redraw(lambda: axes_mid.get_area(product_graph, x_range=[-5, 5], color=GREEN).set_opacity(0.5))

        self.add(wavelet_graph, product_graph, shaded_area)

        scales_data = [
            {"j": 0, "k_start": -4, "k_end": 4, "axes_bot": axes_bot0, "color": RED, "label": bot0_label},
            {"j": 1, "k_start": -8, "k_end": 8, "axes_bot": axes_bot1, "color": "#D4AF37", "label": bot1_label},
            {"j": 2, "k_start": -16, "k_end": 16, "axes_bot": axes_bot2, "color": TEAL, "label": bot2_label},
        ]

        for data in scales_data:
            current_j = data["j"]
            k_start = data["k_start"]
            k_end = data["k_end"]
            axes_bot = data["axes_bot"]
            dot_color = data["color"]
            
            self.play(j_tracker.animate.set_value(current_j), k_tracker.animate.set_value(k_start), run_time=1.0)
            
            discrete_k_vals = list(range(k_start, k_end + 1))
            c_k_vals = []
            for k_val in discrete_k_vals:
                y_vals = f(X_INT) * psi_jk(X_INT, current_j, k_val)
                c_k_vals.append(np.sum(y_vals) * DX)
                
            stems = VGroup()
            for k_val, c_k in zip(discrete_k_vals, c_k_vals):
                k_pos = k_val / (2**current_j)
                stem = Line(axes_bot.c2p(k_pos, 0), axes_bot.c2p(k_pos, c_k), color=dot_color)
                dot = Dot(axes_bot.c2p(k_pos, c_k), color=dot_color, radius=0.06)
                group = VGroup(stem, dot)
                group.k_val = k_val
                group.set_opacity(0)
                stems.add(group)
                
            def create_stem_updater(stems_vgroup):
                def update_stems(vgroup):
                    current_k = k_tracker.get_value()
                    for group in vgroup:
                        if current_k >= group.k_val - 0.01:
                            group.set_opacity(1)
                        else:
                            group.set_opacity(0)
                return update_stems
                
            updater = create_stem_updater(stems)
            stems.add_updater(updater)
            self.add(stems)
            
            self.wait(0.2)
            num_k = len(discrete_k_vals)
            step_time = max(0.05, 3.0 / num_k)
            wait_time = max(0.02, 1.5 / num_k)
            
            for k_val in discrete_k_vals[1:]:
                self.play(k_tracker.animate.set_value(k_val), run_time=step_time)
                self.wait(wait_time)
                
            self.wait(0.5)
            stems.remove_updater(updater)
            
            current_label = data["label"]
            new_label = MathTex(
                fr"\sum_{{k}} d_{{{current_j}}}(k)\cdot\psi_{{{current_j},k}}(x)",
                font_size=24,
                color=BLACK
            ).move_to(current_label, aligned_edge=LEFT)
            self.play(Transform(current_label, new_label))
            
            def current_reconstructed_func(x, c_j=current_j, c_vals=c_k_vals, k_vals=discrete_k_vals):
                val = 0
                for k_v, c_k in zip(k_vals, c_vals):
                    val += c_k * psi_jk(x, c_j, k_v)
                return val
            
            reconstructed_graph = axes_bot.plot(current_reconstructed_func, color=YELLOW)
            
            self.play(
                FadeOut(stems),
                FadeIn(reconstructed_graph),
                run_time=1.0
            )
            self.wait(1)