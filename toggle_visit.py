from qgis.PyQt.QtCore import Qt

layer = iface.activeLayer()  # your stations layer

# Make sure the layer is editable
if not layer.isEditable():
    layer.startEditing()

# Function to toggle visited
def toggle_station(feature_id):
    feat = layer.getFeature(feature_id)
    feat["visited"] = 1 if feat["visited"] == 0 else 0
    layer.updateFeature(feat)
    iface.mapCanvas().refresh()

# Map tool to detect clicks
from qgis.gui import QgsMapToolIdentifyFeature

class ToggleVisitedTool(QgsMapToolIdentifyFeature):
    def __init__(self, canvas, layer):
        super().__init__(canvas, layer)
        self.canvas = canvas
        self.layer = layer

    def canvasReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            results = self.identify(event.x(), event.y())
            if results:
                feature = results[0].mFeature
                toggle_station(feature.id())

# Activate the tool
tool = ToggleVisitedTool(iface.mapCanvas(), layer)
iface.mapCanvas().setMapTool(tool)
print("Click on stations to toggle visited!")
