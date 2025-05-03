from settings import *

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.status = random.randint(0,1)
        self.alive_col = 'bisque'
        self.dead_col = 'maroon'
        self.color = self.alive_col if self.status else self.dead_col
        self.image = pygame.Surface((node_size,)*2, pygame.SRCALPHA)
        self.rect = self.image.get_frect(topleft=pos)
        self.previous_mouse_state = False
        self.draw_node()

    def draw_node(self):
        pygame.draw.rect(self.image, self.color, self.image.get_frect().scale_by(node_scale_factor, node_scale_factor), 0, 4)        
        pygame.draw.rect(self.image, 'black', self.image.get_frect().scale_by(node_scale_factor, node_scale_factor), 2, 4)

    def update(self, *args, **kwargs):
        current_mouse_state = pygame.mouse.get_pressed()[0]
        if current_mouse_state and not self.previous_mouse_state and self.rect.collidepoint(pygame.mouse.get_pos()): self.status = 0 if self.status else 1
        self.color = self.alive_col if self.status else self.dead_col
        self.draw_node()
        self.previous_mouse_state = current_mouse_state

class Board:
    def __init__(self, *groups):
        self.nodes = [[Node((i * node_size, j * node_size), *groups) for j in range(node_nums)] for i in range(node_nums)]
        self.groups = groups
        self.limitless = False

    def count(self, i: int, j: int) -> int:
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),  # Top row
            ( 0, -1),          ( 0, 1),    # Left and Right
            ( 1, -1), ( 1, 0), ( 1, 1)      # Bottom row
        ]
        total = 0
        for dx, dy in neighbors:
            ni, nj = i + dx, j + dy
            if 0 <= ni < node_nums and 0 <= nj < node_nums: total += self.nodes[ni][nj].status
        return total

    def self_run(self):
        new_statuses = [[node.status for node in row] for row in self.nodes]  # Copy status into a list
        for i in range(node_nums):
            for j in range(node_nums):
                c = self.count(i, j)  # Get the count of neighbors
                if c < 2 or c > 3:
                    new_statuses[i][j] = 0  # Cell dies
                elif c == 3:
                    new_statuses[i][j] = 1  # Cell comes to life
                elif c == 2:
                    new_statuses[i][j] = self.nodes[i][j].status  # Cell stays the same

        for i in range(node_nums):
            for j in range(node_nums):
                self.nodes[i][j].status = new_statuses[i][j]

    def set_empty(self):
        """Set the entire grid to dead state."""
        for row in self.nodes:
            for node in row:
                node.status = 0

    def set_new(self):
        """Randomize the grid."""
        for row in self.nodes:
            for node in row:
                node.status = random.randint(0, 1)

    def update(self):
        """Handles updates based on keyboard inputs."""
        keys = pygame.key.get_just_pressed()

        # Toggle limitless mode with Enter key
        if keys[pygame.K_RETURN]:
            self.limitless = not self.limitless
        
        if self.limitless:  # Run automatically in limitless mode
            self.self_run()
        elif keys[pygame.K_RSHIFT]:  # Run by pressing RSHIFT
            self.self_run()

        # Clear or randomize the grid using keyboard shortcuts
        if keys[pygame.K_RALT]:
            self.set_empty()
        elif keys[pygame.K_RCTRL]:
            self.set_new()
