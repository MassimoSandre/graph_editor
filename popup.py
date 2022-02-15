import pygame

class Popup:
    def __init__(self, message, box, display_time=None ) -> None:
        self.msg = message
        self.display_time = display_time
        self.to_display = 0

        self.box = box
        self.myfont = pygame.font.SysFont('Arial', 20)

    def show(self):
        if self.display_time == None:
            self.to_display = -1
        else:
            self.to_display = self.display_time

    def hide(self):
        self.to_display = 0

    def update(self):
        if self.to_display > 0:
            self.to_display -=1
    
    def render(self, screen):
        if self.to_display != 0:
            pygame.draw.rect(screen, (60,60,60), self.box, 0, 5)

            cx = self.box.x + int(self.box.w/2)
            cy = self.box.y + int(self.box.h/2)
            
            texts = self.myfont.render(str(self.msg), False, (255,255,255))
                    
            offset_x = int(texts.get_rect().width/2)
            offset_y = int(texts.get_rect().height/2)
            screen.blit(texts,(cx-offset_x, cy-offset_y))
