from manim import *
import numpy as np
from scipy.integrate import quad

# --- Shared Mathematical Functions ---
def f(x): 
    return np.sin(x) + 0.5 * np.cos(2.5 * x)

def phi(x): 
    return np.exp(-np.pi * x**2) 

def psi(x): 
    return (1 - 2 * np.pi * x**2) * np.exp(-np.pi * x**2) 

def phi_jk(x, j, k): 
    return (2**(j / 2)) * phi((2**j) * x - k)

def psi_jk(x, j, k): 
    return (2**(j / 2)) * psi((2**j) * x - k)


# ==========================================
# ANIMATION 1: Scaling Approximation (2 Axes)
# ==========================================
class ScalingApproximation(Scene):
    def construct(self):
        # Top title
        top_label = Tex("Scaling Function sliding over signal", font_size=32).to_edge(UP)
        
        # Axes with reduced x_length to prevent UI overlap in corners
        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=3, x_length=8.5).next_to(top_label, DOWN, buff=0.4)
        axes_bot = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=3, x_length=8.5).shift(DOWN * 2)

        signal_graph = axes_top.plot(f, color=BLUE)
        f_legend = MathTex("f(x)", color=BLUE, font_size=32).move_to(axes_top.c2p(4, 1.5))
        phi_legend = MathTex("\\varphi_{j_0,k}(x)", color=YELLOW, font_size=32).next_to(f_legend, DOWN, buff=0.1)

        self.play(Create(VGroup(axes_top, axes_bot)), Write(top_label), Create(signal_graph), Write(f_legend), Write(phi_legend))

        # Dynamic UI Labels firmly in the corner
        k_tracker = ValueTracker(-4)
        j = 0 

        j_label = MathTex("j_0 = 0 \\text{ (fixed)}", font_size=36).to_corner(UL)
        k_label = always_redraw(lambda: MathTex(f"k = {int(round(k_tracker.get_value(), 0))}", font_size=36).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        scaling_graph = always_redraw(lambda: axes_top.plot(lambda x: phi_jk(x, j, k_tracker.get_value()), color=YELLOW))
        self.add(scaling_graph)

        # Unlabeled bottom stem plot updater
        def update_coef(mob):
            k_val = k_tracker.get_value()
            area, _ = quad(lambda x: f(x) * phi_jk(x, j, k_val), -5, 5)
            mob.become(VGroup(Dot(axes_bot.c2p(k_val, area), color=RED), Line(axes_bot.c2p(k_val, 0), axes_bot.c2p(k_val, area), color=RED)))

        dynamic_stem = VGroup().add_updater(update_coef)
        self.add(dynamic_stem)

        extracted_points = []
        for k_val in range(-4, 5):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.6)
            area, _ = quad(lambda x: f(x) * phi_jk(x, j, k_val), -5, 5)
            pt = axes_bot.c2p(k_val, area)
            extracted_points.append(pt)
            self.add(Dot(pt, color=RED), Line(axes_bot.c2p(k_val, 0), pt, color=RED))
            self.wait(0.2)
            
        # Draw the envelope line at the end
        envelope = VMobject(color=WHITE, stroke_width=3).set_points_as_corners(extracted_points)
        self.play(Create(envelope), run_time=1.5)
        self.wait(2)


# ==========================================
# ANIMATION 2: Scaling Inner Product (3 Axes)
# ==========================================
class ScalingInnerProduct(Scene):
    def construct(self):
        top_label = Tex("Signal $f(x)$ \& Scaling function $\\varphi_{j_0,k}(x)$", font_size=28).to_edge(UP)
        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5).next_to(top_label, DOWN, buff=0.2)
        
        mid_label = Tex("Inner product: $f(x) \\cdot \\varphi_{j_0,k}(x)$ (Area = $c_{j_0}(k)$)", font_size=28).next_to(axes_top, DOWN, buff=0.2, aligned_edge=LEFT)
        axes_mid = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5).next_to(mid_label, DOWN, buff=0.2)
        
        bot_label = Tex("Extracted coarse coefficients $c_{j_0}(k)$", font_size=28).next_to(axes_mid, DOWN, buff=0.2, aligned_edge=LEFT)
        axes_bot = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5).next_to(bot_label, DOWN, buff=0.2)

        signal_graph = axes_top.plot(f, color=BLUE)
        self.play(Create(VGroup(axes_top, axes_mid, axes_bot)), Write(VGroup(top_label, mid_label, bot_label)), Create(signal_graph))

        k_tracker = ValueTracker(-4)
        j = 0 

        j_label = MathTex("j_0 = 0 \\text{ (fixed)}", font_size=36).to_corner(UL)
        k_label = always_redraw(lambda: MathTex(f"k = {int(round(k_tracker.get_value(), 0))}", font_size=36).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        def product(x, k): return f(x) * phi_jk(x, j, k)

        scaling_graph = always_redraw(lambda: axes_top.plot(lambda x: phi_jk(x, j, k_tracker.get_value()), color=YELLOW))
        product_graph = always_redraw(lambda: axes_mid.plot(lambda x: product(x, k_tracker.get_value()), color=GREEN))
        shaded_area = always_redraw(lambda: axes_mid.get_area(product_graph, x_range=[-5, 5], color=GREEN, opacity=0.5))

        def update_coef(mob):
            k_val = k_tracker.get_value()
            area, _ = quad(lambda x: product(x, k_val), -5, 5)
            mob.become(VGroup(Dot(axes_bot.c2p(k_val, area), color=RED), Line(axes_bot.c2p(k_val, 0), axes_bot.c2p(k_val, area), color=RED)))

        dynamic_stem = VGroup().add_updater(update_coef)
        self.add(scaling_graph, product_graph, shaded_area, dynamic_stem)

        extracted_points = []
        for k_val in range(-4, 5):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.6)
            area, _ = quad(lambda x: product(x, k_val), -5, 5)
            pt = axes_bot.c2p(k_val, area)
            extracted_points.append(pt)
            self.add(Dot(pt, color=RED), Line(axes_bot.c2p(k_val, 0), pt, color=RED))
        
        envelope = VMobject(color=WHITE, stroke_width=3).set_points_as_corners(extracted_points)
        self.play(Create(envelope), run_time=1.5)
        self.wait(2)


# ==========================================
# ANIMATION 3: Wavelet Details (2 Axes, 3 Scales)
# ==========================================
class WaveletDetails(Scene):
    def construct(self):
        top_label = Tex("Wavelet Function sliding over signal (Multiple Scales)", font_size=32).to_edge(UP)
        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=3, x_length=8.5).next_to(top_label, DOWN, buff=0.4)
        axes_bot = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=3, x_length=8.5).shift(DOWN * 2)

        signal_graph = axes_top.plot(f, color=BLUE)
        f_legend = MathTex("f(x)", color=BLUE, font_size=32).move_to(axes_top.c2p(4, 1.5))
        psi_legend = MathTex("\\psi_{j,k}(x)", color=ORANGE, font_size=32).next_to(f_legend, DOWN, buff=0.1)

        self.play(Create(VGroup(axes_top, axes_bot)), Write(top_label), Create(signal_graph), Write(f_legend), Write(psi_legend))

        j_tracker = ValueTracker(0)
        k_tracker = ValueTracker(-4)

        j_label = always_redraw(lambda: MathTex(f"j = {int(round(j_tracker.get_value(), 0))}", font_size=36).to_corner(UL))
        k_label = always_redraw(lambda: MathTex(f"k = {int(round(k_tracker.get_value(), 0))}", font_size=36).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        wavelet_graph = always_redraw(lambda: axes_top.plot(lambda x: psi_jk(x, j_tracker.get_value(), k_tracker.get_value()), color=ORANGE))
        self.add(wavelet_graph)

        def update_coef(mob):
            j_val = int(round(j_tracker.get_value(), 0))
            k_val = k_tracker.get_value()
            area, _ = quad(lambda x: f(x) * psi_jk(x, j_val, k_val), -5, 5)
            x_pos = k_val / (2**j_val)
            
            # Color coding for different scales
            if j_val == 0: color = RED
            elif j_val == 1: color = YELLOW
            else: color = TEAL
                
            mob.become(VGroup(Dot(axes_bot.c2p(x_pos, area), color=color), Line(axes_bot.c2p(x_pos, 0), axes_bot.c2p(x_pos, area), color=color)))

        dynamic_stem = VGroup().add_updater(update_coef)
        self.add(dynamic_stem)

        # --- Scale j = 0 ---
        pts_j0 = []
        for k_val in range(-4, 5):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.5)
            area, _ = quad(lambda x: f(x) * psi_jk(x, 0, k_val), -5, 5)
            pt = axes_bot.c2p(k_val, area)
            pts_j0.append(pt)
            self.add(Dot(pt, color=RED), Line(axes_bot.c2p(k_val, 0), pt, color=RED))
        
        env0 = VMobject(color=RED, stroke_width=3).set_points_as_corners(pts_j0)
        self.play(Create(env0))
        self.wait(1)

        # --- Scale j = 1 ---
        self.play(j_tracker.animate.set_value(1), k_tracker.animate.set_value(-8), run_time=1.5)
        pts_j1 = []
        for k_val in range(-8, 9, 2):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.4)
            area, _ = quad(lambda x: f(x) * psi_jk(x, 1, k_val), -5, 5)
            pt = axes_bot.c2p(k_val/2, area)
            pts_j1.append(pt)
            self.add(Dot(pt, color=YELLOW), Line(axes_bot.c2p(k_val/2, 0), pt, color=YELLOW))
            
        env1 = VMobject(color=YELLOW, stroke_width=3).set_points_as_corners(pts_j1)
        self.play(Create(env1))
        self.wait(1)

        # --- Scale j = 2 ---
        self.play(j_tracker.animate.set_value(2), k_tracker.animate.set_value(-16), run_time=1.5)
        pts_j2 = []
        for k_val in range(-16, 17, 4):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.3)
            area, _ = quad(lambda x: f(x) * psi_jk(x, 2, k_val), -5, 5)
            pt = axes_bot.c2p(k_val/4, area)
            pts_j2.append(pt)
            self.add(Dot(pt, color=TEAL), Line(axes_bot.c2p(k_val/4, 0), pt, color=TEAL))
            
        env2 = VMobject(color=TEAL, stroke_width=3).set_points_as_corners(pts_j2)
        self.play(Create(env2))
        self.wait(2)


# ==========================================
# ANIMATION 4: Wavelet Inner Product (3 Axes, 3 Scales)
# ==========================================
class WaveletInnerProduct(Scene):
    def construct(self):
        j_tracker = ValueTracker(0)
        k_tracker = ValueTracker(-4)

        top_label = always_redraw(lambda: Tex(f"Signal $f(x)$ \& Wavelet function $\\psi_{{{int(j_tracker.get_value())},k}}(x)$", font_size=28).to_edge(UP))
        axes_top = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5).next_to(top_label, DOWN, buff=0.2)
        
        mid_label = Tex("Inner product: $f(x) \\cdot \\psi_{j,k}(x)$ (Area = $d_j(k)$)", font_size=28).next_to(axes_top, DOWN, buff=0.2, aligned_edge=LEFT)
        axes_mid = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5).next_to(mid_label, DOWN, buff=0.2)
        
        bot_label = Tex("Extracted detail coefficients $d_j(k)$", font_size=28).next_to(axes_mid, DOWN, buff=0.2, aligned_edge=LEFT)
        axes_bot = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], y_length=1.8, x_length=8.5).next_to(bot_label, DOWN, buff=0.2)

        signal_graph = axes_top.plot(f, color=BLUE)
        self.play(Create(VGroup(axes_top, axes_mid, axes_bot)), Write(VGroup(top_label, mid_label, bot_label)), Create(signal_graph))

        j_label = always_redraw(lambda: MathTex(f"j = {int(round(j_tracker.get_value(), 0))}", font_size=36).to_corner(UL))
        k_label = always_redraw(lambda: MathTex(f"k = {int(round(k_tracker.get_value(), 0))}", font_size=36).next_to(j_label, DOWN, aligned_edge=LEFT))
        self.play(Write(j_label), Write(k_label))

        def product(x, j, k): return f(x) * psi_jk(x, j, k)

        wavelet_graph = always_redraw(lambda: axes_top.plot(lambda x: psi_jk(x, j_tracker.get_value(), k_tracker.get_value()), color=ORANGE))
        product_graph = always_redraw(lambda: axes_mid.plot(lambda x: product(x, j_tracker.get_value(), k_tracker.get_value()), color=GREEN))
        shaded_area = always_redraw(lambda: axes_mid.get_area(product_graph, x_range=[-5, 5], color=GREEN, opacity=0.5))

        def update_coef(mob):
            j_val = int(round(j_tracker.get_value(), 0))
            k_val = k_tracker.get_value()
            area, _ = quad(lambda x: product(x, j_val, k_val), -5, 5)
            x_pos = k_val / (2**j_val)
            
            if j_val == 0: color = RED
            elif j_val == 1: color = YELLOW
            else: color = TEAL
                
            mob.become(VGroup(Dot(axes_bot.c2p(x_pos, area), color=color), Line(axes_bot.c2p(x_pos, 0), axes_bot.c2p(x_pos, area), color=color)))

        dynamic_stem = VGroup().add_updater(update_coef)
        self.add(wavelet_graph, product_graph, shaded_area, dynamic_stem)

        # --- Scale j = 0 ---
        pts_j0 = []
        for k_val in range(-4, 5):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.5)
            area, _ = quad(lambda x: product(x, 0, k_val), -5, 5)
            pt = axes_bot.c2p(k_val, area)
            pts_j0.append(pt)
            self.add(Dot(pt, color=RED), Line(axes_bot.c2p(k_val, 0), pt, color=RED))
            
        env0 = VMobject(color=RED, stroke_width=3).set_points_as_corners(pts_j0)
        self.play(Create(env0))
        self.wait(1)
        
        # --- Scale j = 1 ---
        self.play(j_tracker.animate.set_value(1), k_tracker.animate.set_value(-8), run_time=1.5)
        pts_j1 = []
        for k_val in range(-8, 9, 2):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.4)
            area, _ = quad(lambda x: product(x, 1, k_val), -5, 5)
            pt = axes_bot.c2p(k_val/2, area)
            pts_j1.append(pt)
            self.add(Dot(pt, color=YELLOW), Line(axes_bot.c2p(k_val/2, 0), pt, color=YELLOW))

        env1 = VMobject(color=YELLOW, stroke_width=3).set_points_as_corners(pts_j1)
        self.play(Create(env1))
        self.wait(1)

        # --- Scale j = 2 ---
        self.play(j_tracker.animate.set_value(2), k_tracker.animate.set_value(-16), run_time=1.5)
        pts_j2 = []
        for k_val in range(-16, 17, 4):
            self.play(k_tracker.animate.set_value(k_val), run_time=0.3)
            area, _ = quad(lambda x: product(x, 2, k_val), -5, 5)
            pt = axes_bot.c2p(k_val/4, area)
            pts_j2.append(pt)
            self.add(Dot(pt, color=TEAL), Line(axes_bot.c2p(k_val/4, 0), pt, color=TEAL))
            
        env2 = VMobject(color=TEAL, stroke_width=3).set_points_as_corners(pts_j2)
        self.play(Create(env2))
        self.wait(2)