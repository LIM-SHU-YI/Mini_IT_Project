import pygame
import common
from button import Button

class EmotionGame:
    def __init__(self, screen):
        self.screen = screen
        self.current_emotion = ""
        self.user_text = ""
        self.hint_count = 0
        self.total_hint_count = 0
        self.wrong_answers = 0
        self.completed_emotions = set()
        self.current_hint = ""
        self.active = False
        self.input_rect = pygame.Rect(screen.get_width() // 2 - 70, 300, 140, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.font = common.arcade(32)  # Using the common.arcade font

        # Load emotion button images
        self.kidsemo_img = pygame.image.load("Photo used/Match/emozuo.png")
        self.boyfriendemo_img = pygame.image.load("Photo used/Match/emozhong.png")
        self.dogowneremo_img = pygame.image.load("Photo used/Match/emoyou.png")

        # Create emotion buttons
        self.kidsemo_btn = Button(260, 400, image=self.kidsemo_img)
        self.boyfriendemo_btn = Button(646, 400, image=self.boyfriendemo_img)
        self.dogowneremo_btn = Button(1040, 400, image=self.dogowneremo_img)

        self.hint_btn = Button(screen.get_width() - 150, 50, text_input="HINT", font=common.arcade(30), base_color="Black", hovering_color="Gray")
        self.back_btn = Button(50, 50, text_input="BACK", font=common.arcade(30), base_color="Black", hovering_color="Gray")

    def draw_emotion_buttons(self, screen):
        for emotion, btn in zip(["sad", "angry", "happy"], [self.kidsemo_btn, self.boyfriendemo_btn, self.dogowneremo_btn]):
            if emotion not in self.completed_emotions:
                btn.update(screen)
            else:
                pygame.draw.rect(screen, (255, 255, 255), btn.rect)
                text, text_rect = common.normal_text(emotion.capitalize(), common.arcade(30), (0, 0, 0), btn.rect.center)
                screen.blit(text, text_rect)

    def check_emotion_button_click(self, pos):
        if self.kidsemo_btn.checkforinput(pos) and "sad" not in self.completed_emotions:
            self.current_emotion = "sad"
            return True
        elif self.boyfriendemo_btn.checkforinput(pos) and "angry" not in self.completed_emotions:
            self.current_emotion = "angry"
            return True
        elif self.dogowneremo_btn.checkforinput(pos) and "happy" not in self.completed_emotions:
            self.current_emotion = "happy"
            return True
        return False

    def draw_emotion_question(self):
        self.screen.fill((255, 255, 255))
        self.back_btn.update(self.screen)
        self.hint_btn.update(self.screen)
        
        question_text, question_rect = common.normal_text("What is the emotion showed by this gallery?", common.arcade(30), (0, 0, 0), (self.screen.get_width() // 2, 200))
        self.screen.blit(question_text, question_rect)

        # Draw input box
        color = self.color_active if self.active else self.color_passive
        pygame.draw.rect(self.screen, color, self.input_rect, 2)

        # Render user input text
        text_surface = self.font.render(self.user_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # Adjust input box width if needed
        self.input_rect.w = max(140, text_surface.get_width() + 10)

        if self.current_hint:
            hint_text, hint_rect = common.normal_text(self.current_hint, common.arcade(24), (0, 0, 0), (self.screen.get_width() // 2, 400))
            self.screen.blit(hint_text, hint_rect)

    def draw_emotion_result(self, result):
        self.screen.fill((255, 255, 255))
        result_text, result_rect = common.normal_text(result, common.arcade(50), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        emotion_text, emotion_rect = common.normal_text(f"The emotion was: {self.current_emotion}", common.arcade(30), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(result_text, result_rect)
        self.screen.blit(emotion_text, emotion_rect)

    def get_hint(self):
        if self.total_hint_count < 2 and self.hint_count < 2:
            self.hint_count += 1
            self.total_hint_count += 1
            if self.hint_count == 1:
                self.current_hint = f"The answer has {len(self.current_emotion)} letters."
            else:
                self.current_hint = f"The first letter is '{self.current_emotion[0]}'."
        else:
            self.current_hint = "No more hints available."
        return self.current_hint

    def check_emotion_answer(self, user_input):
        return user_input.lower() == self.current_emotion

    def show_message(self, message):
        self.screen.fill((255, 255, 255))
        text, text_rect = common.normal_text(message, common.arcade(30), (0, 0, 0), (self.screen.get_width() // 2, self.screen.get_height() // 2))
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
                if self.hint_btn.checkforinput(event.pos):
                    self.current_hint = self.get_hint()
                if self.back_btn.checkforinput(event.pos):
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
                        self.draw_emotion_result("Correct!" if self.current_emotion in self.completed_emotions else "Wrong!")
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Show result for 2 seconds
                        if len(self.completed_emotions) == 3 or self.wrong_answers >= 2:
                            return "FINAL_RESULT"
                        else:
                            return "MAIN_MENU"
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

        return None

    def reset(self):
        self.user_text = ""
        self.hint_count = 0
        self.current_hint = ""
        self.active = False