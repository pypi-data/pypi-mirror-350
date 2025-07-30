from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QMessageBox


class LandmarkPlugin:
    def __init__(self, viewer):
        self.viewer = viewer
        self.active = False

    def activate(self):
        self.active = True
        # Disattiva lo zoom
        self.viewer.disattiva_zoom()
        self.viewer.image.setCursor(Qt.CrossCursor)
        self.viewer.image.setFocus()

        self.viewer.mode_label.setText("ADD LANDMARKS MODE")

        QMessageBox.information(
            self.viewer,
            "Inserimento Landmark",
            "Seleziona un nome dalla lista e clicca sull'immagine per posizionare il landmark.",
        )

    def deactivate(self):
        self.active = False
        self.viewer.image.setCursor(Qt.CrossCursor)
        self.viewer.mode_label.setText("")

    def handle_click(self, name, pos):
        self.viewer.image.setCursor(Qt.CrossCursor)
        # Salva la tupla (x, y) nel dizionario
        self.viewer.landmarks[name]["coordinates"] = (pos.x(), pos.y())
        # print("----", self.viewer.landmarks)
        # Costruisci lista delle coordinate esistenti
        coordinate_punti = [
            v["coordinates"]
            for v in self.viewer.landmarks.values()
            if v["coordinates"] is not None
        ]
        # print("CCOORDINATES", coordinate_punti)
        # Disegna i punti sul layer
        if "landmarks" not in self.viewer.layer_manager.layers:
            self.viewer.layer_manager.create_layer("landmarks")

        self.viewer.layer_manager.clear_layer("landmarks")
        lista_qpointf = []
        for i in range(len(coordinate_punti)):
            if coordinate_punti[i]:
                lista_qpointf.append(
                    QPointF(coordinate_punti[i][0], coordinate_punti[i][1])
                )
        self.viewer.layer_manager.draw_points(
            "landmarks", lista_qpointf, color=QColor(255, 0, 0, 180)
        )

        # Avanza nel combo box
        current_index = self.viewer.landmark_combo.currentIndex()
        if current_index < self.viewer.landmark_combo.count() - 1:
            self.viewer.landmark_combo.setCurrentIndex(current_index + 1)

            if current_index < self.viewer.landmark_combo.count() - 1:
                self.viewer.landmark_combo.setCurrentIndex(current_index + 1)
