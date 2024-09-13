import pygame

class Button:
    def __init__(self, x, y, image=None, text_input=None, font=None, base_color="White", hovering_color="Blue", scale=1.0, shadow_color="Black", shadow_offset=(7, 7), visible=True, shadow_on=True):
        self.x_pos = x
        self.y_pos = y
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.visible = visible
        self.shadow_on = shadow_on

        if image is not None:
            # Image button
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.mask = pygame.mask.from_surface(self.image)  # Create a mask for the image
        else:
            # Text button
            self.image = None
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

            if self.shadow_on:
                # if dw shadow just False
                self.shadow = self.font.render(self.text_input, True, self.shadow_color)
                self.shadow_rect = self.shadow.get_rect(center=(self.x_pos + self.shadow_offset[0], self.y_pos + self.shadow_offset[1]))

        self.clicked = False


    def update(self, surface):
        if not self.visible:
            return

        if self.image is not None:
            # Image button
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                # Check if the mouse is hovering over a non-transparent pixel
                mouse_x = pos[0] - self.rect.left
                mouse_y = pos[1] - self.rect.top
                if self.mask.get_at((mouse_x, mouse_y)):
                    self.image.set_alpha(128)  # Half opacity when hover on
                else:
                    self.image.set_alpha(255)  # Full opacity when not hovered
            else:
                self.image.set_alpha(255)  # Full opacity when not hovered
            surface.blit(self.image, self.rect)

        else:
            # Text button
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.text = self.font.render(self.text_input, True, self.hovering_color)  # Change text color on hover
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)

            if self.shadow_on:
                surface.blit(self.shadow, self.shadow_rect)
            surface.blit(self.text, self.rect)


    def checkforinput(self, position):
        return self.rect.collidepoint(position)

    def set_base_color(self, color):
        self.base_color = color

    def set_hovering_color(self, color):
        self.hovering_color = color