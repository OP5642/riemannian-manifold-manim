from manim import *

class ParametrizedCurveScene(MovingCameraScene):
    def construct(self):
        title = Text("Kako merimo dužinu krive na mnogostrukosti?",
                     font_size=38,
                     color=YELLOW)
        self.play(Write(title))
        self.wait(2.5)
        self.play(Unwrite(title))

        # Define parametrized functions for x(t) and y(t)
        def x(t):
            return t*(3*np.sin(t) + 3*np.cos(t))
        def dx(t):
            return 3*np.sin(t) + 3*np.cos(t) + t*(3*np.cos(t)-3*np.sin(t))
        def y(t):
            return np.sin(t)*3 + 0.5
        def dy(t):
            return np.cos(t)*3

        # Define the parametrized curve
        parametric_curve = ParametricFunction(
            lambda t: np.array([x(t)+2*y(t), 2*x(t)-y(t), 0]),
            t_range=[-1, .5],
            color=BLUE
        )

        sub_curve = ParametricFunction(
            lambda t: np.array([x(t)+2*y(t), 2*x(t)-y(t), 0]),
            t_range=[-1,-.8],
            color=BLUE
        )

        # Create the curve and add it to the scene
        paragraph1 = Tex(r"""
        Pretpostavimo da nam je data kriva \(\gamma: [0,1] \to \mathbb{R}^n\).
        """)

        paragraph2 = Tex(r"""
        Kako računamo njenu dužinu?
        """)

        paragraph2.move_to(DOWN*3)
        paragraph1.move_to(DOWN*2)
        self.play(Write(paragraph1))
        self.play(Create(parametric_curve, run_time=2))
        self.wait(.5)
        self.play(Write(paragraph2))
        self.wait(2)
        self.play(Unwrite(paragraph1), Unwrite(paragraph2))

        # Create a list of tangent vectors
        vectors = VGroup()
        for t in np.linspace(-1,.45, 20):
            position = np.array([x(t)+2*y(t), 2*x(t)-y(t), 0])
            tangent_vector = np.array([dx(t)+2*dy(t), 2*dx(t)-dy(t), 0])
            unit_tangent_vector = tangent_vector/np.linalg.norm(tangent_vector)
            unit_tangent_vector = 1.3 * unit_tangent_vector  # Scale the vector
            vector = Arrow(start=position,
                           end=position + unit_tangent_vector,
                           color=RED)
            vectors.add(vector)

        self.play(LaggedStartMap(Create, vectors))  # Draw the vectors
        # self.play(AnimationGroup(*[Create(vec) for vec in vectors]))
        self.wait(2)

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(height=2).move_to(sub_curve))
        self.wait(1)
        self.play(Restore(self.camera.frame))
        paragraph3 = Tex(r"""
        Vidimo da je lokalno ona približno jednaka dužini\\ tangentnog vektora.
        """)

        paragraph3.move_to(DOWN*2)
        self.play(Write(paragraph3))
        self.wait(3)
        paragraph4 = Tex(r"""
        Dakle, ima smisla reći da je dužina 
        \[l(\gamma) = \int_{[0,1]} \lVert \gamma'(t)\rVert dt.\]
        """)
        paragraph4.to_edge(DOWN)
        self.play(TransformMatchingShapes(paragraph3, paragraph4))
        self.wait(3)

        animations = [
            FadeOut(vectors),
            FadeOut(parametric_curve),
            FadeOut(paragraph4)
        ]

        self.play(AnimationGroup(*animations))
        self.wait(2)

class ManifoldCurveScene(ThreeDScene):
    def construct(self):
        # Setup the 3D Scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        paragraph1 = Tex(r"""
        Kako bi ovo funkcionisalo na nekoj mnogostrukosti \(M\)?
        """)
        paragraph1.move_to(UP*3)
        self.add_fixed_in_frame_mobjects(paragraph1)
        self.play(Write(paragraph1))
        self.wait(2)

        # Define the surface
        surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                -.5*u**2-.5*v**2
            ]),
            u_range=[-2,2],
            v_range=[-2,2],
            color=BLUE_D,
            fill_opacity=0.7,
        )

        self.begin_ambient_camera_rotation(rate=0.1)  # Slow camera rotation
        self.play(Create(surface, run_time=1))
        self.wait(1.5)

        def x(t):
            return np.sin(2*t)
        def dx(t):
            return 2*np.cos(2*t)
        def y(t):
            return np.sin(t)
        def dy(t):
            return np.cos(t)
        def z(t):
            return -.5*x(t)**2 - .5*y(t)**2
        def dz(t):
            return -dx(t)*x(t) - dy(t)*y(t)
        def curve_func(t):
            return np.array([x(t), y(t), z(t)])

        parametric_curve = ParametricFunction(
            lambda t: np.array([x(t), y(t), z(t)]),
            t_range=[-2,2],
            color=RED
        )
        self.play(Create(parametric_curve, run_time=2))
        self.wait(3)

        paragraph2 = Tex(r"""
        Problem nam pravi pojam tangentnog vektora.
        """)
        paragraph2.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph2)
        self.play(Write(paragraph2))
        self.wait(2)
        self.play(Unwrite(paragraph2), Unwrite(paragraph1))

        paragraph3 = Tex(r"""
        Treba nam nešto što će izgledati kao \(\mathbb{R}^n\) u tački\\
        da bismo mogli da merimo dužinu vektora.
        """)
        paragraph3.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph3)
        self.play(Write(paragraph3))
        self.wait(2)
        self.play(Unwrite(paragraph3))


        paragraph4 = Tex(r"""
        To je upravo tangentni prostor.
        """)
        paragraph4.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph4)
        self.play(Write(paragraph4))
        self.wait(3)
        self.play(Unwrite(paragraph4))

        self.stop_ambient_camera_rotation()  # Stop camera rotation
        self.move_camera(theta = -25*DEGREES, phi=50 * DEGREES, zoom=2)

        self.wait(2)

        def unit_tangent_vector(t):
            tangent_vector = np.array([dx(t), dy(t), dz(t)])  # Tangent vector
            unit_tangent_vector = tangent_vector/np.linalg.norm(tangent_vector)
            return unit_tangent_vector

        vector = Arrow(start=curve_func(-2),
                       end=curve_func(-2) + unit_tangent_vector(-2),
                       color=RED)

        def tangent_plane_func(t, u, v):
            return np.array([x(t), y(t), z(t)]) + \
                        u * np.array([1, 0, -x(t)]) + v* np.array([0, 1, -y(t)])

        tangent_plane = Surface(
            lambda u, v: tangent_plane_func(-2, u, v),
            u_range=[-1, 1],
            v_range=[-1, 1],
            fill_color=GREEN_D,
            fill_opacity=0.5,
        )
        self.play(Create(tangent_plane))
        self.begin_ambient_camera_rotation()  # Stop camera rotation
        self.begin_ambient_camera_rotation(rate=0.3)  # Slow camera rotation
        self.wait(9)

        paragraph4 = Tex(r"""
        Ovo imamo u svakoj tački.
        """)
        paragraph4.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph4)
        self.play(Write(paragraph4))
        self.wait(3)
        self.play(Unwrite(paragraph4))

        # Define a tracker
        t_tracker = ValueTracker(-2)
        tangent_plane.add_updater(
            lambda m: m.become(
                Surface(
                    lambda u, v: tangent_plane_func(t_tracker.get_value(),
                                                    u,
                                                    v),
                    u_range=[-1, 1],
                    v_range=[-1, 1],
                    fill_color=GREEN_D,
                    fill_opacity=0.5,
                )
            )
        )

        moving_dot = Dot3D(curve_func(-2), radius = 0.06, color= RED)
        moving_dot.add_updater(
            lambda m: m.move_to(curve_func(t_tracker.get_value()))
        )

        # Update the position of the arrow, ensuring no shift
        def update_arrow(arrow, t):
            start_point = curve_func(t)
            arrow.put_start_and_end_on(start_point,
                                       start_point + unit_tangent_vector(t))

        vector.add_updater(lambda m: update_arrow(vector,
                                                  t_tracker.get_value()))

        self.add(tangent_plane, vector, moving_dot)
        self.play(t_tracker.animate.set_value(2), run_time=10, rate_func=linear)
        self.play(Unwrite(paragraph4))
        self.wait(2)

        self.move_camera(zoom=1)

        paragraph5 = Tex(r"""
        Tangentni prostor je vektorski prostor, možemo meriti\\
        dužinu vektora ako uvedemo skalarni proizvod.
        """)
        paragraph5.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph5)
        self.play(Write(paragraph5))
        self.wait(3)
        self.play(Unwrite(paragraph5))

        paragraph6 = Tex(r"""
        Ako još skalarni proizvod zavisi glatko od tačke \(p \in M\)\\
        onda ga nazivamo \emph{Rimanovom metrikom} \(g\) na \(M\).
        """)
        paragraph6.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph6)
        self.play(Write(paragraph6))
        self.wait(3)
        self.play(Unwrite(paragraph6))

        paragraph7 = Tex(r"""
        \[l(\gamma) = \int_{[0,1]} \lVert \gamma'(t)\rVert_g dt\]
        """)
        paragraph7.move_to(UP*3)
        paragraph8 = Tex(r"""
        Formula je ista, ali je interpretacija potpuno drugačija.
        """)
        paragraph8.move_to(UP*2)
        self.add_fixed_in_frame_mobjects(paragraph7)
        self.play(Write(paragraph7))
        self.wait(1)
        self.add_fixed_in_frame_mobjects(paragraph8)
        self.play(Write(paragraph8))
        self.wait(2)

        # FadeOut 
        animations = [
            FadeOut(vector),
            FadeOut(parametric_curve),
            FadeOut(tangent_plane),
            FadeOut(surface),
            FadeOut(moving_dot)
        ]
        self.play(Unwrite(paragraph8))

        self.play(AnimationGroup(*animations))
        self.play(paragraph7.animate.move_to(ORIGIN))
        self.wait(2.5)
        self.play(Unwrite(paragraph7))
        self.wait(2)
