from manim import *
import numpy as np

def f(x): 
    return np.sin(x) + 0.5 * np.cos(2.5 * x)

def phi(x): 
    return np.exp(-np.pi * x**2) 

def phi_jk(x, j, k): 
    return (2**(j / 2)) * phi((2**j) * x - k)

X_INT = np.linspace(-5, 5, 1000)
DX = X_INT[1] - X_INT[0]

class ScalingInnerProduct(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5, axis_config={"color": BLACK})
        axes_mid = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5, axis_config={"color": BLACK})
        axes_bot = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5, axis_config={"color": BLACK})

        VGroup(axes_top, axes_mid, axes_bot).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        top_label = Tex(r"Signal $f(x)$ \& Scaling function $\varphi_{j_0,k}(x)$", font_size=28, color=BLACK).next_to(axes_top, UP, buff=0.1, aligned_edge=LEFT)
        mid_label = Tex(r"Inner product: $\langle f, \varphi_{j_0,k} \rangle$", font_size=28, color=BLACK).next_to(axes_mid, UP, buff=0.1, aligned_edge=LEFT)
        bot_label = Tex(r"Discrete coarse coefficients $c_{j_0}(k)$ and Reconstruction", font_size=28, color=BLACK).next_to(axes_bot, UP, buff=0.1, aligned_edge=LEFT)

        signal_graph = axes_top.plot(f, color=BLUE)
        self.play(Create(VGroup(axes_top, axes_mid, axes_bot)), Write(VGroup(top_label, mid_label, bot_label)), Create(signal_graph))

        k_tracker = ValueTracker(-5)
        j = 0 

        j_label = MathTex(r"j_0 = 0 \text{ (fixed)}", font_size=36, color=BLACK).to_corner(UL)
        k_label = always_redraw(lambda: MathTex(f"k = {k_tracker.get_value():.2f}", font_size=36, color=BLACK).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        def product(x, k): return f(x) * phi_jk(x, j, k)
        scaling_color = "#D4AF37" 
        
        scaling_graph = always_redraw(lambda: axes_top.plot(lambda x: phi_jk(x, j, k_tracker.get_value()), color=scaling_color))
        product_graph = always_redraw(lambda: axes_mid.plot(lambda x: product(x, k_tracker.get_value()), color=GREEN))
        shaded_area = always_redraw(lambda: axes_mid.get_area(product_graph, x_range=[-5, 5], color=GREEN, opacity=0.5))

        discrete_k_vals = list(range(-5, 6))
        c_k_vals = []
        for k_val in discrete_k_vals:
            y_vals = f(X_INT) * phi_jk(X_INT, j, k_val)
            c_k_vals.append(np.sum(y_vals) * DX)
            
        stems = VGroup()
        for k_val, c_k in zip(discrete_k_vals, c_k_vals):
            stem = Line(axes_bot.c2p(k_val, 0), axes_bot.c2p(k_val, c_k), color=RED)
            dot = Dot(axes_bot.c2p(k_val, c_k), color=RED)
            group = VGroup(stem, dot)
            group.k_val = k_val
            group.set_opacity(0)
            stems.add(group)

        def update_stems(vgroup):
            current_k = k_tracker.get_value()
            for group in vgroup:
                if current_k >= group.k_val:
                    group.set_opacity(1)
                else:
                    group.set_opacity(0)
                    
        stems.add_updater(update_stems)
        self.add(scaling_graph, product_graph, shaded_area, stems)
        
        self.play(k_tracker.animate.set_value(5), run_time=2, rate_func=linear)
        self.wait(1)
        stems.clear_updaters()

        reconstructed_signal = lambda x: 0 * x
        reconstructed_graph = axes_bot.plot(reconstructed_signal, color=YELLOW)
        self.add(reconstructed_graph)
        
        for k_val, c_k in zip(discrete_k_vals, c_k_vals):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.1)
            term_func = lambda x, k=k_val, c=c_k: c * phi_jk(x, j, k)
            term_graph = axes_bot.plot(term_func, color=BLUE_B, opacity=0.5)
            self.play(Create(term_graph), run_time=0.2)
            
            old_reconstructed_signal = reconstructed_signal
            reconstructed_signal = lambda x, old_f=old_reconstructed_signal, t_f=term_func: old_f(x) + t_f(x)
            new_reconstructed_graph = axes_bot.plot(reconstructed_signal, color=YELLOW)
            
            self.play(Transform(reconstructed_graph, new_reconstructed_graph), run_time=0.2)
            
        self.wait(2)
