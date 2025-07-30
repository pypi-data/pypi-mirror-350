""" Maximum Projection QGraphicsScene extension """
import pathlib

from PySide6.QtCore import QPoint, Qt, QRect, QRectF
from PySide6.QtGui import QImage, QPixmap, QPolygonF, QPen, QBrush, QFont, QPainter
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from shapely import Polygon


class MaximumProjection(QGraphicsScene):
    def __init__(self, cell_names, cell_contours, max_projection_path):
        super().__init__()

        self.default_font = QFont("Arial", 12, 1)
        self.cells = cell_names
        self.cell_contours = cell_contours
        self.image_path = max_projection_path

        self.new_centroids = None

        self.image = None
        self.pixmap = None
        self.pixmap_item = None

        self.pen = None
        self.brush = None

        self.cell_outline_polygons = []
        self.cell_labels = []

        #  References back to polygons for post-draw color changes
        self.cell_outline_references = []
        self.outline_dict = {}

        self._generate_new_centroids()
        self._load_maxproj_image()
        self._create_outline_polygons()
        self._create_cell_labels()
        self._draw_cell_outlines()
        self._create_reference_dict()

    def change_outline_color(self, key, new_state: int):
        color = None
        polygon = self.outline_dict[key]

        if new_state == 1:  # Selected
            color = Qt.GlobalColor.green
        elif new_state == 0:  # Not Selected
            color = Qt.GlobalColor.red

        self.pen.setColor(color)  # This might just work?
        polygon.setPen(self.pen)
        polygon.update()

    def reset_polygon_colors(self):
        for cell in self.cells:
            self.change_outline_color(cell, 0)

    def save(self):
        self.reset_polygon_colors()
        scene_rect = QRectF(self.sceneRect())
        scene_size = scene_rect.size().toSize()
        image = QImage(scene_size.width(), scene_size.height(), QImage.Format.Format_ARGB32_Premultiplied)
        painter = QPainter(image)

        self.render(painter, image.rect(), scene_rect)
        painter.end()
        save_path = self.image_path.with_stem(f'labeled-HD-maxproj').with_suffix('.tif')
        image.save(str(save_path))

    def _load_maxproj_image(self):
        self.image = QImage(self.image_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.addItem(self.pixmap_item)

    def _create_outline_polygons(self):
        for cell in self.cells:  # Iterate through cells
            polygon_verts = []
            cell_coordinates = self.cell_contours[cell][0]  # Get the vertices for a specific cell

            for pair in cell_coordinates:
                _x, _y = pair
                _point = QPoint(_x, _y) * 4
                polygon_verts.append(_point)  # We need a list of QPoints, so generate a QPoint for each pair

            _cell_polygon = QPolygonF(polygon_verts)
            self.cell_outline_polygons.append(_cell_polygon)

    def _create_reference_dict(self):
        self.outline_dict = dict(list(zip(self.cells, self.cell_outline_references)))

    def _create_cell_labels(self):
        for cell in self.cells:
            centroid = self.new_centroids[cell]
            _x, _y = centroid
            _cell_label = str(int(cell.split('C')[1]))  # Little trickery to drop leading zeros

            _label = QGraphicsTextItem(_cell_label)
            _position = QPoint(_x, _y) * 4
            _label.setPos(_position)

            _label.setFont(self.default_font)
            self.cell_labels.append(_label)

    def _draw_cell_outlines(self):
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.NoBrush)
        self.pen = QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap,
                        Qt.PenJoinStyle.RoundJoin)

        for i, polygon in enumerate(self.cell_outline_polygons):
            _polygon_reference = self.addPolygon(polygon, self.pen, self.brush)
            _label = self.cell_labels[i]
            _label.setParentItem(_polygon_reference)
            self.addItem(_label)
            self.cell_outline_references.append(_polygon_reference)

    def _generate_new_centroids(self):
        centroids = []
        for cell in self.cells:
            polygon_verts = self.cell_contours[cell][0]
            polygon = Polygon(polygon_verts)
            new_centroid = (polygon.centroid.x, polygon.centroid.y)
            centroids.append(new_centroid)

        self.new_centroids = dict(list(zip(self.cells, centroids)))
