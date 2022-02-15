# TODO
# finish shortest path implementation (line 126)
# mst button and implementation
# zoom implementation
# selection and multiple node dragging implementation

import pygame
import random 
from pygame.locals import *
from node import Node
from button import Button
from popup import Popup


def compute_distance(starting_node, results, graph):

    queue = [(starting_node, 0)]

    while len(queue) > 0:
        current_node, distance = queue.pop(0)
        if results[graph.index(current_node)] > distance:
            results[graph.index(current_node)] = distance
            for n in current_node.arcs:
                if distance + n[1] < results[graph.index(n[0])]:
                    queue.append((n[0], distance + n[1]))
            

CIRCLE_RADIUS = 15

size = width, height = 620, 540

black = 0,0,0
white = 255,255,255
blue = 0,0,255

screen = pygame.display.set_mode(size) # RESIZABLE

clock = pygame.time.Clock()

obj_list = []
#x = Node(1,2,20,50)
#obj_list.append(x)

# BUTTONS
distance_button = Button((10,490),100, 35, "Distance")
shortest_path_button = Button((120, 490), 100, 35, "Shortest Path")

distance_results = []
distance_done = False

drawing = False
dragging = False
moved = False
connecting = False
dragging_index = 0

distance = False

shortest_path_start = False
shortest_path_end = False

selection = None


editing = False
editing_information = (0,0)
current_value = ""

# POPUPS
DEFAULT_POPUP_RECT = pygame.Rect(100,10,420,40)

distance_popup = Popup("Select the starting node", DEFAULT_POPUP_RECT)

shortest_path_start_popup = Popup("Select the starting node", DEFAULT_POPUP_RECT)
shortest_path_end_popup = Popup("Select the ending node", DEFAULT_POPUP_RECT)

while True:
    screen.fill(black)

    if not editing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    # left click
                    mouse_x, mouse_y = event.pos
                    
                    if distance:
                        if distance_button.is_inside(event.pos):
                            
                            distance = False
                            distance_popup.hide()
                        else:
                            for ob in obj_list:
                                if ob.is_inside(mouse_x, mouse_y):
                                    distance_done = True
                                    distance = False
                                    distance_results = [float("inf")]*len(obj_list)
                                    ob.select(True)

                                    compute_distance(ob, distance_results, obj_list)
                                    distance_popup.hide()
                                    break
                    elif shortest_path_start:
                        if shortest_path_button.is_inside(event.pos):
                            shortest_path_start = False
                            shortest_path_start_popup.hide()
                        else:
                            for ob in obj_list:
                                if ob.is_inside(mouse_x, mouse_y):
                                    shortest_path_start = False
                                    shortest_path_end = True
                                    selection = obj_list.index(ob)
                                    ob.select(True)
                                    shortest_path_start = False
                                    shortest_path_start_popup.hide()
                                    shortest_path_end.show()
                                    break

                    elif shortest_path_end:
                        if shortest_path_button.is_inside(event.pos):
                            shortest_path_end = False
                            shortest_path_end_popup.hide()
                        else:
                            for ob in obj_list:
                                if ob.is_inside(mouse_x, mouse_y):
                                    # TODO:
                                    # computer distance and then compute the path between 'selection' and ob
                                    # somehow highlight this path
                                    pass
                    else:
                        if distance_button.is_inside(event.pos):
                            distance = True
                            distance_popup.show()
                        elif shortest_path_button.is_inside(event.pos):
                            shortest_path_start = True
                            shortest_path_end = False
                            shortest_path_start_popup.show()
                        else:
                            i = 0
                            if connecting:
                                starting_index = dragging_index
                            dragging_index = None
                            f = False
                            for ob in obj_list:
                                if ob.is_inside(mouse_x, mouse_y):
                                    if not connecting:
                                        dragging = True
                                        moved = False
                                        dragging_index = i
                                        starting_x = mouse_x
                                        starting_y = mouse_y
                                    else:
                                        dragging_index = i

                                    f = True
                                    break
                                i = i + 1

                            if not f:
                                for ob in obj_list:
                                    x = ob.get_selected_arc_destination(mouse_x, mouse_y)
                                    if x != None:
                                        editing = True
                                        editing_information = (ob, x)
                                        current_value = str(ob.get_arc_weight(x))
                                        #print(current_value)
                                        distance_done = False
                                        break

                                
                            

                    if connecting:
                        if dragging_index != None:
                            # gestire la connessione di 2 oggetti
                            # dato che voglio anche considerare l'eventualità in cui un utente
                            # provi a inserire 2 archi tra gli stessi 2 oggetti
                            # uso sempre la funzione "edit_arc", che sovrascrive un'altro
                            # o ne crea uno nuovo, se non ne trova uno corrispondente
                            obj_list[starting_index].edit_arc(obj_list[dragging_index],1, True)
                            #obj_list[dragging_index].edit_arc(obj_list[starting_index],1, False)
                            distance_done = False
                        connecting = False


                elif event.button == 2:
                    # middle click
                    mouse_x, mouse_y = event.pos
                    ob_todel = None
                    for ob in obj_list:
                        if ob.is_inside(mouse_x, mouse_y):
                            ob_todel = ob
                            break

                    if ob_todel != None:
                        obj_list.remove(ob_todel)
                        distance_done = False
                    else:
                        for ob in obj_list:
                            x = ob.get_selected_arc_destination(mouse_x, mouse_y)
                            if x != None:
                                ob.remove_arc(x, True)
                                distance_done = False
                                break
                    
                elif event.button == 3:
                    # right click
                    distance_done = False
                    #drawing = True
                    mouse_x, mouse_y = event.pos
                    #starting_x = mouse_x
                    #starting_y = mouse_y
                    #drawing_w = 1
                    #drawing_h = 1
                    x = Node(mouse_x, mouse_y, CIRCLE_RADIUS)
                    obj_list.append(x)

                    
                # 5 -> scroll up
                # 6 -> scroll down
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    
                    if dragging and not moved:
                        connecting = True

                    dragging = False
               
                
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_x, mouse_y = event.pos
                    drawing_w = mouse_x - starting_x
                    drawing_h = mouse_y - starting_y 
                if dragging:
                    moved = True
                    mouse_x, mouse_y = event.pos
                    vec_x = mouse_x - starting_x
                    vec_y = mouse_y - starting_y
                    obj_list[dragging_index].translate(vec_x, vec_y)
                    starting_x = mouse_x
                    starting_y = mouse_y
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    editing = False
                if event.key == pygame.K_RETURN:
                    editing = False
                if event.key == K_BACKSPACE:
                    current_value = current_value[0:-1]
                if event.key == pygame.K_0:
                    current_value = current_value + "0"
                if event.key == pygame.K_1:
                    current_value = current_value + "1"
                if event.key == pygame.K_2:
                    current_value = current_value + "2"
                if event.key == pygame.K_3:
                    current_value = current_value + "3"
                if event.key == pygame.K_4:
                    current_value = current_value + "4"
                if event.key == pygame.K_5:
                    current_value = current_value + "5"
                if event.key == pygame.K_6:
                    current_value = current_value + "6"
                if event.key == pygame.K_7:
                    current_value = current_value + "7"
                if event.key == pygame.K_8:
                    current_value = current_value + "8"
                if event.key == pygame.K_9:
                    current_value = current_value + "9"

        
        if current_value == "":
            current_value = "0"
        editing_information[0].edit_arc(editing_information[1], max(1, int(current_value)), True)


    

    # sistema di rendering non efficente:
    #   1. viene iterata 2 volte la lista degli oggetti
    for ob in obj_list:
        ob.render_arcs(screen, pygame.mouse.get_pos())
        if distance_done:
            if obj_list.index(ob) == distance_results.index(0):
                ob.select(True)
            else:
                ob.select(False)
        else:
            ob.select(False)
    
    for ob in obj_list:
        ob.render(screen)
        if distance_done:
            ob.render_text(screen, distance_results[obj_list.index(ob)])

    # BUTTON RENDER
    distance_button.render(screen, pygame.mouse.get_pos(), distance)
    shortest_path_button.render(screen, pygame.mouse.get_pos(), shortest_path_start^shortest_path_end)

    if connecting:
        pygame.draw.line(screen, white, (starting_x, starting_y), pygame.mouse.get_pos())


    # POPUP UPDATE
    distance_popup.update()
    shortest_path_start_popup.update()
    shortest_path_end_popup.update()

    # POPUP RENDER
    distance_popup.render(screen)
    shortest_path_start_popup.render(screen)
    shortest_path_end_popup.render(screen)

    pygame.display.update()
    
    clock.tick(60)
 