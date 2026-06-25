from manim import *
import numpy as np

class MultiresolutionReconstruction(Scene):
    def construct(self):
        # 1. Setup Stacked Axes
        axes_top = Axes(x_range=[0, 10, 1], y_range=[-2.5, 2.5, 1], y_length=3, x_length=10).to_edge(UP)
        axes_bot = Axes(x_range=[0, 10, 1], y_range=[-1.5, 1.5, 1], y_length=2, x_length=10).to_edge(DOWN)

        # 2. Define the Signal Components (Simulating V0, W0, W1)
        # We use a synthetic signal f(x) made of 3 frequencies
        def v0_func(x): return np.sin(x)                   # Coarse base (Scaling Space V_0)
        def w0_func(x): return 0.6 * np.cos(3 * x)         # Medium detail (Wavelet Space W_0)
        def w1_func(x): return 0.3 * np.sin(10 * x)        # Fine detail (Wavelet Space W_1)
        def f_func(x):  return v0_func(x) + w0_func(x) + w1_func(x) # Target Signal

        # 3. Create the Target Signal (drawn faintly in the background)
        target_signal = axes_top.plot(f_func, color=WHITE, stroke_opacity=0.3)
        target_label = MathTex("f(x) \\text{ (Target Signal)}", color=WHITE, font_size=28).next_to(axes_top, UP, aligned_edge=RIGHT)
        
        self.play(Create(axes_top), Create(axes_bot), Create(target_signal), Write(target_label))

        # --- STEP 1: The Coarse Approximation (V_0) ---
        title_bot = Tex("Current Component being added:", font_size=28).next_to(axes_bot, UP, aligned_edge=LEFT)
        self.play(Write(title_bot))

        v0_graph = axes_bot.plot(v0_func, color=BLUE)
        v0_label = MathTex("V_0 \\text{ (Coarse base from Scaling Function, } j=0)", color=BLUE, font_size=28).next_to(title_bot, RIGHT)
        
        self.play(Create(v0_graph), Write(v0_label))
        self.wait(1)

        # Move V0 to the top as the start of our reconstruction
        current_recon_graph = axes_top.plot(v0_func, color=BLUE)
        recon_label = MathTex("\\text{Reconstruction: } V_0", color=BLUE, font_size=32).next_to(axes_top, UP, aligned_edge=LEFT)
        
        self.play(TransformFromCopy(v0_graph, current_recon_graph), Write(recon_label))
        self.wait(1)

        # --- STEP 2: Adding Detail scale j=0 (W_0) ---
        self.play(FadeOut(v0_graph), FadeOut(v0_label))
        
        w0_graph = axes_bot.plot(w0_func, color=ORANGE)
        w0_label = MathTex("W_0 \\text{ (Medium detail from Wavelet, } j=0)", color=ORANGE, font_size=28).next_to(title_bot, RIGHT)
        
        self.play(Create(w0_graph), Write(w0_label))
        self.wait(1)

        # Add W0 to V0 to create V1
        def v1_func(x): return v0_func(x) + w0_func(x)
        v1_graph = axes_top.plot(v1_func, color=TEAL)
        v1_label = MathTex("\\text{Reconstruction: } V_1 = V_0 \\oplus W_0", color=TEAL, font_size=32).next_to(axes_top, UP, aligned_edge=LEFT)

        # Animate the addition visually
        self.play(
            Transform(current_recon_graph, v1_graph),
            Transform(recon_label, v1_label),
            run_time=2
        )
        self.wait(1)

        # --- STEP 3: Adding Detail scale j=1 (W_1) ---
        self.play(FadeOut(w0_graph), FadeOut(w0_label))
        
        w1_graph = axes_bot.plot(w1_func, color=RED)
        w1_label = MathTex("W_1 \\text{ (Fine detail from Wavelet, } j=1)", color=RED, font_size=28).next_to(title_bot, RIGHT)
        
        self.play(Create(w1_graph), Write(w1_label))
        self.wait(1)

        # Add W1 to V1 to create V2 (The final signal)
        v2_graph = axes_top.plot(f_func, color=GREEN)
        v2_label = MathTex("\\text{Reconstruction: } V_2 = V_1 \\oplus W_1 = f(x)", color=GREEN, font_size=32).next_to(axes_top, UP, aligned_edge=LEFT)

        self.play(
            Transform(current_recon_graph, v2_graph),
            Transform(recon_label, v2_label),
            run_time=2
        )
        self.wait(2)