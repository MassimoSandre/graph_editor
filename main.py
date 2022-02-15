import pygame
import random 
from pygame.locals import *
from node import Node
from button import Button


def shortest_path(starting_node, results, graph):

    queue = [(starting_node, 0)]

    while len(queue) > 0:
        current_node, distance = queue.pop(0)
        if results[graph.index(current_node)] > distance:
            results[graph.index(current_node)] = distance
            for n in current_node.arcs:
                if distance + n[1] < results[graph.index(n[0])]:
                    queue.append((n[0], distance + n[1]))
            


    # if results[graph.index(starting_node)] > dist:
    #     results[graph.index(starting_node)] = dist
    #     for n in starting_node.arcs:
    #         shortest_path(n[0], results, graph, dist+1)


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

dfs_button = Button((10,490),150, 35, "Shortest path")
dfs_results = []
dfs_done = False

drawing = False
dragging = False
moved = False
connecting = False
dfs = False
dragging_index = 0

editing = False
editing_information = (0,0)
current_value = ""

while True:
    screen.fill(black)

    if not editing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    # left click
                    mouse_x, mouse_y = event.pos
                    
                    if dfs:
                        for ob in obj_list:
                            if ob.is_inside(mouse_x, mouse_y):
                                dfs_done = True
                                dfs = False
                                dfs_results = [float("inf")]*len(obj_list)
                                ob.select(True)

                                shortest_path(ob, dfs_results, obj_list)
                                
                                break
                    else:
                        if dfs_button.is_inside(event.pos):
                            print("eseguo dfs - selezionare un punto da cui partire")
                            dfs = True
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
                                        dfs_done = False
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
                            dfs_done = False
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
                        dfs_done = False
                    else:
                        for ob in obj_list:
                            x = ob.get_selected_arc_destination(mouse_x, mouse_y)
                            if x != None:
                                ob.remove_arc(x, True)
                                dfs_done = False
                                break
                    
                elif event.button == 3:
                    # right click
                    dfs_done = False
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
                # elif event.button == 3:
                #     drawing = False
                #     if drawing_w < 0:
                #         starting_x = starting_x + drawing_w
                #         drawing_w = -drawing_w

                #     if drawing_h < 0:
                #         starting_y = starting_y + drawing_h
                #         drawing_h = -drawing_h

                #     x = Node(starting_x, starting_y, drawing_w, drawing_h)
                #     obj_list.append(x)
                
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
        if dfs_done:
            if obj_list.index(ob) == dfs_results.index(0):
                ob.select(True)
            else:
                ob.select(False)
        else:
            ob.select(False)
    
    for ob in obj_list:
        ob.render(screen)
        if dfs_done:
            ob.render_text(screen, dfs_results[obj_list.index(ob)])

    
    dfs_button.render(screen, pygame.mouse.get_pos(), dfs)

    if connecting:
        pygame.draw.line(screen, white, (starting_x, starting_y), pygame.mouse.get_pos())


    pygame.display.update()
    
    clock.tick(60)
 