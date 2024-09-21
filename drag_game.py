import pygame
import common
from button import Button

class DraggableItem:
    def __init__(self, x, y, image, correct_gallery):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.original_pos = (x, y)
        self.correct_gallery = correct_gallery
        self.visible = True
        self.placed_correctly = False

    def update(self, event_list):
        if not self.visible or self.placed_correctly:
            return

        mouse_pos = pygame.mouse.get_pos()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    relative_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
                    if self.rect.collidepoint(mouse_pos) and self.mask.get_at(relative_pos):
                        self.dragging = True
                        self.offset_x = self.rect.x - mouse_pos[0]
                        self.offset_y = self.rect.y - mouse_pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

        if self.dragging:
            self.rect.x = mouse_pos[0] + self.offset_x
            self.rect.y = mouse_pos[1] + self.offset_y

    def draw(self, surface):
        if self.visible and not self.placed_correctly:
            surface.blit(self.image, self.rect)

    def reset_position(self):
        self.rect.topleft = self.original_pos

    def is_colliding_with(self, button):
        if not button.rect:
            return False
        offset = (button.rect.x - self.rect.x, button.rect.y - self.rect.y)
        return self.mask.overlap(pygame.mask.from_surface(button.image), offset) is not None

class DragGame:
    def __init__(self, screen):
        self.screen = screen
        self.all_items_placed = False
        self.game_started = False

        # Load images
        self.interface_bg = pygame.image.load("Photo used/Match/interfaceview.png")
        self.envelop_img = pygame.image.load("Photo used/Match/envelop.png")
        self.flower_img = pygame.image.load("Photo used/Match/flower.png")
        self.bonepresent_img = pygame.image.load("Photo used/Match/bonepresent.png")
        self.start_btn_img = pygame.image.load("Photo used/Match/itemdragstart.png")
        self.kidsinter_img = pygame.image.load("Photo used/Match/kidsinter.png")
        self.boyfriendinter_img = pygame.image.load("Photo used/Match/boyfriendinter.png")
        self.dogownerinter_img = pygame.image.load("Photo used/Match/dogownerinter.png")
        
        # Create buttons
        self.kidsinter_btn = Button(260, 245, image=self.kidsinter_img)
        self.boyfriendinter_btn = Button(646, 236, image=self.boyfriendinter_img)
        self.dogownerinter_btn = Button(1040, 236, image=self.dogownerinter_img)
        self.start_btn = Button(1040, 590, image=self.start_btn_img)
        self.back_btn = Button(50, 50, text_input="BACK", font=common.arcade(30), base_color="White", hovering_color="Gray")

        # Create draggable items
        self.items = [
            DraggableItem(940, 610, self.envelop_img, self.kidsinter_btn),
            DraggableItem(240, 590, self.flower_img, self.boyfriendinter_btn),
            DraggableItem(540, 585, self.bonepresent_img, self.dogownerinter_btn)
        ]

    def draw(self):
        self.screen.blit(self.interface_bg, (0, 0))
        self.kidsinter_btn.update(self.screen)
        self.boyfriendinter_btn.update(self.screen)
        self.dogownerinter_btn.update(self.screen)
        if self.game_started:
            for item in self.items:
                item.draw(self.screen)
        else:
            self.start_btn.update(self.screen)
        self.back_btn.update(self.screen)

    def update(self, event_list):
        self.draw()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.checkforinput(event.pos) and not self.game_started:
                    self.game_started = True
                elif self.back_btn.checkforinput(event.pos):
                    return "MAIN_MENU"

            if event.type == pygame.MOUSEBUTTONUP and self.game_started:
                for item in self.items:
                    if item.dragging and not item.placed_correctly:
                        if item.is_colliding_with(item.correct_gallery):
                            self.show_message("Correct!")
                            item.placed_correctly = True
                            item.visible = False
                        elif any(item.is_colliding_with(gallery) for gallery in [self.kidsinter_btn, self.boyfriendinter_btn, self.dogownerinter_btn]):
                            self.show_message("Incorrect!")
                            item.reset_position()
                        else:
                            item.reset_position()

        if self.game_started:
            for item in self.items:
                item.update(event_list)

            self.all_items_placed = all(item.placed_correctly for item in self.items)
            if self.all_items_placed:
                self.show_message("All items placed correctly!")
                return "MAIN_MENU"

        return None

    def show_message(self, message):
        self.screen.fill((255, 255, 255))
        text, text_rect = common.normal_text(message, common.arcade(30), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        common.pygame.display.flip()
        common.pygame.time.wait(2000)

    def reset(self):
        self.game_started = False
        self.all_items_placed = False
        for item in self.items:
            item.reset_position()
            item.placed_correctly = False
            item.visible = True