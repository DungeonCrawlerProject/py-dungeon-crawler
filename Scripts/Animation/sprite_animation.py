import pygame
from Scripts.sprite import PNGSprite

class SpriteAnimation(PNGSprite):
    @classmethod
    def make_from_sprite_sheet(
            cls,
            location: str,
            width: int,
            height: int,
            ms_per_frame,
    ):
        img = pygame.image.load(location).convert_alpha()

        inst = cls(ms_per_frame)
        inst.frames = inst.chop_sprite(img, width, height)
        inst.__original_frames = inst.chop_sprite(img, width, height)
        inst.__original_image = inst.frames[0]
        inst.__unrotated_image = inst.chop_sprite(img, width, height)
        inst.image = inst.__original_image.copy()  # Make a copy of the original image
        inst.rect = inst.image.get_rect()
        return inst
    
    def __init__(self, ms_per_frame) -> None:
        super().__init__()
        self.ms_per_frame = ms_per_frame
        self.start_time = None

    def start_anim(self):
        self.start_time = pygame.time.get_ticks()

    def run_once(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        frame_idx = elapsed_time // self.ms_per_frame
        if frame_idx > 5:
            return 0
        self.image = self.frames[frame_idx]
        return 1
    
