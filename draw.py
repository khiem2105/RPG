"""This file draw the player and the different sprites that compose the game.
The camera is taken into consideration which implies that the sprites are draw relatively to it."""
from math import sqrt
from operator import sub
import pygame as pg
from sprites import AOE_zone, Path
from pathfinding import movement_point
import settings


def draw(self):
    """main draw function, it prints only the sprites that can be seen by the player."""
    pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
    # this function is called first to update all the sprites before print them
    draw_reachable(self)
    if self.mmap:
        self.screen.fill(settings.BLACK)
        for sprite in self.mmap_group[self.m_current_level]:
            self.screen.blit(sprite.image, sprite.rect)

    elif self.pause:
        for key in self.buttons:
            pg.draw.rect(
                self.screen,
                (90, 0, 0),
                (
                    self.buttons[key].rect.x,
                    self.buttons[key].rect.y - 5,
                    *self.buttons[key].rect.size,
                ),
            )
            self.screen.blit(
                self.buttons[key].name_surface,
                (self.buttons[key].text_rect.x, self.buttons[key].rect.y),
            )
            if self.buttons[key].iscolliding:
                x_delta, y_delta = self.buttons[key].rect.size
                pg.draw.rect(
                    self.screen,
                    (215, 154, 16),
                    (
                        self.buttons[key].rect.x,
                        self.buttons[key].rect.y - 5,
                        x_delta - 1,
                        y_delta - 1,
                    ),
                    2,
                )

    elif self.shortcut:
        self.screen.fill((10, 10, 10))
        for i, key in enumerate(self.buttons):
            pg.draw.rect(
                self.screen,
                (90, 0, 0),
                (
                    (((i + 1) * settings.SPACING) // settings.HEIGHT)
                    * (settings.WIDTH // 3)
                    + 50,
                    ((i) % (settings.HEIGHT // settings.SPACING) * settings.SPACING)
                    + 50,
                    150 - 20,
                    30,
                ),
            )
            self.screen.blit(
                self.buttons[key].name_surface,
                (self.buttons[key].text_rect.x, self.buttons[key].rect.y + 5),
            )
        for key in self.inputs:
            self.inputs[key].draw(self.screen, (200, 200, 200), True)

    else:
        self.screen.blit(self.background, self.camera.camera.topleft)
        for sprite in self.sprites[self.current_level]["D"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprites[self.current_level]["R"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprites[self.current_level]["J"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.sprites[self.current_level]["M"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprites[self.current_level]["C"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprites[self.current_level]["Pa"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.sprites[self.current_level]["ZG"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.sprites[self.current_level]["AOE"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.player.stealth:
            blit_alpha(
                self.screen, self.player.image, self.camera.apply(self.player), 40
            )
        else:
            self.screen.blit(self.player.image, self.camera.apply(self.player))
        for sprite in self.sprites[self.current_level]["E"]:
            if sprite.isseen:
                if (
                    -self.camera.x - settings.WIDTH * 0.4
                    <= sprite.rect.x
                    <= -self.camera.x + settings.WIDTH * 1.4
                    and -self.camera.y - settings.HEIGHT * 0.4
                    <= sprite.rect.y
                    <= -self.camera.y + settings.HEIGHT * 1.4
                ):
                    if sprite.health < sprite.max_health:
                        sprite.draw_health(self.screen)
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                    tmp = sprite.name.get_rect()
                    for x_delta in range(-1, 2):
                        for y_delta in range(-1, 2):
                            self.screen.blit(
                                sprite.outline,
                                (
                                    self.camera.apply(sprite).x
                                    - tmp.width // 5
                                    + x_delta,
                                    self.camera.apply(sprite).y
                                    - settings.TILESIZE // 3
                                    + y_delta,
                                ),
                            )
                    self.screen.blit(
                        sprite.name,
                        (
                            self.camera.apply(sprite).x - tmp.width // 5,
                            self.camera.apply(sprite).y - settings.TILESIZE // 3,
                        ),
                    )
        for sprite in self.sprites[self.current_level]["S"]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.f_background, self.camera.camera.topleft)
        self.player.draw_player_turn(self.screen)
        self.player.draw_player_level(self.screen)
        for sprite in self.sprites[self.current_level]["E"]:
            if sprite.isseen:
                if (
                    -self.camera.x - settings.WIDTH * 0.4
                    <= sprite.rect.x
                    <= -self.camera.x + settings.WIDTH * 1.4
                    and -self.camera.y - settings.HEIGHT * 0.4
                    <= sprite.rect.y
                    <= -self.camera.y + settings.HEIGHT * 1.4
                ):
                    if sprite.looting:
                        self.screen.blit(sprite.looting, sprite.looting_pos)
        for sprite in self.sprites[self.current_level]["J"]:
            if sprite.talking:
                self.screen.blit(sprite.talking, sprite.talking_pos)
        for sprite in self.sprites[self.current_level]["M"]:
            if sprite.talking:
                self.screen.blit(sprite.talking, sprite.talking_pos)
        for sprite in self.sprites[self.current_level]["V"]:
            if (
                -self.camera.x - settings.WIDTH * 0.4
                <= sprite.rect.x
                <= -self.camera.x + settings.WIDTH * 1.4
                and -self.camera.y - settings.HEIGHT * 0.4
                <= sprite.rect.y
                <= -self.camera.y + settings.HEIGHT * 1.4
            ):

                self.screen.blit(sprite.image, self.camera.apply(sprite))
        for enemy in self.enemy[self.current_level]:
            if enemy.health < enemy.max_health:
                enemy.draw_health(self.screen)
        for sprite in self.sprites[self.current_level]["C"]:
            if sprite.screen_surface:
                self.screen.blit(sprite.screen_surface, sprite.screen_pos)
        for key in self.log:
            if self.log[key]:
                self.log[key].print_log(self.screen)
        self.screen.blit(
            self.player.spell_surface,
            (
                settings.WIDTH // 2 - self.player.spell_surface.get_width() // 2,
                settings.HEIGHT - self.player.spell_surface.get_height(),
            ),
        )

        self.player.draw_player_health(
            self.screen,
            settings.WIDTH // 2 - self.player.spell_surface.get_width() // 2 - 22,
            settings.HEIGHT - self.player.spell_surface.get_height(),
            self.player.health / (self.player.dic_player["Con"] * 10),
        )
        self.player.draw_player_mana(
            self.screen,
            settings.WIDTH // 2 + self.player.spell_surface.get_width() // 2,
            settings.HEIGHT - self.player.spell_surface.get_height(),
            self.player.mana / (self.player.dic_player["Int"] * 10),
        )

        self.player.draw_xp_bar(
            self.screen,
            settings.WIDTH // 2 - self.player.spell_surface.get_width() // 2,
            settings.HEIGHT - self.player.spell_surface.get_height() - 6,
            self.player.dic_player["xp"]
            / (100 * pow(2, self.player.dic_player["level"] - 1)),
        )

        if self.player.player_sheet.surf:
            self.screen.blit(
                self.player.player_sheet.surf,
                (
                    settings.WIDTH // 2
                    - self.player.player_sheet.surf.get_rect().width // 2,
                    settings.HEIGHT // 2
                    - self.player.player_sheet.surf.get_rect().height // 2,
                ),
            )

        if self.is_console_opened:
            self.my_input.draw(self.screen, color=(255, 255, 255))

    pg.display.flip()


def draw_path(self):
    """draw the path that will follow the player"""
    flush_path(self)  # if there were a precedent path destroy it
    for tile in self.sprites[self.current_level]["R"].sprites():
        for nodes in self.player.path:
            if nodes.row == tile.y and nodes.col == tile.x:
                self.sprites[self.current_level]["Pa"].add(Path(self, tile.x, tile.y))
    for tile in self.sprites[self.current_level]["G"].sprites():
        for nodes in self.player.path:
            if nodes.row == tile.y and nodes.col == tile.x:
                self.sprites[self.current_level]["Pa"].add(Path(self, tile.x, tile.y))


def flush_path(self):
    """reset the display of the path"""
    for tile in self.sprites[self.current_level]["Pa"].sprites():
        self.sprites[self.current_level]["A"].remove(tile)
        self.sprites[self.current_level]["Pa"].remove(tile)


def blit_alpha(target, source, location, opacity):
    """allow to print transparent png"""
    temp = pg.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-location[0], -location[1]))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def draw_reachable(self):
    """update the sprites that the player can see : If he can reach them alpha = 0,
    if he already saw them before alpha = 200 (the player remembers the path followed),
    else alpha = 255 (The player has no idea what is at this location)"""
    if self.player.reach_draw:
        self.camera.update(self.focus)
        flush_reachable(self)
        player_pos = self.player.pos
        movement_point(
            self,
            self.player,
            self.player.get_current_position(self.current_level),
            self.player.pm,
        )
        for tile in self.sprites[self.current_level]["F"].sprites():
            for nodes in self.player.reachables[self.current_level]:
                try:
                    if nodes.row == tile.y and nodes.col == tile.x:
                        self.sprites[self.current_level]["R"].add(tile)
                        tile.alpha = 0
                        tile.image.set_alpha(tile.alpha)
                        tile.m_image.set_alpha(tile.alpha)
                except AttributeError:
                    pass

            if (
                sqrt(
                    (tile.rect.x + settings.TILESIZE / 2 - player_pos.x) ** 2
                    + (tile.rect.y + settings.TILESIZE / 2 - player_pos.y) ** 2
                )
                < settings.PM - 20
                and not self.sprites[self.current_level]["R"].has(tile)
                and not self.player.stealth
            ) or (
                sqrt(
                    (tile.rect.x + settings.TILESIZE / 2 - player_pos.x) ** 2
                    + (tile.rect.y + settings.TILESIZE / 2 - player_pos.y) ** 2
                )
                < settings.PM * (3 / 4) - 20
                and not self.sprites[self.current_level]["R"].has(tile)
                and self.player.stealth
            ):
                if tile.image.get_alpha() > 0:
                    tile.alpha = 200
                    tile.image.set_alpha(tile.alpha)
                    tile.m_image.set_alpha(tile.alpha)

        self.player.reach_draw = False
        if not self.player.reachables[self.current_level]:
            self.player.reachables[self.current_level].append("None")
        update_draw(self)


def flush_reachable(self):
    """the sprites that were reachable are kept in memory"""
    for tile in self.sprites[self.current_level]["R"].sprites():
        self.sprites[self.current_level]["R"].remove(tile)
        tile.alpha = 200
        tile.image.set_alpha(tile.alpha)
        tile.m_image.set_alpha(tile.alpha)


def draw_aoe_area(self):
    """Draw the area of effect when casting an aoe spell"""
    flush_aoe_area(self)
    mouse_position = pg.mouse.get_pos()
    mouse_node = self.player.game.grid[self.current_level][
        int((mouse_position[1] - self.camera.get_pos()[1]) / settings.TILESIZE)
    ][int((mouse_position[0] - self.camera.get_pos()[0]) / settings.TILESIZE)]
    for tile in self.sprites[self.current_level]["F"].sprites():
        tup = map(sub, (tile.rect.x + 16, tile.rect.y + 16), mouse_node.get_pos())
        test = tuple([abs(elt) for elt in tup])
        if (
            self.player.my_spell
            and not self.player.my_spell.type == "bonus"
            and not self.player.my_spell.type == "on_player"
        ):
            if (test[0]) <= max(32, self.player.my_spell.AOE[0]) and (
                (test[1]) <= max(32, self.player.my_spell.AOE[1])
            ):
                self.sprites[self.current_level]["AOE"].add(
                    AOE_zone(self, tile.x, tile.y)
                )
            else:
                if (test[0]) <= 32 and ((test[1]) <= 32):
                    self.sprites[self.current_level]["AOE"].add(
                        AOE_zone(self, tile.x, tile.y)
                    )


def flush_aoe_area(self):
    """flush the aoe and a sprites group"""
    for tile in self.sprites[self.current_level]["AOE"].sprites():
        self.sprites[self.current_level]["A"].remove(tile)
        self.sprites[self.current_level]["AOE"].remove(tile)


def update_draw(self):
    """update sprites dictionnary when it is needed
    and not at each frame"""
    self.sprites[self.current_level]["D"].empty()
    self.sprites[self.current_level]["DF"].empty()
    self.f_background = pg.Surface(
        (100 * settings.TILESIZE, 100 * settings.TILESIZE), pg.SRCALPHA, 32
    )
    if self.first:
        self.first = False

    # for enemy in self.enemy[self.current_level]:
    #     if enemy.health < MOB_HEALTH:
    #         enemy.draw_health()
    for sprite in self.sprites[self.current_level]["G"]:
        if (
            -self.camera.x - settings.WIDTH * 0.4
            <= sprite.rect.x
            <= -self.camera.x + settings.WIDTH * 1.4
            and -self.camera.y - settings.HEIGHT * 0.4
            <= sprite.rect.y
            <= -self.camera.y + settings.HEIGHT * 1.4
        ):
            self.background.blit(sprite.image, sprite.rect.move(0, 0))
    for sprite in self.sprites[self.current_level]["W"]:
        if (
            -self.camera.x - settings.WIDTH * 0.4
            <= sprite.rect.x
            <= -self.camera.x + settings.WIDTH * 1.4
            and -self.camera.y - settings.HEIGHT * 0.4
            <= sprite.rect.y
            <= -self.camera.y + settings.HEIGHT * 1.4
        ):

            self.background.blit(sprite.image, sprite.rect.move(0, 0))
    for sprite in self.sprites[self.current_level]["E"]:

        if (
            -self.camera.x - settings.WIDTH * 0.4
            <= sprite.rect.x
            <= -self.camera.x + settings.WIDTH * 1.4
            and -self.camera.y - settings.HEIGHT * 0.4
            <= sprite.rect.y
            <= -self.camera.y + settings.HEIGHT * 1.4
        ):
            if not sprite.isseen:
                self.background.blit(sprite.image, sprite.rect.move(0, 0))
    for sprite in self.sprites[self.current_level]["F"]:
        if (
            -self.camera.x - settings.WIDTH * 0.4
            <= sprite.rect.x
            <= -self.camera.x + settings.WIDTH * 1.4
            and -self.camera.y - settings.HEIGHT * 0.4
            <= sprite.rect.y
            <= -self.camera.y + settings.HEIGHT * 1.4
        ):

            if sprite.image.get_alpha() < 255:
                self.sprites[self.current_level]["D"].add(sprite)
            else:
                self.f_background.blit(sprite.image, sprite.rect.move(0, 0))
    for sprite in self.sprites[self.current_level]["AOE"]:
        if (
            -self.camera.x - settings.WIDTH * 0.4
            <= sprite.rect.x
            <= -self.camera.x + settings.WIDTH * 1.4
            and -self.camera.y - settings.HEIGHT * 0.4
            <= sprite.rect.y
            <= -self.camera.y + settings.HEIGHT * 1.4
        ):

            self.background.blit(sprite.image, sprite.rect.move(0, 0))
