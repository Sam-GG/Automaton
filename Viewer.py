import pygame

class Viewer:
    def __init__(self, update_func, display_size):
        self.update_func = update_func
        self.display_size = display_size
        pygame.init()
        self.display = pygame.display.set_mode(display_size, 0, 32)
        
    
    def set_title(self, title):
        pygame.display.set_caption(title)
    
    def start(self):
        self.set_title('Automaton')

        pygame.font.init()
        myfont = pygame.font.SysFont('Helvitica', 27)
        
        running = True
        while running:
            for event in pygame.event.get():
               
                if event.type == pygame.QUIT:
                    running = False

            # Call update function, fetch new image state and step count
            Z, steps, = self.update_func()   

            #Renders "steps" text
            textsurface = myfont.render(('Steps: '+ str(steps)), False, (255, 255, 00))
            textshadow = myfont.render(('Steps: '+ str(steps)), False, (0, 0, 0))
            
            #Display text and array
            surf = pygame.surfarray.make_surface(Z)
            surf = pygame.transform.scale(surf, (self.display_size))
            self.display.blit(surf, (0, 0))
            self.display.blit(textshadow,(3,0))
            self.display.blit(textsurface,(0,0))
           
            pygame.display.update()

        pygame.quit()