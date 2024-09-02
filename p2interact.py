import pygame
import common
from button import Button

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

# Track the current drag object
current_dragging_obj = None

# Define the DraggableObject class
class DraggableObject:
    def __init__(self, image, center, draggable=True, visible=True):
        self.image = image
        self.original_center = center  # Store img back to the original position
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for pixel-perfect collision
        self.dragging = False
        self.draggable = draggable
        self.visible = visible

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event, other=None):
        global current_dragging_obj  # Use the global to track the current drag object

        if not self.draggable:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_x = self.rect.centerx - event.pos[0]
                self.offset_y = self.rect.centery - event.pos[1]
                current_dragging_obj = self  # Set the following object as the current drag one

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            current_dragging_obj = None  # Reset the current drag object

             # If the water object is dropped and it collides with blueempty
            if other and self.is_colliding_with(other):
                other.visible = True
                if self == dogfood_obj:
                # Only set redfull_obj visible when dogfood_obj is dropped on it
                    redfull_obj.visible = True
                elif self == water_obj:
                    # Ensure bluewater_obj is not affected by dogfood_obj drop
                    bluewater_obj.visible = True
            # Reset the position to the original center when the mouse is released
            self.rect.center = self.original_center

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.centerx = event.pos[0] + self.offset_x
                self.rect.centery = event.pos[1] + self.offset_y

    def is_colliding_with(self, other):
        # Calculate the offset between the two masks
        offset = (other.rect.left - self.rect.left, other.rect.top - self.rect.top)
        # Check for overlap between the masks
        return self.mask.overlap(other.mask, offset) is not None

# Load images
interface = pygame.image.load("asset/image/part2a/int.png")
redempty = pygame.image.load("asset/image/part2a/redempty.png")
redfull = pygame.image.load("asset/image/part2a/redfull.png")
blueempty = pygame.image.load("asset/image/part2a/blueempty.png")
bluewater = pygame.image.load("asset/image/part2a/bluewater.png")
water = pygame.image.load("asset/image/part2a/water.png")
toy = pygame.image.load("asset/image/part2a/toy.png")
dogfood = pygame.image.load("asset/image/part2a/dogfood.png")
bone = pygame.image.load("asset/image/part2a/bone.png")
heart = pygame.image.load("asset/image/part2a/1h.png")
heart2 = pygame.image.load("asset/image/part2a/2h.png")
heart3 = pygame.image.load("asset/image/part2a/3h.png")
heart4 = pygame.image.load("asset/image/part2a/4h.png")
sdog = pygame.image.load("asset/image/part2a/sdog.png")
clear = pygame.image.load("asset/image/part2a/clear.png")

# Initialize DraggableObjects
redempty_obj = DraggableObject(redempty, (900, 454), draggable=False, visible=True)
redfull_obj = DraggableObject(redfull, (900, 454), draggable=False, visible=False)
blueempty_obj= DraggableObject(blueempty, (1123, 457), draggable=False, visible=True)
bluewater_obj= DraggableObject(bluewater, (1123, 457), draggable=False, visible=False)
water_obj = DraggableObject(water, (1050, 627))
toy_obj = DraggableObject(toy, (240, 624))
dogfood_obj = DraggableObject(dogfood, (525, 625))
bone_obj = DraggableObject(bone, (805, 625))
sdog_obj = DraggableObject(sdog, (635, 283),draggable=False)

# Main function
def p2int():
    common.running = True
    global current_dragging_obj
    
    while common.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                print("Quit event detected in p2int()")
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()

            # Handle events for the draggable water object only, and pass blueempty_obj to check collision on drop
            water_obj.handle_event(event, blueempty_obj)
            dogfood_obj.handle_event(event, redfull_obj)
            toy_obj.handle_event(event)
            bone_obj.handle_event(event)
            sdog_obj.handle_event(event)

        # Clear screen
        screen.blit(clear, (0, 0))

        # Draw all objects except the currently dragged one
        for obj in [sdog_obj, redempty_obj, redfull_obj, blueempty_obj, bluewater_obj, water_obj, toy_obj, dogfood_obj, bone_obj]:
            if obj != current_dragging_obj:
                obj.draw(screen)

        # Draw the currently dragged object last, if any
        if current_dragging_obj:
            current_dragging_obj.draw(screen)


        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()


# Running for quick debug
# while common.running:
#     p2int()
#     pygame.display.flip()