from game_utils.images import *
from pygame import Rect, Surface

SPRITESHEET_SIM_RECT = Rect(0, 0, 100, 100)
SPRITESHEET_SIM__SURFACT = Surface(SPRITESHEET_SIM_RECT.size)


def test_sprite_sheet():
    ssheet = SpriteSheet(spritesheet=SPRITESHEET_SIM__SURFACT)

    seg = ssheet.get_spritesheet_segment(Rect(0, 0, 20, 20))
    assert seg.get_rect().size == (20, 20)


def test_sprite_sheet_list():
    ssheet_list = SpriteSheetList(
        spritesheet=SPRITESHEET_SIM__SURFACT,
        n_sprites=5,
    )

    seg = ssheet_list[0]
    assert seg.get_rect().size == (100, 20)


def test_sprite_sheet_map():
    ssheet_map = SpriteSheetMap(
        spritesheet=SPRITESHEET_SIM__SURFACT,
        keys=["a", "b", "c", "d", "e"],
        n_sprites=5,
    )

    seg = ssheet_map["a"]
    assert seg is not None
    assert seg.get_rect().size == (100, 20)
