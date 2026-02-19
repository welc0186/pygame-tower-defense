from os.path import join

import esper
from gamelib.mgmt.scene_base import SceneBase
from gamelib.sprite.spritesheet_grid import SpriteSheetGrid
from gamelib.ecs import (
    MoveProcessor,
    RenderSurfaceProcessor,
    RenderSurfaceComponent,
    PositionComponent,
    VelocityComponent,
)
from gamelib.tiles.tmx import TmxImageTileMap
import pygame


SPRITE_SHEET = SpriteSheetGrid(join("assets", "towerDefense_tilesheet.png"), 64, 64)
GRASS_SPRITE = SPRITE_SHEET.get(3, 2)
ENEMY_SPRITE = SPRITE_SHEET.get(15, 10)

CSV_MAP = join("assets", "pygame_tower_defense.csv")

RED = 255, 0, 0


def create_backdrop() -> pygame.Surface:
    sprite_tilemap = TmxImageTileMap(
        join("assets", "Tiled", "pygame_tower_defense.tmx")
    )
    return sprite_tilemap.generate_surface()


def create_enemy() -> int:
    enemy_entity = esper.create_entity()
    esper.add_component(enemy_entity, PositionComponent(-64, 192))
    esper.add_component(enemy_entity, VelocityComponent((1, 0)))
    esper.add_component(enemy_entity, RenderSurfaceComponent(ENEMY_SPRITE))
    return enemy_entity


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
        self.backdrop = create_backdrop()
        esper.add_processor(MoveProcessor(), priority=50)
        esper.add_processor(RenderSurfaceProcessor(screen), priority=10)
        create_enemy()

    def update(self, events, pressed_keys, dt: float = 0) -> None:
        self.screen.blit(self.backdrop, (0, 0))
        esper.process(dt)
