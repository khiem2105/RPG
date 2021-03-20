"""This file purpose is to find the shortest path from two point with obstacle on the way"""
from queue import PriorityQueue
from math import sqrt
import settings


class Node:
    """Primary element of the game, the map is several node with different specificity"""

    def __init__(self, game, row, col):
        self.game = game
        self.row = row
        self.col = col
        self.x = col * settings.TILESIZE
        self.y = row * settings.TILESIZE
        self.width = settings.TILESIZE
        self.neighbors = []
        self.reachable = []
        self.is_barrier = False
        self.score = 0

    def get_pos(self):
        """return the center of the node"""
        return self.x + settings.TILESIZE / 2, self.y + settings.TILESIZE / 2

    def make_barrier(self):
        "Wall"
        self.is_barrier = True

    def unmake_barrier(self):
        "Zombie"
        self.is_barrier = False

    def find_neighbors(self):
        """find all the neighbors that can be reach"""
        grid = self.game.grid
        left = [
            grid[self.game.current_level][j][i]
            for j in range(self.row - 1, self.row + 2)
            for i in range(self.col - 1, self.col + 2)
            if (i == self.col and j != self.row) or (i != self.col and j == self.row)
        ]
        for node in left:
            if not node.is_barrier:
                self.neighbors.append(node)
        if (
            not grid[self.game.current_level][self.row - 1][self.col - 1].is_barrier
            and not grid[self.game.current_level][self.row - 1][self.col].is_barrier
            and not grid[self.game.current_level][self.row][self.col - 1].is_barrier
        ):
            self.neighbors.append(
                grid[self.game.current_level][self.row - 1][self.col - 1]
            )
        if (
            not grid[self.game.current_level][self.row - 1][self.col + 1].is_barrier
            and not grid[self.game.current_level][self.row - 1][self.col].is_barrier
            and not grid[self.game.current_level][self.row][self.col + 1].is_barrier
        ):
            self.neighbors.append(
                grid[self.game.current_level][self.row - 1][self.col + 1]
            )
        if (
            not grid[self.game.current_level][self.row + 1][self.col - 1].is_barrier
            and not grid[self.game.current_level][self.row + 1][self.col].is_barrier
            and not grid[self.game.current_level][self.row][self.col - 1].is_barrier
        ):
            self.neighbors.append(
                grid[self.game.current_level][self.row + 1][self.col - 1]
            )
        if (
            not grid[self.game.current_level][self.row + 1][self.col + 1].is_barrier
            and (not grid[self.game.current_level][self.row + 1][self.col].is_barrier)
            and (not grid[self.game.current_level][self.row][self.col + 1].is_barrier)
        ):
            self.neighbors.append(
                grid[self.game.current_level][self.row + 1][self.col + 1]
            )


def movement_point(self, player, start, move_point):
    """Recursive function it checks all the neighbors from the start
    and if the path to them is below the amount of movement point that the player has"""
    if move_point > settings.TILESIZE:
        for node in start.neighbors:
            if node not in player.reachables[self.current_level]:
                astar(
                    self,
                    player,
                    player.get_current_position(player.game.current_level),
                    node,
                )
                player.path = []
                if node.score < move_point:
                    player.reachables[self.player.game.current_level].append(node)
                else:
                    return
                movement_point(self, player, node, move_point)


def astar(game, character, start, end):
    """algorithm that find the shortest path between two point"""
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = dict.copy(game.g_score[game.current_level])
    g_score[start] = 0
    f_score = dict.copy(game.f_score[game.current_level])
    f_score[start] = hyp(start.get_pos(), end.get_pos()) + g_score[start]
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            current.score = g_score[current]
            character.path.append(end)
            reconstruct_path(character, came_from, end)
            return current.score
        for neighbor in current.neighbors:
            if not neighbor.is_barrier:
                temp_g_score = g_score[current] + hyp(
                    current.get_pos(), neighbor.get_pos()
                )

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = g_score[neighbor] + hyp(
                        neighbor.get_pos(), end.get_pos()
                    )

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

    return False


def reconstruct_path(entity, came_from, current):
    """To be define"""
    while current in came_from:
        if current.is_barrier:
            continue
        current = came_from[current]
        entity.path.append(current)
    entity.path.reverse()
    entity.path.pop(0)


def hyp(p1, p2):
    """calculate the distance between two points"""
    px1, py1 = p1
    px2, py2 = p2
    return sqrt((px1 - px2) ** 2 + (py1 - py2) ** 2)
