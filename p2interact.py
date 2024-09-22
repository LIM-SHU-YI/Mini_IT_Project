import pygame
import common
from button import Button
import doglearning

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_caption("Memories")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
# Track the current drag object
current_dragging_obj = None

# Event tracking variables
dogfood_dropped = False
water_dropped = False
toy_dropped = False
bone_dropped = False
choco_dropped = False

(be, be_rect) = common.normal_text("Bad ending :( Your dog died... You are a terrible person = =", common.cutedisplay(50), "White", pos=(640, 300))
(fr, fr_rect) = common.normal_text("You do know that chocolate is poisonous to dogs, right?", common.cutedisplay(50), "White", pos=(640, 420))
(oh, oh_rect) = common.normal_text("Oh, sure, giving chocolate to dogs is such a brilliant idea.", common.cutedisplay(50), "White", pos=(640, 300))
(what, what_rect) = common.normal_text("What could possibly go wrong? ;)", common.cutedisplay(50), "White", pos=(640, 420))


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

    def handle_event(self, event, *others):
        global current_dragging_obj, dogfood_dropped, water_dropped, toy_dropped, bone_dropped, choco_dropped # Use the global to track the current drag object

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

            for other in others:
                    # If the water object is dropped and it collides with blueempty
                if self.is_colliding_with(other):
                    if self == dogfood_obj:
                    # Only set redfull_obj visible when dogfood_obj is dropped on it
                        redfull_obj.visible = True
                        dogfood_dropped = True  # Mark dogfood event as occurred
                        
                    elif self == water_obj:
                        # Ensure bluewater_obj is not affected by dogfood_obj drop
                        bluewater_obj.visible = True
                        water_dropped = True  # Mark water event as occurred

                    elif self == toy_obj:
                        toy_dropped = True

                    elif self == bone_obj:
                        bone_dropped = True

                    elif self == choco_obj:

                        screen.fill((0, 0, 0))
                        screen.blit(oh, oh_rect)
                        screen.blit(what, what_rect)
                        pygame.display.flip()
                        
                        start_time = pygame.time.get_ticks()
                        while common.running:
                            current_time = pygame.time.get_ticks()
                            elapsed_time = current_time - start_time
                            # Check if the 4 seconds have passed
                            if elapsed_time >= 4000:      # 4000 milliseconds = 4 seconds
                                break

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    common.running = False
                                    return
                                
                            pygame.time.wait(100)
                        
                        common.fade_in(screen, dead, duration=2000)
                        pygame.display.flip()

                        start_time = pygame.time.get_ticks()
                        while common.running:
                            current_time = pygame.time.get_ticks()
                            elapsed_time = current_time - start_time
                            if elapsed_time >= 2000:
                                common.fade_out(screen, dead, duration=1000)
                                break

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    common.running = False
                                    return

                            pygame.time.wait(100)

                        common.fade_in(screen, dead2, duration=2000)
                        pygame.display.flip()

                        start_time = pygame.time.get_ticks()
                        while common.running:
                            current_time = pygame.time.get_ticks()
                            elapsed_time = current_time - start_time
                            if elapsed_time >= 2000:
                                common.fade_out(screen, dead2, duration=1000)
                                break

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    common.running = False
                                    return
                            pygame.time.wait(100)

                        screen.fill((0, 0, 0))
                        screen.blit(be, be_rect)
                        screen.blit(fr, fr_rect)
                        pygame.display.flip()
                        choco_dropped = True
                        stop_scene = True
                        while stop_scene:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    stop_scene = False  # Allow the game to quit
                                    common.running = False
                            # Limit the loop to avoid high CPU usage
                            pygame.time.wait(100)
                                        
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
choco = pygame.image.load("asset/image/part2a/choco.png")
dead = pygame.image.load("asset/image/part2a/dead.png")
dead2 = pygame.image.load("asset/image/part2a/dead2.png")
button_bg = pygame.image.load("asset/image/buttonbg.png")
ending = pygame.image.load("asset/image/part2a/ending.png")

def rundl():
    # pygame.time.wait(2000)
    common.fade_in(screen, button_bg, duration=1000)
    pygame.display.flip()

    start_time = pygame.time.get_ticks()
    while common.running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        if elapsed_time >= 3000:
            doglearning.doglearning_main_game_loop()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common.running = False
                return
        pygame.time.wait(100)

# Initialize DraggableObjects
redempty_obj = DraggableObject(redempty, (900, 454), draggable=False, visible=True)
redfull_obj = DraggableObject(redfull, (900, 454), draggable=False, visible=False)
blueempty_obj= DraggableObject(blueempty, (1123, 457), draggable=False, visible=True)
bluewater_obj= DraggableObject(bluewater, (1123, 457), draggable=False, visible=False)
water_obj = DraggableObject(water, (1140, 627))
toy_obj = DraggableObject(toy, (150, 624))
dogfood_obj = DraggableObject(dogfood, (415, 625))
bone_obj = DraggableObject(bone, (915, 625))
sdog_obj = DraggableObject(sdog, (635, 283), draggable=False)
choco_obj = DraggableObject(choco, (665,625))

# Main function
def p2int():
    common.running = True
    global current_dragging_obj

    delay = None

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
            dogfood_obj.handle_event(event, redempty_obj)
            toy_obj.handle_event(event, sdog_obj)
            bone_obj.handle_event(event, sdog_obj)
            choco_obj.handle_event(event, redempty_obj, blueempty_obj, sdog_obj)


        screen.blit(clear, (0, 0))

        # Draw all objects except the currently dragged one
        for obj in [sdog_obj, redempty_obj, redfull_obj, blueempty_obj, bluewater_obj, water_obj, toy_obj, dogfood_obj, bone_obj, choco_obj]:
            if obj != current_dragging_obj:
                obj.draw(screen)

        # Draw the currently dragged object last, if any
        if current_dragging_obj:
            current_dragging_obj.draw(screen)

        tracking_count = sum([dogfood_dropped, water_dropped, toy_dropped, bone_dropped])
        # display hearts based on number of tracking triggered
        if tracking_count == 4 and delay is None:
            screen.blit(heart4, (0, 0))  # Display heart4 if all four events occurred
            delay = pygame.time.get_ticks()
        elif tracking_count == 3:
            screen.blit(heart3, (0, 0))  # Display heart3 if three events occurred
        elif tracking_count == 2:
            screen.blit(heart2, (0, 0))  # Display heart2 if two events occurred
        elif tracking_count == 1:
            screen.blit(heart, (0, 0))   # Display heart if only one event occurred

        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)
        
        if delay:
            screen.blit(ending, (0, 0))
            if common.music_button.visible:
                common.music_button.update(screen)
            if common.mute_button.visible:
                common.mute_button.update(screen)
            pygame.display.flip()
            current_time = pygame.time.get_ticks()
            if current_time - delay >= 850:
                rundl()  # Call the rundl function after the delay
                delay = None  # Reset delay to avoid repeated calls

        # Update the display
        pygame.display.flip()

    pygame.quit()


# Running for quick debug
# while common.running:
#     p2int()
#     pygame.display.flip()