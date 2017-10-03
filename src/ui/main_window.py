import math

from cairo import ImageSurface
from gi.repository import Gtk
from gi.repository import GObject


class ArtificialAntApplication(Gtk.Application):

    def __init__(self, simulation):
        super().__init__(application_id='cz.netuka.radovan.artificial_ant')
        self.window = None
        self.simulation = simulation

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(self)
        self.window.present()
        GObject.timeout_add(50, self.animate)

    def animate(self):
        self.simulation.do_tick()
        self.window.queue_draw()
        return True



class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application, title='Artificial Ant')
        self.set_default_size(600, 600)
        self.canvas = SimulationCanvas(application.simulation)
        self.add(self.canvas)
        self.canvas.show()


class SimulationCanvas(Gtk.DrawingArea):

    def __init__(self, simulation):
        super().__init__()
        self.connect('draw', self.on_draw)
        self.simulation = simulation

    @property
    def width(self):
        return self.get_allocation().width

    @property
    def height(self):
        return self.get_allocation().height

    @property
    def tile_width(self):
        return self.width / self.tiles_in_column

    @property
    def half_tile_width(self):
        return self.tile_width / 2

    @property
    def tile_height(self):
        return self.height / self.tiles_in_row

    @property
    def half_tile_height(self):
        return self.tile_height / 2

    @property
    def tiles_in_row(self):
        return self.simulation.grid.width

    @property
    def tiles_in_column(self):
        return self.simulation.grid.height

    @property
    def grid_color(self):
        return 1.0, 1.0, 1.0

    @property
    def tile_border_width(self):
        return 1

    @property
    def tile_border_color(self):
        return 128 / 255, 128 / 255, 128 / 255

    @property
    def bait_color(self):
        return 115 / 255, 64 / 255, 33 / 255

    @property
    def ant_image(self):
        return ImageSurface.create_from_png('/home/rnetuka/Projekty/Python/Artificial Ant/res/ant.png')

    @property
    def ant_color(self):
        return 1.0, 0, 0

    def on_draw(self, window, context):
        self.draw_background(context)
        self.draw_grid(context)
        self.draw_baits(context)
        self.draw_ant(context)

    def draw_background(self, context):
        context.set_source_rgb(*self.grid_color)
        context.rectangle(0, 0, self.width, self.height)
        context.fill()

    def draw_grid(self, context):
        context.set_source_rgb(*self.tile_border_color)
        context.set_line_width(self.tile_border_width)

        for x in range(1, self.tiles_in_column):
            context.move_to(x * self.tile_width, 0)
            context.line_to(x * self.tile_width, self.height)

        for y in range(1, self.tiles_in_row):
            context.move_to(0, y * self.tile_height)
            context.line_to(self.width, y * self.tile_height)

        context.stroke()

    def draw_ant(self, context):
        #width = self.ant_image.get_width()
        #height = self.ant_image.get_height()

        ant_x, ant_y = self.simulation.ant_position
        ant_x *= self.tile_width
        ant_y *= self.tile_height

        #rotating_angles = {'north': 0, 'east': 90, 'south': 180, 'west': 270}

        #context.translate(ant_x + (self.tile_width / 2), ant_y + (self.tile_height / 2))
        #context.rotate(rotating_angles[self.simulation.ant_facing_direction] * math.pi /180)
        #context.translate(-1 * (ant_x + (self.tile_width / 2)), -1 * (ant_y + self.tile_height / 2))

        #scale_ration_w = self.tile_width / width
        #scale_ration_h = self.tile_height / height

        #context.scale(scale_ration_w, scale_ration_h)

        #ant_x /= scale_ration_w
        #ant_y /= scale_ration_h

        #context.set_source_surface(self.ant_image, ant_x, ant_y)
        #context.paint()

        directions = {
            'north': ((ant_x + self.half_tile_width, ant_y), (ant_x + self.tile_width, ant_y + self.tile_height), (ant_x, ant_y + self.tile_height)),
            'east': ((ant_x + self.tile_width, ant_y + self.half_tile_height), (ant_x, ant_y + self.tile_height), (ant_x, ant_y)),
            'south': ((ant_x + self.half_tile_width, ant_y + self.tile_height), (ant_x, ant_y), (ant_x + self.tile_width, ant_y)),
            'west': ((ant_x, ant_y + self.half_tile_height), (ant_x + self.tile_width, ant_y), (ant_x + self.tile_width, ant_y + self.tile_height))
        }
        direction = directions[self.simulation.ant_facing_direction]

        context.set_source_rgb(*self.ant_color)
        context.move_to(*direction[0])
        context.line_to(*direction[1])
        context.line_to(*direction[2])
        context.line_to(*direction[0])
        context.close_path()
        context.fill()

    def draw_baits(self, context):
        for bait_x, bait_y in self.simulation.grid.baits:
            bait_x *= self.tile_width
            bait_y *= self.tile_height

            context.set_source_rgb(*self.bait_color)
            context.arc(bait_x + (self.tile_width / 2), bait_y + (self.tile_height / 2), self.tile_width / 3, 0, 2 * math.pi)
            context.fill()