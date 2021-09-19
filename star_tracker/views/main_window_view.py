from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from model.main_model import MainModel
from controllers.main_ctrl import MainController
from views.MainWindow_ui import Ui_MainWindow
from views.frame_view import AutomaticMovements
try:
    from MainWindow_ui import Ui_MainWindow
except ImportError:
    from views.MainWindow_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,  model : MainModel, main_controller : MainController, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._model = model
        self._main_controller = main_controller
        
        #connect to controller
        self._load_stars_file.clicked.connect(self._main_controller.load_stars_dialog)
        self._load_movements_file.clicked.connect(self._main_controller.load_movements_dialog)
        self._load_camera_file.clicked.connect(self._main_controller.load_camera_dialog)

        self.view3D_icon.clicked.connect(self._main_controller.change_view_plot_mode)
        self.view3D_text.clicked.connect(self._main_controller.change_view_plot_mode)
        self._roll_spin.valueChanged.connect(self._main_controller.change_roll)
        self._roll_scroll.valueChanged.connect(self._main_controller.change_roll)
        self._ar_spin.valueChanged.connect(self._main_controller.change_ar)
        self._ar_scroll.valueChanged.connect(self._main_controller.change_ar)
        self._dec_spin.valueChanged.connect(self._main_controller.change_dec)
        self._dec_scroll.valueChanged.connect(self._main_controller.change_dec)
        self._source_button.clicked.connect(self._main_controller.open_source)
        self._about_button.clicked.connect(self._main_controller.open_about_dialog)
        
        #event signal
        self._model.load_stars_file_changed.connect(self.open_stars)
        self._model.load_movements_file_changed.connect(self.open_movements)
        self._model.load_camera_file_changed.connect(self.open_camera)

        self._model.camera_name_changed.connect(self.load_camera)

        self._model.view_plot_mode_changed.connect(self.change_mode_view_icon)
        self._model.view_plot_mode_changed.connect(self.change_mode_view_text)
        
        self._model.manual_controls_enable_chaged.connect(self.enable_manual_controls)
        self._model.roll_changed.connect(self.change_roll)
        self._model.ar_changed.connect(self.change_ar)
        self._model.dec_changed.connect(self.change_dec)
        
    def open_stars(self):
        file = QFileDialog(self)
        file.setNameFilter("*.csv")
        file.setFileMode(QFileDialog.ExistingFile)
        file.setWindowTitle('Load Stars File')
        if file.exec_():
            fileName = file.selectedFiles()
            fileName = fileName[0]
            self._main_controller.change_stars_input_file(fileName)
    
    def open_movements(self):
        file = QFileDialog(self)
        file.setNameFilter("*.csv")
        file.setFileMode(QFileDialog.ExistingFile)
        file.setWindowTitle('Load Movements File')
        if file.exec_():
            fileName = file.selectedFiles()
            fileName = fileName[0]
            self._main_controller.change_movements_input_file(fileName)
    
    def open_camera(self):
        file = QFileDialog(self)
        file.setNameFilter("*.json")
        file.setFileMode(QFileDialog.ExistingFile)
        file.setWindowTitle('Load Camera File')
        if file.exec_():
            fileName = file.selectedFiles()
            fileName = fileName[0]
            self._main_controller.change_camera_input_file(fileName)
    
    def load_camera(self,value):
        self._camera_file.setText(value)
    
    def change_mode_view_icon(self,value):
        icon1 = QIcon()
        if value:
            icon1.addFile(u":/icon/icons/3d.png", QSize(), QIcon.Normal)
        else:
            icon1.addFile(u":/icon/icons/axis.png", QSize(), QIcon.Normal)
        self.view3D_icon.setIcon(icon1)
        self.view3D_icon.setIconSize(QSize(64, 64))
        self.view3D_icon.setChecked(value)

    def change_mode_view_text(self,value):
        self.view3D_text.setChecked(value)
    
    def change_roll(self, value):
        self._roll_scroll.setValue(value)
        self._roll_spin.setValue(value)
    
    def change_ar(self, value):
        self._ar_scroll.setValue(value)
        self._ar_spin.setValue(value)
    
    def change_dec(self, value):
        self._dec_scroll.setValue(value)
        self._dec_spin.setValue(value)
    
    def enable_manual_controls(self,value):
        self._dec_scroll.setDisabled(not value)
        self._dec_spin.setDisabled(not value)
        self._ar_scroll.setDisabled(not value)
        self._ar_spin.setDisabled(not value)
        self._roll_scroll.setDisabled(not value)
        self._roll_spin.setDisabled(not value)
    
    @property
    def view_plot_widget(self):
        return self.viewPlot
    
    @property
    def view_automatic_control_frame(self) -> AutomaticMovements:
        self._automatic_control_frame.file = self._file
        self._automatic_control_frame.play_button = self._play_button
        self._automatic_control_frame.movement_play_progress_bar = self._movement_play_progress_bar

        return self._automatic_control_frame