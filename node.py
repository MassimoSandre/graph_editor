import pygame
import math

class Node():
    def __init__(self, pos_x, pos_y, radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.arc_radius = 12
        self.arcs = []
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.selected = False

    def add_arc(self, dest_obj, weight, displayed):
        self.arcs.append([dest_obj, weight, displayed])

    def select(self, select):
        self.selected = select

    def get_selected_arc_destination(self, pos_x, pos_y):
        for a in self.arcs:
            if a[2]:
                x1, y1 = self.get_position()
                x2, y2 = a[0].get_position()

                cx = int((x1 + x2)/2)
                cy = int((y1 + y2)/2)
                
                d = math.sqrt((cx - pos_x)**2 + (cy - pos_y)**2)

                if d < self.arc_radius:
                    return a[0]

        return None


    def remove_arc(self, dest_obj, displayed):
        if displayed:
            dest_obj.remove_arc(self, False)
        found = False
        for a in self.arcs:
            if a[0] == dest_obj:
                self.arcs.remove(a)
                break

    def edit_arc(self, dest_obj, weight, displayed):
        if displayed:
            dest_obj.edit_arc(self, weight, False)
            
        
        found = False
        for a in self.arcs:
            if a[0] == dest_obj:
                found = True
                a[1] = weight
                a[2] = displayed
                break
        # cerca l'arco che punta a dest_obj e modificalo con il nuovo peso
        # se l'arco non viene trovato si chiama la funzione add_arc, con gli stessi parametri
        if not found:
            self.add_arc(dest_obj, weight, displayed)


    def get_arc_weight(self, dest_obj):
        for a in self.arcs:
            if a[0] == dest_obj:
                return a[1]
        return None

    def translate(self, comp_x, comp_y):
        self.pos_x += comp_x
        self.pos_y += comp_y

    def is_inside(self, point_x, point_y):
        d = math.sqrt((point_x - self.pos_x)**2 + (point_y - self.pos_y)**2)

        if d > self.radius:
            return False

        return True

    def get_position(self):
        return (self.pos_x, self.pos_y)


    def render_arcs(self,screen, mouse_pos):
        for a in self.arcs:
            if a[2]:
                x1, y1 = self.get_position()
                x2, y2 = a[0].get_position()

                cx = int((x1 + x2)/2)
                cy = int((y1 + y2)/2)
                
                d = math.sqrt((cx - mouse_pos[0])**2 + (cy - mouse_pos[1])**2)    

                pygame.draw.line(screen, (255,255,255), (x1, y1), (x2,y2))

                if d < self.arc_radius:
                    pygame.draw.circle(screen, (255,255,255), (cx, cy),self.arc_radius, 0)
                    texts = self.myfont.render(str(a[1]), False, (0,0,0))
                else:
                    pygame.draw.circle(screen, (0,0,0), (cx, cy),self.arc_radius, 0)
                    texts = self.myfont.render(str(a[1]), False, (255,255,255))
                
                offset_x = int(texts.get_rect().width/2)
                offset_y = int(texts.get_rect().height/2)
                screen.blit(texts,(cx-offset_x, cy-offset_y))


    def render(self, screen):
        #pygame.draw.circle(screen, (0,0,0), self.get_position(),self.radius, 0)
        if self.selected:
            pygame.draw.circle(screen, (255,0,0), self.get_position(),self.radius, 0)
        else:
            pygame.draw.circle(screen, (255,255,255), self.get_position(),self.radius, 0)

    def render_text(self, screen, message):
        texts = self.myfont.render(str(message), False, (0,0,0))
        offset_x = int(texts.get_rect().width/2)
        offset_y = int(texts.get_rect().height/2)
        screen.blit(texts,(self.pos_x-offset_x, self.pos_y-offset_y))

