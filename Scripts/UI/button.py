import pygame

class Button:
    def __init__(self, text, x, y, width, height, func) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
    
    def draw(self, screen) -> None:
        #pygame.draw.rect(screen, (211, 211, 211), (self.x, self.y, self.width, self. height))
        self.draw_text(screen, self.text, self.height, (0, 0, 0))


    def draw_text(self, screen, text, size, color):
        font = pygame.font.Font("Fonts/alagard.ttf", int(size))
        img = font.render(text, False, color)
        btn_center = (self.x + self.width / 2, self.y + self.height / 2)
        pos = tuple(map(lambda x, y: x - y, btn_center, img.get_rect().center))
        screen.blit(img, pos)


    def click(self):
        self.func()