from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QPoint
import time
from numpy import sqrt, floor
from igraph import Graph, plot
import BaseRobot


class Signals(QObject):
    finished = pyqtSignal(int)

    informAboutNextPointToMove = pyqtSignal(QPoint)
    informToClearQueueMovement = pyqtSignal()

    informAboutNextPointToShoot = pyqtSignal(QPoint)
    informToClearQueueShooting = pyqtSignal()


class Brain(QRunnable):

    def __init__(self, n, arena, difficulty="Medium"):
        QRunnable.__init__(self)
        self.n = n

        self.signals = Signals()

        self.arena = arena
        self.arena_graph = Graph()
        self.unreachableTiles = []

        self.human_player = BaseRobot.BaseRobot(0, 0, 0, 0, 0, None)
        self.robo_player = BaseRobot.BaseRobot(0, 0, 0, 0, 0, None)

        self.stop = False
        self.informedEnaugh = False

        self.sleepTime = 1

        self.handleDifficulty(difficulty)

    def handleDifficulty(self, difficulty):
        if difficulty == "Hard":
            self.sleepTime = 1
        elif difficulty == "Normal":
            self.sleepTime = 5
        elif difficulty == "Easy":
            self.sleepTime = 7

    def inform_brain(self, human_player, robo_player):
        self.informedEnaugh = True
        self.human_player = human_player
        self.robo_player = robo_player

    def createGraph(self):
        self.arena_graph.add_vertices(self.arena.tile_count_x *
                                      self.arena.tile_count_y)

        self.unreachableTiles = self.calculateUnreachableTiles()

        for x in range(self.arena.tile_count_x):
            for y in range(self.arena.tile_count_y):
                tileIndexInGraph = self.getTileIndexInGraph(x, y)

                if tileIndexInGraph in self.unreachableTiles:
                    continue

                added_ngbr_offsets = []
                direct_ngbr_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                diagonal_ngbr_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

                # Adding direct neighbours to graph (up, left, right, down)
                for offset_x, offset_y in direct_ngbr_offsets:
                    ngbr_x = x + offset_x
                    ngbr_y = y + offset_y
                    if self.isLegalTileInArena(ngbr_x, ngbr_y):
                        ngbrTileIndexInGraph = self.getTileIndexInGraph(ngbr_x,
                                                                        ngbr_y)
                        if ngbrTileIndexInGraph not in self.unreachableTiles:
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
                        ngbrTileIndexInGraph = self.getTileIndexInGraph(ngbr_x,
                                                                        ngbr_y)
                        if ngbrTileIndexInGraph not in self.unreachableTiles:
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

    def calculateUnreachableTiles(self):
        unreachableTiles = []

        # Adding tiles that have collision and are neighbours of ones that do
        for x in range(self.arena.tile_count_x):
            for y in range(self.arena.tile_count_y):
                tileIndexInGraph = self.getTileIndexInGraph(x, y)

                if self.arena.matrix[x][y].collision:
                    unreachableTiles.append(tileIndexInGraph)

                    for offset_x in (-1, 0, 1):
                        for offset_y in (-1, 0, 1):
                            ngbrTileIndex = self.getTileIndexInGraph(x + offset_x,
                                                                     y + offset_y)
                            unreachableTiles.append(ngbrTileIndex)

        # Adding tiles that are near the Map-border
        for x in range(self.arena.tile_count_x):
            unreachableTiles.append(x)  # top
            unreachableTiles.append((self.arena.tile_count_y - 1) *
                                    self.arena.tile_count_x + x)  # bottom
        for y in range(self.arena.tile_count_y):
            unreachableTiles.append(y * self.arena.tile_count_x)  # left
            unreachableTiles.append(y * self.arena.tile_count_x +
                                    self.arena.tile_count_x - 1)  # right

        return unreachableTiles

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
        layout = []
        for i in range(self.arena_graph.vcount()):
            layout.append(self.getTilePositionInArena(i))

        plot(self.arena_graph,
             layout=layout,
             vertex_size=1,
             vertex_color=['blue'],
             edge_color=['red'])

    def getTileIndexInGraph(self, x, y):
        return int(y) * self.arena.tile_count_x + int(x)

    def getTilePositionInArena(self, index):
        x = index % self.arena.tile_count_x * self.arena.tile_width \
            + int(0.5 * self.arena.tile_height)  # center
        y = floor(index / self.arena.tile_count_x) * self.arena.tile_width \
            + int(0.5 * self.arena.tile_width)  # center
        return (x, y)

    def calculateShooting(self):
        if not self.stop:
            self.signals.informToClearQueueShooting.emit()

            self.signals.informAboutNextPointToShoot.emit(
                QPoint(int(self.human_player.rect().center().x()),
                       int(self.human_player.rect().center().y()))
            )

    def calculatePath(self):
        if self.arena_graph.vcount() == 0:
            self.createGraph()
            # self.plotGraph()

        if self.informedEnaugh:
            FROMIndexInGraph = self.getTileIndexInGraph(
                                    floor(
                                        (self.robo_player.x +
                                            0.5 * self.robo_player.r) /
                                        self.arena.tile_width),
                                    floor(
                                        (self.robo_player.y +
                                            0.5 * self.robo_player.r) /
                                        self.arena.tile_width))

            TOIndexInGraph = self.getTileIndexInGraph(
                                    floor(
                                        (self.human_player.x +
                                            0.5 * self.human_player.r) /
                                        self.arena.tile_width),
                                    floor(
                                        (self.human_player.y +
                                            0.5 * self.human_player.r) /
                                        self.arena.tile_height))

            searchIndex = 50

            if TOIndexInGraph in self.unreachableTiles:
                reachableTileFound = False
                for offset_x in range(-searchIndex, searchIndex, 1):
                    for offset_y in range(-searchIndex, searchIndex, 1):
                        newTOIndexInGraph = TOIndexInGraph + offset_x + \
                                            offset_y * self.arena.tile_count_x
                        x, y = self.getTilePositionInArena(newTOIndexInGraph)
                        if (self.isLegalTileInArena(x, y) and
                           newTOIndexInGraph not in self.unreachableTiles):
                            TOIndexInGraph = newTOIndexInGraph
                            reachableTileFound = True
                            break
                    if reachableTileFound:
                        break

            if FROMIndexInGraph in self.unreachableTiles:
                reachableTileFound = False
                for offset_x in range(-searchIndex, searchIndex, 1):
                    for offset_y in range(-searchIndex, searchIndex, 1):
                        newFROMIndexInGraph = FROMIndexInGraph + offset_x + \
                                            offset_y * self.arena.tile_count_x
                        x, y = self.getTilePositionInArena(newFROMIndexInGraph)
                        if (self.isLegalTileInArena(x, y) and
                           newFROMIndexInGraph not in self.unreachableTiles):
                            FROMIndexInGraph = newFROMIndexInGraph
                            reachableTileFound = True
                            break
                    if reachableTileFound:
                        break

            try:
                path = self.arena_graph.get_shortest_paths(FROMIndexInGraph,
                                                           TOIndexInGraph,
                                                           output="vpath")
            except RuntimeWarning:
                pass

            # Informing AI about Point to move to
            if len(path[0]) > 0:
                self.signals.informToClearQueueMovement.emit()

                path[0].pop(0)
                for p in path[0]:
                    x, y = self.getTilePositionInArena(p)
                    if not self.stop:
                        self.signals.informAboutNextPointToMove.emit(
                                                                    QPoint(int(x),
                                                                           int(y)))

    def run(self):
        if self.stop:
            return
        else:
            self.calculatePath()
            self.calculateShooting()

            time.sleep(self.sleepTime)

            if not self.stop:
                self.signals.finished.emit(self.n)
