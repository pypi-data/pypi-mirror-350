import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from pySPM.tools.timer_display import Ui_ToF_Timer
from pySPM.tools.win32_helper import findWindow, getText


class GUI_Timer(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_ToF_Timer()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def update(self):
        ok = False
        A = findWindow("Measurement Progress")
        if len(A) > 0:
            B = findWindow(C="Edit", parent=A[0])
            if len(B) > 0:
                AnalTime = int(getText(B[2]).replace(",", ""))
                TotScans = int(getText(B[1]).replace(",", ""))
                Scans = int(getText(B[0]).replace(",", ""))
                self.ui.label_2.setText(f"Scans: {Scans} / {TotScans}")
                self.ui.label_3.setText(f"Analysis Time: {AnalTime} s")
                self.ui.progressBar.setValue(Scans)
                self.ui.progressBar.setMaximum(TotScans)
                ok = True
        if not ok:
            self.ui.label.setText(
                "Remaining time: Unavailable (measurement not in progress?)"
            )
            return
        if Scans > 0:
            r = AnalTime * (TotScans - Scans) / Scans
            h = int(r // 3600)
            m = int((r - h * 3600) // 60)
            s = int(r - h * 3600 - m * 60)
            self.ui.label.setText(f"Remaining time: {h:02d}:{m:02d}:{s:02d}")
        else:
            self.ui.label.setText("Remaining time: Unknown")


def main():
    app = QApplication(sys.argv)
    window = GUI_Timer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
