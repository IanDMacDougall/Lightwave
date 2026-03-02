from UI.communications import LightwaveCommunications

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap

from utilities import ensure_directory_exists, app_data_dir, remove_past_scheduled_calls, save_data, SCHEDULED_CALLS_FILE, load_data

if __name__ == "__main__":
    app = QApplication([])
    
    
    # Ensure directory
    ensure_directory_exists(app_data_dir)  
    
    # Update scheduled calls from local files 
    scheduled_calls = load_data(SCHEDULED_CALLS_FILE)
    remove_past_scheduled_calls()  
    save_data(SCHEDULED_CALLS_FILE, scheduled_calls)
    window = LightwaveCommunications()  
    
    # Logo display ("splash screen")
    splash_pix = QPixmap('logo.png')  
    
    splash = QSplashScreen(splash_pix)
    splash.show()
    
    app.processEvents()
    
    QTimer.singleShot(3000, splash.close)
    QTimer.singleShot(3000, window.show)
    
    # Execute
    app.exec()