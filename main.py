from classses import *


# press enter to toggle run
# press shift(right) to go to next iteration manually


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES, pygame.SRCALPHA)
        self.clock = pygame.Clock()
        
        self.group = pygame.sprite.Group()

        self.board = Board(self.group)
        
    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    
            self.screen.fill('bisque')
            
            self.board.update()
            self.group.update(self.dt)
            self.group.draw(self.screen)
            
            # pygame.display.set_caption(f'FPS: {self.clock.get_fps()}')
            # pygame.display.set_caption(f'FPS: {FPS}')
            pygame.display.set_caption(f'mode: {"limitless" if self.board.limitless else "manual"} FPS: {self.clock.get_fps()}')
            
            pygame.display.flip()
            
            
Game().run()
            