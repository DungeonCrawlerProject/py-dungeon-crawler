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
        self.__original_frames = []
        self.__original_image = None  # Store the original image for rotation
        self.__unrotated_image = None
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
    
    def get_original_image(self):
        return self.__original_image

    def get_original_frames(self):
        return self.__original_frames
    
    def scale_frames(self, scalar):

        for i, frame in enumerate(self.frames):
            size = self.get_original_image().get_rect()
            a = pygame.Vector2(size.width, size.height)
            self.frames[i] = pygame.transform.scale(frame, scalar * a)
            self.__unrotated_image[i] = pygame.transform.scale(frame, scalar * a)
    
    def rotate(self, deg: float) -> None:
        # THE ORIGINAL IMAGE NEEDS A REWORK
        safe_ref = self.__unrotated_image[self.current_frame]
        self.image = pygame.transform.rotate(safe_ref, deg)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_all_frames(self, deg: float) -> None:
        for i in range(len(self.__original_frames)):
            self.frames[i] = pygame.transform.rotate(self.__original_frames[i], deg)