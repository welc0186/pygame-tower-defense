from os.path import join

import esper
from gamelib.mgmt.scene_base import SceneBase
from gamelib.sprite.spritesheet_grid import SpriteSheetGrid
from gamelib.ecs import (
    RenderSurfaceProcessor,
    RenderSurfaceComponent,
    PositionComponent,
)
from gamelib.tiles.tiles import TileMap
from gamelib.tiles.tmx import TmxImageTileMap
import pygame


SPRITE_SHEET = SpriteSheetGrid(join("assets", "towerDefense_tilesheet.png"), 64, 64)
GRASS_SPRITE = SPRITE_SHEET.get(3, 2)

CSV_MAP = join("assets", "pygame_tower_defense.csv")

RED = 255, 0, 0


def create_backdrop() -> pygame.Surface:
    sprite_tilemap = TmxImageTileMap(
        join("assets", "Tiled", "pygame_tower_defense.tmx")
    )
    return sprite_tilemap.generate_surface()


class MainScene(SceneBase):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        esper.switch_world("default")
        try:
            esper.delete_world("main")
        except KeyError:
            pass
        esper.switch_world("main")
        esper.clear_database()
        esper.add_processor(RenderSurfaceProcessor(screen))
        backdrop_entity = esper.create_entity()
        esper.add_component(backdrop_entity, PositionComponent(0, 0))
        esper.add_component(backdrop_entity, RenderSurfaceComponent(create_backdrop()))

    def update(self, events, pressed_keys, dt: float = 0) -> None:
        esper.process(dt)
