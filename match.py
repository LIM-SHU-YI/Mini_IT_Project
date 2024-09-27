import pygame
import sys
import ctypes
import common
from button import Button

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memories")
icon = pygame.image.load("asset/image/gameicon.png")
pygame.display.set_icon(icon)

#Initialize for improved text input
#ctypes.windll.user32.SetProcessDPIAware()
# ctypes.windll.imm32.ImmDisableIME(0)

badendingtext = (
    "Bad Ending\n\n"
    "The Grim Reaper feeling confused or indifferent,\n"
    "continuing to coldly carry out his duties without change.\n\n"
    "Grim Reaper said:\n "
    "I will never understand these fleeting and fragile emotions.\n"
    "Perhaps they were never meant for me.\n\n\n"
    "-The End-"
)

happyendingtext = (
    "Happy Ending\n\n"
    "The Grim Reaper deciding to no longer carry out his duties coldly \nbut to guide souls more gently, "
    "allowing them to leave peacefully.\n\n"
    "Grim Reaper said:\n"
    "I once thought I was merely the one who takes life, \n"
    "but now I know that love is the true meaning of living.\n\n\n"
    "-The End-"
)

#Game states
MAIN_MENU = 0
KIDS_VIEW = 1
BOYFRIEND_VIEW = 2
DOGOWNER_VIEW = 3
DRAG_GAME = 4
EMOTION_GAME = 5
FINAL_RESULT = 6

#Interface images
interface_bg = pygame.image.load("Photo used/Match/interfaceview.png")
kidsinter_img = pygame.image.load("Photo used/Match/kidsinter.png")
kids_img = pygame.image.load("Photo used/Match/kids.png")
boyfriendinter_img = pygame.image.load("Photo used/Match/boyfriendinter.png")
boyfriend_img = pygame.image.load("Photo used/Match/boyfriend.png")
dogownerinter_img = pygame.image.load("Photo used/Match/dogownerinter.png")
dogowner_img = pygame.image.load("Photo used/Match/dogowner.png")
back_img = pygame.image.load("asset/image/return.png")
music_img = pygame.image.load("asset/image/m.png")
mute_img = pygame.image.load("asset/image/mm.png")

#Interface buttons
kidsinter_btn = Button(260, 245, image=kidsinter_img)
boyfriendinter_btn = Button(646, 236, image=boyfriendinter_img)
dogownerinter_btn = Button(1040, 236, image=dogownerinter_img)
back_btn = Button(50, 50, image=back_img,scale=0.27)
music_button = Button(1230, 50, image=music_img, scale=0.35)
mute_button = Button(1230, 50, image=mute_img, scale=0.35, visible=False)

def onoffm():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            common.running = False
            return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                common.click.play()
                common.music_on_off()
                return False
            elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                common.click.play()
                common.music_on_off()
                return False
    return False

def updatem(screen):
    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

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

class RELICSITEM:
    def __init__(self, screen):
        self.screen = screen
        self.all_items_placed = False
        self.game_started = False

        # Drag images
        self.interface_bg = pygame.image.load("Photo used/Match/interfaceview.png")
        self.start_btn_img = pygame.image.load("Photo used/Match/itemdragstart.png")
        self.envelop_img = pygame.image.load("Photo used/Match/envelop.png")
        self.flower_img = pygame.image.load("Photo used/Match/flower.png")
        self.bonepresent_img = pygame.image.load("Photo used/Match/bonepresent.png")
        self.kids_correct_img = pygame.image.load("Photo used/Match/kidscorrect.png")
        self.boyfriend_correct_img = pygame.image.load("Photo used/Match/boyfriendcorrect.png")
        self.dogowner_correct_img = pygame.image.load("Photo used/Match/dogownercorrect.png")

        # Drag buttons
        self.start_btn = Button(1040, 590, image=self.start_btn_img)

        # Draggable items
        self.items = [
            DraggableItem(940, 610, self.envelop_img, kidsinter_btn),
            DraggableItem(240, 600, self.flower_img, boyfriendinter_btn),
            DraggableItem(540, 600, self.bonepresent_img, dogownerinter_btn)
        ]

    def draw(self):
        self.screen.blit(self.interface_bg, (0, 0))
    
        if not self.items[0].placed_correctly:
            kidsinter_btn.update(self.screen)
        else:
            self.screen.blit(self.kids_correct_img, kidsinter_btn.rect)

        if not self.items[1].placed_correctly:
            boyfriendinter_btn.update(self.screen)
        else:
            self.screen.blit(self.boyfriend_correct_img, boyfriendinter_btn.rect)

        if not self.items[2].placed_correctly:
            dogownerinter_btn.update(self.screen)
        else:
            self.screen.blit(self.dogowner_correct_img, dogownerinter_btn.rect)
        
        if self.game_started:
            for item in self.items:
                item.draw(self.screen)
        else:
            self.start_btn.update(self.screen)
        back_btn.update(self.screen)


    def update(self, event_list):
        self.draw()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.checkforinput(event.pos) and not self.game_started:
                    self.game_started = True
                elif back_btn.checkforinput(event.pos):
                    common.click.play()
                    return "MAIN_MENU"

            if event.type == pygame.MOUSEBUTTONUP and self.game_started:
                for item in self.items:
                    if item.dragging and not item.placed_correctly:
                        if item.is_colliding_with(item.correct_gallery):
                            self.show_message("Correct!")
                            item.placed_correctly = True
                            item.visible = False
                        elif any(item.is_colliding_with(gallery) for gallery in [kidsinter_btn, boyfriendinter_btn, dogownerinter_btn]):
                            self.show_message("Incorrect!")
                            item.reset_position()
                        else:
                            item.reset_position()

        if self.game_started:
            for item in self.items:
                item.update(event_list)

            self.all_items_placed = all(item.placed_correctly for item in self.items)
            if self.all_items_placed:
                self.show_message("All relics give back to the owner and all of them become happy!")
                pygame.time.wait(2000)
                return "MAIN_MENU"

        return None

    def show_message(self, message):
        self.screen.fill((255, 255, 255))
        text, text_rect = common.normal_text(message, common.cutedisplay(30), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def reset(self):
        self.game_started = False
        self.all_items_placed = False
        for item in self.items:
            item.reset_position()
            item.placed_correctly = False
            item.visible = True

class EmotionGame:
    def __init__(self, screen):
        self.screen = screen
        self.current_emotion = ""
        self.user_text = ""
        self.total_hint_count = 2
        self.wrong_answers = 0
        self.completed_emotions = set()
        self.active = False
        self.input_rect = pygame.Rect(screen.get_width() // 2 - 70, 300, 140, 52)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.font = common.cutedisplay(32)
        
        # Emotion images
        self.kidsemo_img = pygame.image.load("Photo used/Match/emozuo.png")
        self.boyfriendemo_img = pygame.image.load("Photo used/Match/emozhong.png")
        self.dogowneremo_img = pygame.image.load("Photo used/Match/emoyou.png")
        self.hint_img = pygame.image.load("Photo used/Match/hint.png")

        # Emotion buttons
        self.kidsemo_btn = Button(260, 400, image=self.kidsemo_img)
        self.boyfriendemo_btn = Button(646, 400, image=self.boyfriendemo_img)
        self.dogowneremo_btn = Button(1040, 400, image=self.dogowneremo_img)
        self.hint_btn = Button(1200, 55, image=self.hint_img, scale=0.8)
        self.hint_text = f"HINT x{self.total_hint_count}"

        self.music_btn = None

        self.emotions = {
            "sad": ["sadness", "The little boy's mother died."],
            "angry": ["angriness", "Her boyfriend is late without any reason."],
            "happy": ["happiness", "The dog goes for a walk with its favorite owner."]
        }

        self.emotion_hint_count = {
            "sad": 0,
            "angry": 0,
            "happy": 0
        }


    def draw_emotion_buttons(self, screen):
        for emotion, btn in zip(["sad", "angry", "happy"], [self.kidsemo_btn, self.boyfriendemo_btn, self.dogowneremo_btn]):
            if emotion not in self.completed_emotions:
                btn.update(screen)
            else:
                pygame.draw.rect(screen, (255, 255, 255), btn.rect)
                text, text_rect = common.normal_text(emotion.capitalize(), common.cutedisplay(30), (0, 0, 0), btn.rect.center)
                screen.blit(text, text_rect)

    def check_emotion_button_click(self, pos):
        if self.kidsemo_btn.checkforinput(pos) and "sad" not in self.completed_emotions:
            self.current_emotion = "sad"
            self.current_hint = ""
            return True
        elif self.boyfriendemo_btn.checkforinput(pos) and "angry" not in self.completed_emotions:
            self.current_emotion = "angry"
            self.current_hint = ""
            return True
        elif self.dogowneremo_btn.checkforinput(pos) and "happy" not in self.completed_emotions:
            self.current_emotion = "happy"
            self.current_hint = ""
            return True
        return False

    def draw_emotion_question(self):
        self.screen.fill((255, 255, 255))
        back_btn.update(self.screen)
        
        if self.total_hint_count > 0:
            self.hint_btn.update(self.screen)
            
            # Display hint count
            hint_count_text, hint_count_rect = common.normal_text(self.hint_text, common.cutedisplay(20), (0, 0, 0), (1200, 110))
            self.screen.blit(hint_count_text, hint_count_rect)
        
        question_text, question_rect = common.normal_text("What is the emotion shown by this gallery?", common.cutedisplay(30), (0, 0, 0), (self.screen.get_width() // 2, 240))
        self.screen.blit(question_text, question_rect)

        color = self.color_active if self.active else self.color_passive
        pygame.draw.rect(self.screen, color, self.input_rect, 2)

        text_surface = self.font.render(self.user_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        self.input_rect.w = max(140, text_surface.get_width() + 10)

        if self.current_hint:
            hint_text, hint_rect = common.normal_text(self.current_hint, common.cutedisplay(24), (0, 0, 0), (self.screen.get_width() // 2, 400))
            self.screen.blit(hint_text, hint_rect)

    def draw_emotion_result(self, result):
        self.screen.fill((255, 255, 255))
        result_text, result_rect = common.normal_text(result, common.cutedisplay(50), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        emotion_text, emotion_rect = common.normal_text(f"The emotion was: {self.current_emotion}", common.cutedisplay(30), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(result_text, result_rect)
        self.screen.blit(emotion_text, emotion_rect)

    def get_hint(self):
        if self.total_hint_count > 0:
            self.total_hint_count -= 1
            self.emotion_hint_count[self.current_emotion] += 1
            
            if self.emotion_hint_count[self.current_emotion] == 1:
                self.current_hint = self.emotions[self.current_emotion][1]
            else:
                self.current_hint = f"The first letter is '{self.emotions[self.current_emotion][0][0]}'."
            
            # Update hint text
            self.hint_text = f"HINT x{self.total_hint_count}"
            return self.current_hint
        else:
            self.current_hint = "No more hints available."
            return self.current_hint

    def check_emotion_answer(self, user_input):
        correct_answers = [self.current_emotion, self.emotions[self.current_emotion][0]]
        if user_input.lower().strip() in [ans.lower() for ans in correct_answers]:
            self.completed_emotions.add(self.current_emotion)
            if len(self.completed_emotions) == 3:
                self.kidsemo_btn.visible = False
                self.boyfriendemo_btn.visible = False
                self.dogowneremo_btn.visible = False
            return True
        else:
            self.wrong_answers += 1
            return False
        
    def show_message(self, message):
        self.screen.fill((255, 255, 255))
        text, text_rect = common.normal_text(message, common.cutedisplay(30), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)

    def update(self, event_list):
        self.draw_emotion_question()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
                if self.total_hint_count > 0 and self.hint_btn.checkforinput(event.pos):
                    self.current_hint = self.get_hint()
                if back_btn.checkforinput(event.pos):
                    common.click.play()
                    return "MAIN_MENU"
               
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.check_emotion_answer(self.user_text):
                            self.completed_emotions.add(self.current_emotion)
                            self.show_message("Correct!")
                        else:
                            self.wrong_answers += 1
                            self.show_message("Wrong!")
                        
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        
                        if len(self.completed_emotions) == 3 or self.wrong_answers >= 3:
                            return "FINAL_RESULT"
                        else:
                            self.reset_current_emotion()
                            return "MAIN_MENU"
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

        self.draw_input_box()
        pygame.display.flip()
        return None

    def draw_input_box(self):
        color = self.color_active if self.active else self.color_passive
        pygame.draw.rect(self.screen, color, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(140, text_surface.get_width() + 10)

    def reset_current_emotion(self):
        self.user_text = ""
        self.current_hint = ""
        self.active = False

    def reset(self):
        self.user_text = ""
        self.total_hint_count = 2
        self.hint_text = f"HINT x{self.total_hint_count}"
        self.wrong_answers = 0
        self.completed_emotions = set()
        self.current_hint = ""
        self.active = False
        self.current_emotion = ""
        self.emotion_hint_count = {
            "sad": 0,
            "angry": 0,
            "happy": 0
        }

def draw_main_menu(screen, drag_game, emotion_game):
    screen.blit(interface_bg, (0, 0))
    if not drag_game.all_items_placed:
        drag_game.start_btn.update(screen)
    kidsinter_btn.update(screen)
    boyfriendinter_btn.update(screen)
    dogownerinter_btn.update(screen)
    if drag_game.all_items_placed:
        emotion_game.draw_emotion_buttons(screen)

def draw_view(screen, image):
    screen.blit(image, (0, 0))
    back_btn.update(screen)

def draw_final_result(screen, emotion_game):
    screen.fill((255, 255, 255))
    if len(emotion_game.completed_emotions) == 3:
        result_text = "The Grim Reaper have learned human emotions!"
        ending_text = happyendingtext
    else:
        result_text = "The Grim Reaper did not learn human emotions!"
        ending_text = badendingtext

    text, text_rect = common.normal_text(result_text, common.cutedisplay(60), (0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    
    if common.music_button.visible:
        common.music_button.update(screen)
    if common.mute_button.visible:
        common.mute_button.update(screen)

    pygame.display.flip()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:  # Display the result for 3 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
        
        #Redraw screen update music button state
        screen.fill((255, 255, 255))
        screen.blit(text, text_rect)
        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)
        pygame.display.flip()

    return display_ending_text(screen, ending_text)  

def drawtext(screen, text, font, colour, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        renderedtext = font.render(line, True, colour)
        screen.blit(renderedtext, (x, y + i * renderedtext.get_height()))

def display_ending_text(screen, text):
    starttime = pygame.time.get_ticks()
    displayduration = 30000
    font = common.cutedisplay(35)
    running = True

    while running:
        elapsedtime = pygame.time.get_ticks() - starttime
        screen.fill((0,0,0))
        drawtext(screen, text, font, (255, 255, 255), 50, 50)

        if common.music_button.visible:
            common.music_button.update(screen)
        if common.mute_button.visible:
            common.mute_button.update(screen)

        pygame.display.flip()

        if elapsedtime >= displayduration:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()
                elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                    common.click.play()
                    common.music_on_off()

        pygame.time.Clock().tick(60)

    return True

def match_main():
    current_state = MAIN_MENU
    drag_game = RELICSITEM(screen)
    emotion_game = EmotionGame(screen)

    clock = pygame.time.Clock()
    running = True

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == MAIN_MENU:
                    if drag_game.start_btn.checkforinput(event.pos) and not drag_game.all_items_placed:
                        common.click.play()
                        current_state = DRAG_GAME
                    elif kidsinter_btn.checkforinput(event.pos):
                        current_state = KIDS_VIEW
                    elif boyfriendinter_btn.checkforinput(event.pos):
                        current_state = BOYFRIEND_VIEW
                    elif dogownerinter_btn.checkforinput(event.pos):
                        current_state = DOGOWNER_VIEW
                    elif drag_game.all_items_placed:
                        emotion_clicked = emotion_game.check_emotion_button_click(event.pos)
                        if emotion_clicked:
                            current_state = EMOTION_GAME
                elif current_state in [KIDS_VIEW, BOYFRIEND_VIEW, DOGOWNER_VIEW]:
                    if back_btn.checkforinput(event.pos):
                        common.click.play()
                        current_state = MAIN_MENU

                if current_state != EMOTION_GAME:
                    if common.music_button.visible and common.music_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()
                    elif common.mute_button.visible and common.mute_button.checkforinput(pygame.mouse.get_pos()):
                        common.click.play()
                        common.music_on_off()

        if current_state == MAIN_MENU:
            draw_main_menu(screen, drag_game, emotion_game)
        elif current_state == KIDS_VIEW:
            draw_view(screen, kids_img)
        elif current_state == BOYFRIEND_VIEW:
            draw_view(screen, boyfriend_img)
        elif current_state == DOGOWNER_VIEW:
            draw_view(screen, dogowner_img)
        elif current_state == DRAG_GAME:
            drag_game_result = drag_game.update(event_list)
            if drag_game_result == "MAIN_MENU":
                current_state = MAIN_MENU
        elif current_state == EMOTION_GAME:
            emotion_game_result = emotion_game.update(event_list)
            if emotion_game_result == "MAIN_MENU":
                current_state = MAIN_MENU
            elif emotion_game_result == "FINAL_RESULT":
                current_state = FINAL_RESULT
        elif current_state == FINAL_RESULT:
            continue_game = draw_final_result(screen, emotion_game)
            if not continue_game:
                running = False
            else:
                running = False  # End the game after showing the ending

        if current_state != EMOTION_GAME and current_state != FINAL_RESULT:
            if common.music_button.visible:
                common.music_button.update(screen)
            if common.mute_button.visible:
                common.mute_button.update(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

common.music_playing = True
pygame.mixer.music.play(-1)  
# match_main()

#Debuging Use
#print(f"Before check: user_text='{self.user_text}', current_emotion='{self.current_emotion}'")
#print(f"Set current_emotion to: {self.current_emotion}") 
#print(f"Checking: user input '{user_input}' against '{self.current_emotion}'")
#print(f"Result: {result}")