from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QPoint
import time
from math import floor, sqrt
from igraph import Graph, plot

import BaseRobot


class Signals(QObject):
    finished = pyqtSignal(int)

    informAboutNextPoint = pyqtSignal(QPoint)
    informToClearQueue = pyqtSignal()


class BrainLVL1(QRunnable):

    def __init__(self, n, arena):
        QRunnable.__init__(self)
        self.n = n

        self.signals = Signals()

        self.arena = arena
        self.arena_graph = Graph()

        self.human_player = BaseRobot.BaseRobot(0, 0, 0, 0, 0)
        self.robo_player = BaseRobot.BaseRobot(0, 0, 0, 0, 0)

        self.stop = False
        self.informedEnaugh = False

    def inform_brain(self, human_player, robo_player):
        self.informedEnaugh = True
        self.human_player = human_player
        self.robo_player = robo_player

    def createGraph(self):
        print(f"[{self.n}] Starte GraphGenerator")
        self.arena_graph.add_vertices(self.arena.tile_count_x *
                                      self.arena.tile_count_y)

        for x in range(self.arena.tile_count_x):
            for y in range(self.arena.tile_count_y):
                tileIndexInGraph = self.getTileIndexInGraph(x, y)

                if self.arena.matrix[x][y].collision:
                    continue

                added_ngbr_offsets = []
                direct_ngbr_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                # direct_ngbr_offsets = [(0, 1), (1, 0)]
                diagonal_ngbr_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

                # Adding direct neighbours to graph (up, left, right, down)
                for offset_x, offset_y in direct_ngbr_offsets:
                    ngbr_x = x + offset_x
                    ngbr_y = y + offset_y
                    if self.isLegalTileInArena(ngbr_x, ngbr_y):
                        ngbrTile = self.arena.matrix[ngbr_x][ngbr_y]
                        ngbrTileIndexInGraph = self.getTileIndexInGraph(ngbr_x,
                                                                        ngbr_y)
                        if not ngbrTile.collision:
                            if self.arena_graph.are_connected(tileIndexInGraph,
                                                              ngbrTileIndexInGraph):
                                added_ngbr_offsets.append((offset_x, offset_y))
                            else:
                                self.arena_graph.add_edge(tileIndexInGraph,
                                                          ngbrTileIndexInGraph,
                                                          weight=1
                                                          )
                                added_ngbr_offsets.append((offset_x, offset_y))

                # Adding diagonal neighbours to graph
                for offset_x, offset_y in diagonal_ngbr_offsets:
                    ngbr_x = x + offset_x
                    ngbr_y = y + offset_y
                    if self.isLegalTileInArena(ngbr_x, ngbr_y):
                        ngbrTile = self.arena.matrix[ngbr_x][ngbr_y]
                        ngbrTileIndexInGraph = self.getTileIndexInGraph(ngbr_x,
                                                                        ngbr_y)
                        if not ngbrTile.collision:
                            if self.arena_graph.are_connected(tileIndexInGraph,
                                                              ngbrTileIndexInGraph):
                                continue
                            else:
                                if self.diagonalNgbrCanBeAdded((offset_x,
                                                                offset_y),
                                                               added_ngbr_offsets):
                                    self.arena_graph.add_edge(tileIndexInGraph,
                                                              ngbrTileIndexInGraph,
                                                              weight=sqrt(2))

        print(f"[{self.n}] Stop GraphGenerator")

    def isLegalTileInArena(self, x, y):
        return (0 <= x < self.arena.tile_count_x) and \
               (0 <= y < self.arena.tile_count_y)

    def diagonalNgbrCanBeAdded(self, offset, added_offsets):
        upper_right_ok = (1, 0) in added_offsets and (0, -1) in added_offsets
        upper_left_ok = (-1, 0) in added_offsets and (0, -1) in added_offsets
        lower_right_ok = (1, 0) in added_offsets and (0, 1) in added_offsets
        lower_left_ok = (-1, 0) in added_offsets and (0, 1) in added_offsets

        if offset == (1, 1) and lower_right_ok:
            return True
        if offset == (-1, 1) and lower_left_ok:
            return True
        if offset == (-1, -1) and upper_left_ok:
            return True
        if offset == (1, -1) and upper_right_ok:
            return True
        return False

    def plotGraph(self):
        print(f"[{self.n}] Starte Plot")

        layout = []
        for i in range(self.arena_graph.vcount()):
            layout.append(self.getTilePositionInArena(i))

        plot(self.arena_graph,
             layout=layout,
             vertex_size=1,
             vertex_color=['blue'],
             edge_color=['red'])

        print(f"[{self.n}] Stop Plot")

    def getTileIndexInGraph(self, x, y):
        return int(x) * self.arena.tile_count_y + int(y)

    def getTilePositionInArena(self, index):
        x = int(index / self.arena.tile_count_x) * self.arena.tile_width \
            + int(0.5 * self.arena.tile_width)  # center
        y = index % self.arena.tile_count_x * self.arena.tile_width \
            + int(0.5 * self.arena.tile_height)  # center
        return (x, y)

    def run(self):
        if self.arena_graph.vcount() == 0:
            self.createGraph()
            # self.plotGraph()

        if self.stop:
            return
        else:
            if self.informedEnaugh:
                FROMIndexInGraph = self.getTileIndexInGraph(
                                                floor(self.robo_player.x /
                                                      self.arena.tile_width),
                                                floor(self.robo_player.y /
                                                      self.arena.tile_width))

                TOIndexInGraph = self.getTileIndexInGraph(
                                                floor(self.human_player.x /
                                                      self.arena.tile_width),
                                                floor(self.human_player.y /
                                                      self.arena.tile_height))

                path = self.arena_graph.get_shortest_paths(FROMIndexInGraph,
                                                           TOIndexInGraph,
                                                           output="vpath")

                self.signals.informToClearQueue.emit()

                for p in path[0]:
                    x, y = self.getTilePositionInArena(p)
                    if not self.stop:
                        self.signals.informAboutNextPoint.emit(QPoint(int(x),
                                                                      int(y)))

                time.sleep(3)
                
                if not self.stop:
                    self.signals.finished.emit(self.n)
            else:
                if not self.stop:
                    self.signals.finished.emit(self.n)
