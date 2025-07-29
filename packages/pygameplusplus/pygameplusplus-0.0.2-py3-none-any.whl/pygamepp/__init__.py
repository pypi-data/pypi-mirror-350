
import pygame as pg
import sys
import os
import cairosvg
import io
sys.dont_write_bytecode = True
if __name__ == '__main__':
    import colors
    import keys
    import errors
else:
    from . import colors
    from . import keys
    from . import errors
def svg2surface(path):
    png_data = cairosvg.svg2png(url=path)
    return io.BytesIO(png_data)  # This acts like a file object

def soundinit():
    pg.mixer.init()

def playsound(path, volume=1.0, loop=False):
    """
    Plays a sound file.

    Parameters:
    path (str): Path to the sound file (.wav, .ogg, etc).
    volume (float): Volume level from 0.0 to 1.0.
    loop (bool): Whether the sound should loop continuously.
    """
    try:
        sound = pg.mixer.Sound(path)
        sound.set_volume(volume)
        loops = -1 if loop else 0  # -1 means loop forever
        sound.play(loops=loops)
    except pg.error as e:
        print(f"[playsound] Error playing sound '{path}': {e}")


def dirname():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)
def turntocurrent():
    os.chdir(dirname())
class Game:
    def __init__(self, width=800, height=600, title="Pygame++", fullscreen=False, resizeable=True):
        turntocurrent()
        pg.init()
        
        flags = (pg.RESIZABLE if resizeable else 0) | (pg.FULLSCREEN if fullscreen else 0)
        self.screen = pg.display.set_mode((width, height), flags)
        self.set_icon("icon.png")
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        draw = globals().get("draw")
        update = globals().get("update")

        while self.running:
            events = pg.event.get()  # Get events once

            for event in events:
                if event.type == pg.QUIT:
                    self.running = False

            if callable(update):
                update(self, events)  # Pass events here

            self.screen.fill((0, 0, 0))

            if callable(draw):
                draw(self)

            pg.display.flip()
            self.clock.tick(60)

    pg.quit()

    def drawcircle(self, color, pos, radius):
        pg.draw.circle(self.screen, color, pos, radius)
    def draw_image(self,path, position=(0,0)):
        """
        Draws an image at the specified position on the screen.

        Parameters:
        path (str): Path to the image file.
        position (tuple): (x, y) coordinates where the image should be drawn.
        """
        try:
            image = pg.image.load(path).convert_alpha()
            self.screen.blit(image, position)
        except pg.error as e:
            raise errors.AssetNotFoundError(f'failed loading image {path}: {e}')
    def handle_keys(self, keymap):
        """
    Handles key input based on a provided keymap.

    Parameters:
        keymap (dict): Dictionary mapping pygame key constants to functions.
        """
        keys = pg.key.get_pressed()
        for key, action in keymap.items():
            if keys[key]:
                action(self)
    def set_icon(self, path):
        """
        Sets the window icon using an image at the given path.

        Parameters:
        path (str): Path to the icon image file.
        """
        try:
            icon = pg.image.load(path).convert_alpha()
            pg.display.set_icon(icon)
        except pg.error as e:
            raise errors.AssetNotFoundError(f'failed loading icon {path}: {e}')

class Sprite:
    def __init__(self, image_path=None, position=(0, 0), scale=1.0):
        self.imagepath = image_path
        self._dragging = False
        self._drag_offset = (0, 0)
        self.angle=0
        self.pos = position  # store top-left position
        



        try:
            self.original_image = pg.image.load(self.imagepath).convert_alpha()
            if scale != 1.0:
                width = int(self.original_image.get_width() * scale)
                height = int(self.original_image.get_height() * scale)
                self.image = pg.transform.scale(self.original_image, (width, height))
            else:
                self.image = self.original_image
            self.scale = scale  # save for animation

            self.rect = self.image.get_rect(center=self.pos)

        except pg.error as e:
            print(f"Error loading sprite image '{image_path}': {e}")
            self.image = None
            self.rect = pg.Rect(position, (0, 0))
        self.center = self.rect.center

    def make_draggable(self):
        "call this function once"
        self._dragging = False
        self._drag_offset = (0, 0)
    def handle_drag(self,eventss):
            """
            To handle dragging, Call this function in your loop
            """
            for event in eventss:
                if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                    self._dragging = True
                    mouse_x, mouse_y = event.pos
                    self._drag_offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

                elif event.type == pg.MOUSEBUTTONUP:
                    self._dragging = False

                elif event.type == pg.MOUSEMOTION and self._dragging:
                    mouse_x, mouse_y = event.pos
                    self.rect.x = mouse_x + self._drag_offset[0]
                    self.rect.y = mouse_y + self._drag_offset[1]
                    self.pos = (self.rect.x, self.rect.y)
    def draw(self, gamee):
        """Draws the sprite on the screen."""
        if self.image:
            #self.image = pg.image.load(self.imagepath).convert_alpha()
            gamee.screen.blit(self.image, self.rect.topleft)

    def move(self, dx=0, dy=0):
        """Moves the sprite by (dx, dy)."""
        self.rect.x += dx
        self.rect.y += dy

    def collides_with(self, other_sprite):
        """
        Checks collision with another sprite.

        Parameters:
        other_sprite (Sprite): Another instance of Sprite.

        Returns:
        bool: True if the sprites collide, False otherwise.
        """
        return self.rect.colliderect(other_sprite.rect)
    def animate(self, foldername, fps=10):
        now = pg.time.get_ticks()

        if not hasattr(self, 'frames') or not self.frames:
            print("Loading frames...")
            self.frames = []
            for filename in sorted(os.listdir(foldername)):
                if filename.lower().endswith(('.png', '.jpg', '.bmp', '.jpeg')):
                    path = os.path.join(foldername, filename)
                    print("Loading:", filename)
                    img = pg.image.load(path).convert_alpha()
                    self.frames.append(img)

            if self.frames:
                self.current_frame = 0
                self.last_update = now
                self.frame_delay = 1000 // fps

        if hasattr(self, 'frames') and self.frames and now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            raw_frame = self.frames[self.current_frame]

            self.original_image = self._apply_scale(raw_frame)
            self.image = self._apply_rotation(self.original_image)
            self.rect = self.image.get_rect(center=self.center)



            self.last_update = now


    def wasd(self,gamee):
        themap={
            keys.w: lambda g: self.move(dy=-5),
            keys.s: lambda g: self.move(dy=5),
            keys.a: lambda g: self.move(dx=-5),
            keys.d: lambda g: self.move(dx=5)
        }
        gamee.handle_keys(themap)
    def on_click(self, func):
        """
    Sets a function to be called when the sprite is clicked.
    """
        self._click_callback = func

    def handle_click(self, eventss, debug=False):
        """
    Checks if the sprite is clicked and calls the click callback.
    """
        print("Running") if debug else 0
        for event in eventss:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                print(f"Mouse clicked at {event.pos}, sprite rect: {self.rect}")
                if hasattr(self, '_click_callback'):
                    self._click_callback()
    def rotate(self, angle):
        """Rotates the sprite by the given angle (degrees)."""
        self.angle = (self.angle + angle) % 360
        if hasattr(self, 'original_image'):
            self.image = self._apply_rotation(self.original_image)
            self.rect = self.image.get_rect(center=self.center)


    def _apply_rotation(self, image):
        return pg.transform.rotate(image, -self.angle)

    def _apply_scale(self, image):
        if self.scale != 1.0:
            w = int(image.get_width() * self.scale)
            h = int(image.get_height() * self.scale)
            return pg.transform.scale(image, (w, h))
        return image



# User-defined draw and update function


if __name__ == "__main__":

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    game = Game(resizeable=True, title='Test')
    soundinit()

    test = Sprite(svg2surface('someassets/annesbot.svg'), scale=20.0, position=(100,100))
    test.make_draggable()
    test.on_click(lambda: print("clicked"))
    

    playsound('someassets/music/droopy_face.ogg', loop=True)

    def draw(game):
        game.drawcircle(colors.red, (400, 300), 50)
        test.draw(game)

    def update(game, events):
        #test.animate('someassets/dozer')  # ← here!
        test.handle_drag(events)
        test.wasd(game)
        test.handle_click(eventss=events)
        test.rotate(1)



    game.draw = draw
    game.update = update
    game.run()
