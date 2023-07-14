import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from scene import Scene
import sys


WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800
RETURN_ACTION_CONTINUE = 0
RETURN_ACTION_END = 1


class App:
    def __init__(self):
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

        window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'OpenGL', None, None)
        glfw.make_context_current(window)
        glfw.set_input_mode(
            window,
            GLFW_CONSTANTS.GLFW_CURSOR,
            GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
        )

        self.window = window

        # Initialise OpenGl
        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = self.create_shader('shaders/vertex.glsl', 'shaders/fragment.glsl')
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, 'imageTexture'), 0)

        self.scene = Scene()

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WINDOW_WIDTH/WINDOW_HEIGHT,
            near=0.1, far=50, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, 'projection'),
            1, GL_FALSE, projection_transform
        )

        self.model_matrix_location = glGetUniformLocation(self.shader, 'model')
        self.view_matrix_location = glGetUniformLocation(self.shader, 'view')
        self.light_location = {
            'position': [
                glGetUniformLocation(self.shader, f'Lights[{i}].position')
                for i in range(8)
            ],
            'color': [
                glGetUniformLocation(self.shader, f'Lights[{i}].color')
                for i in range(8)
            ],
            'strength': [
                glGetUniformLocation(self.shader, f'Lights[{i}].strength')
                for i in range(8)
            ]
        }
        self.camera_pos_location = glGetUniformLocation(self.shader, 'cameraPos')

        self.last_time = glfw.get_time()
        self.current_time = 0
        self.num_frames = 0
        self.frame_time = 0

        self.walk_offset_lookup = {
            1: 0,
            2: 90,
            3: 45,
            4: 180,
            6: 135,
            7: 90,
            8: 270,
            9: 315,
            11: 0,
            12: 225,
            13: 270,
            14: 180
        }

    def create_shader(self, vertex_filepath, fragment_filepath):
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        return shader

    def run(self):
        while True:
            if glfw.window_should_close(self.window) \
                    or glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                self.quit()

            self.update()
            self.render()
            self.calculate_frame_rate()

            glFlush()

    def handle_keys(self):
        combo = 0
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 1
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 2
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 4
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 8

        if combo in self.walk_offset_lookup:
            direction_modifier = self.walk_offset_lookup[combo]

            d_pos = [
                0.2 * self.frame_time / 16.7 * np.cos(np.deg2rad(self.scene.player.theta + direction_modifier)),
                0.2 * self.frame_time / 16.7 * np.sin(np.deg2rad(self.scene.player.theta + direction_modifier)),
                0
            ]
            self.scene.move_player(d_pos)

    def handle_mouse(self):
        (mouse_x, mouse_y) = glfw.get_cursor_pos(self.window)
        rate = self.frame_time / 16.7
        theta_increment = rate * ((WINDOW_WIDTH / 2) - mouse_x)
        phi_increment = rate * ((WINDOW_HEIGHT / 2) - mouse_y)
        self.scene.spin_player(theta_increment, phi_increment)
        glfw.set_cursor_pos(self.window, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    def calculate_frame_rate(self):
        self.current_time = glfw.get_time()
        delta = self.current_time - self.last_time
        if delta >= 1:
            frame_rate = max(1, int(self.num_frames / delta))
            glfw.set_window_title(self.window, f"Running at {frame_rate} fps.")
            self.last_time = self.current_time
            self.num_frames = -1
            self.frame_time = float(1000.0 / max(1, frame_rate))
        self.num_frames += 1

    def update(self):
        self.handle_keys()
        self.handle_mouse()

        glfw.poll_events()
        self.scene.update(self.frame_time / 16.7)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)

        self.scene.render(
            self.model_matrix_location,
            self.view_matrix_location,
            self.light_location,
            self.camera_pos_location
        )

    def quit(self):
        self.scene.destroy()
        glDeleteProgram(self.shader)
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.run()
