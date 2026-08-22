import os
import sys
import json
import random

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gui.bang_yeu_cau import BangYeuCauTaiNguyen
from gui.engine_adapter import (
    cac_buoc_mo_phong,
    kiem_tra_du_lieu,
    tao_trang_thai,
)

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMessageBox, QPushButton,
    QSlider, QSpinBox, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget
)


#TV5
class TableInputModule(QWidget):
    data_validated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_default_sample_data()

    def setup_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setSpacing(10)

        group_config = QGroupBox("Cấu hình hệ thống")
        layout_config = QHBoxLayout()

        layout_config.addWidget(QLabel("Số tiến trình (n):"))
        self.input_n = QSpinBox()
        self.input_n.setRange(1, 200)
        self.input_n.setValue(5)
        layout_config.addWidget(self.input_n)

        layout_config.addWidget(QLabel("Số loại tài nguyên (m):"))
        self.input_m = QSpinBox()
        self.input_m.setRange(1, 100)
        self.input_m.setValue(3)
        layout_config.addWidget(self.input_m)

        btn_init = QPushButton("Tạo ma trận")
        btn_init.clicked.connect(self.generate_matrix_grid)
        layout_config.addWidget(btn_init)

        group_config.setLayout(layout_config)
        layout_main.addWidget(group_config)

        layout_main.addWidget(QLabel("<b>Bảng Available (Tài nguyên hiện có):</b>"))
        self.grid_available = QTableWidget()
        self.grid_available.setMaximumHeight(65)
        layout_main.addWidget(self.grid_available)

        layout_tables = QHBoxLayout()
        
        box_max = QVBoxLayout()
        box_max.addWidget(QLabel("<b>Max (Tối đa):</b>"))
        self.grid_max = QTableWidget()
        box_max.addWidget(self.grid_max)
        layout_tables.addLayout(box_max)

        box_alloc = QVBoxLayout()
        box_alloc.addWidget(QLabel("<b>Allocation (Đã cấp):</b>"))
        self.grid_alloc = QTableWidget()
        box_alloc.addWidget(self.grid_alloc)
        layout_tables.addLayout(box_alloc)

        box_need = QVBoxLayout()
        box_need.addWidget(QLabel("<b>Need (Cần thêm):</b>"))
        self.grid_need = QTableWidget()
        box_need.addWidget(self.grid_need)
        layout_tables.addLayout(box_need)

        layout_main.addLayout(layout_tables)

        self.display_total = QLabel("<b>Tổng tài nguyên (Total):</b> Chưa tính toán")
        self.display_total.setStyleSheet("color: #1e3a8a; font-size: 12px;")
        layout_main.addWidget(self.display_total)

        layout_actions = QHBoxLayout()

        btn_process = QPushButton("Kiểm tra & Tính Need")
        btn_process.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold; padding: 6px;")
        btn_process.clicked.connect(self.process_need_calculation)
        layout_actions.addWidget(btn_process)

        btn_rand = QPushButton("Sinh ngẫu nhiên")
        btn_rand.clicked.connect(self.randomize_dataset)
        layout_actions.addWidget(btn_rand)

        btn_export = QPushButton("Lưu JSON")
        btn_export.clicked.connect(self.export_to_json)
        layout_actions.addWidget(btn_export)

        btn_import = QPushButton("Mở JSON")
        btn_import.clicked.connect(self.import_from_json)
        layout_actions.addWidget(btn_import)

        layout_main.addLayout(layout_actions)
        self.setLayout(layout_main)

    def disconnect_signals(self):
        try:
            self.grid_max.cellChanged.disconnect(self.validate_cell_entry)
        except (TypeError, RuntimeError):
            pass
        try:
            self.grid_alloc.cellChanged.disconnect(self.validate_cell_entry)
        except (TypeError, RuntimeError):
            pass

    def connect_signals(self):
        self.grid_max.cellChanged.connect(self.validate_cell_entry)
        self.grid_alloc.cellChanged.connect(self.validate_cell_entry)

    def generate_matrix_grid(self):
        self.disconnect_signals()

        val_n = self.input_n.value()
        val_m = self.input_m.value()

        headers_col = [chr(65 + idx) for idx in range(val_m)]
        headers_row = [f"P{idx}" for idx in range(val_n)]

        self.grid_available.setRowCount(1)
        self.grid_available.setColumnCount(val_m)
        self.grid_available.setHorizontalHeaderLabels(headers_col)
        self.grid_available.setVerticalHeaderLabels(["Available"])
        self.grid_available.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for grid in [self.grid_max, self.grid_alloc, self.grid_need]:
            grid.setRowCount(val_n)
            grid.setColumnCount(val_m)
            grid.setHorizontalHeaderLabels(headers_col)
            grid.setVerticalHeaderLabels(headers_row)
            grid.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for r in range(val_n):
            for c in range(val_m):
                cell_item = QTableWidgetItem("0")
                cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                cell_item.setTextAlignment(Qt.AlignCenter)
                self.grid_need.setItem(r, c, cell_item)
                
                if not self.grid_max.item(r, c): 
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.grid_max.setItem(r, c, item)
                if not self.grid_alloc.item(r, c): 
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.grid_alloc.setItem(r, c, item)

        for c in range(val_m):
            if not self.grid_available.item(0, c): 
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.grid_available.setItem(0, c, item)

        self.connect_signals()

    def validate_cell_entry(self, row_idx, col_idx):
        try:
            item_max = self.grid_max.item(row_idx, col_idx)
            item_alloc = self.grid_alloc.item(row_idx, col_idx)

            if not item_max or not item_alloc:
                return

            limit_val = int(item_max.text())
            allocated_val = int(item_alloc.text())

            if allocated_val > limit_val or allocated_val < 0 or limit_val < 0:
                item_alloc.setBackground(Qt.red)
                item_max.setBackground(Qt.red)
            else:
                item_alloc.setBackground(Qt.white)
                item_max.setBackground(Qt.white)
        except ValueError:
            src = self.sender()
            if src:
                curr_item = src.item(row_idx, col_idx)
                if curr_item: 
                    curr_item.setBackground(Qt.red)

    def process_need_calculation(self):
        val_n = self.input_n.value()
        val_m = self.input_m.value()
        
        is_faulty = False
        error_details = []

        for r in range(val_n):
            for c in range(val_m):
                try:
                    alloc_val = int(self.grid_alloc.item(r, c).text())
                    max_val = int(self.grid_max.item(r, c).text())

                    if alloc_val > max_val:
                        is_faulty = True
                        error_details.append(f"P{r} ({chr(65+c)}): Đã cấp ({alloc_val}) > Tối đa ({max_val})")
                        self.grid_alloc.item(r, c).setBackground(Qt.red)
                    else:
                        calc_need = max_val - alloc_val
                        self.grid_need.item(r, c).setText(str(calc_need))
                        self.grid_alloc.item(r, c).setBackground(Qt.white)
                except ValueError:
                    is_faulty = True
                    error_details.append(f"Ô P{r}-{chr(65+c)}: Không phải số nguyên")

        if is_faulty:
            QMessageBox.critical(self, "Lỗi Dữ Liệu", "Dữ liệu nhập vào chưa chính xác:\n\n" + "\n".join(error_details))
            return False

        totals = []
        for c in range(val_m):
            try:
                free_val = int(self.grid_available.item(0, c).text())
                used_val = sum(int(self.grid_alloc.item(r, c).text()) for r in range(val_n))
                totals.append(f"{chr(65+c)} = {free_val + used_val}")
            except ValueError:
                QMessageBox.critical(self, "Lỗi Dữ Liệu", f"Available ô {chr(65+c)} không hợp lệ!")
                return False

        self.display_total.setText(f"<b>Total (Available + Sum(Alloc)):</b> {', '.join(totals)}")
        
        data_payload = self.get_current_data()
        self.data_validated.emit(data_payload)
        return True

    def get_current_data(self):
        val_n, val_m = self.input_n.value(), self.input_m.value()
        return {
            "n": val_n,
            "m": val_m,
            "available": [int(self.grid_available.item(0, c).text()) for c in range(val_m)],
            "max": [[int(self.grid_max.item(r, c).text()) for c in range(val_m)] for r in range(val_n)],
            "allocation": [[int(self.grid_alloc.item(r, c).text()) for c in range(val_m)] for r in range(val_n)],
            "need": [[int(self.grid_need.item(r, c).text()) for c in range(val_m)] for r in range(val_n)]
        }

    def load_default_sample_data(self):
        sample = {
            "n": 5, "m": 3,
            "available": [3, 3, 2],
            "max": [
                [7, 5, 3],
                [3, 2, 2],
                [9, 0, 2],
                [2, 2, 2],
                [4, 3, 3]
            ],
            "allocation": [
                [0, 1, 0],
                [2, 0, 0],
                [3, 0, 2],
                [2, 1, 1],
                [0, 0, 2]
            ]
        }
        self.apply_dataset(sample)

    def apply_dataset(self, payload):
        self.input_n.setValue(payload["n"])
        self.input_m.setValue(payload["m"])
        self.generate_matrix_grid()

        self.disconnect_signals()

        for c in range(payload["m"]):
            self.grid_available.item(0, c).setText(str(payload["available"][c]))

        for r in range(payload["n"]):
            for c in range(payload["m"]):
                self.grid_max.item(r, c).setText(str(payload["max"][r][c]))
                self.grid_alloc.item(r, c).setText(str(payload["allocation"][r][c]))

        self.connect_signals()
        self.process_need_calculation()

    def randomize_dataset(self):
        val_n = self.input_n.value()
        val_m = self.input_m.value()

        self.disconnect_signals()

        for c in range(val_m):
            self.grid_available.item(0, c).setText(str(random.randint(2, 6)))

        for r in range(val_n):
            for c in range(val_m):
                limit = random.randint(3, 10)
                used = random.randint(0, limit)
                self.grid_max.item(r, c).setText(str(limit))
                self.grid_alloc.item(r, c).setText(str(used))

        self.connect_signals()
        self.process_need_calculation()

    def export_to_json(self):
        if not self.process_need_calculation():
            return

        file_dest, _ = QFileDialog.getSaveFileName(self, "Lưu dữ liệu", "input.json", "JSON Files (*.json)")
        if file_dest:
            payload = self.get_current_data()
            with open(file_dest, "w", encoding="utf-8") as f_out:
                json.dump(payload, f_out, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Thông Báo", "Lưu file JSON thành công!")

    def import_from_json(self):
        file_src, _ = QFileDialog.getOpenFileName(self, "Mở dữ liệu", "", "JSON Files (*.json)")
        if file_src:
            try:
                with open(file_src, "r", encoding="utf-8") as f_in:
                    payload = json.load(f_in)
                self.apply_dataset(payload)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi File", f"Không thể đọc file JSON:\n{str(e)}")


#TV6
class SimulationModule(QWidget):
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.steps = []
        self.current_step_idx = 0
        self.is_auto_running = False
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.execute_next_step)

        self.setup_ui()

    def setup_ui(self):
        layout_main = QVBoxLayout()
        layout_main.setSpacing(10)

        group_controls = QGroupBox("Điều Khiển Mô Phỏng")
        layout_controls = QHBoxLayout()

        self.btn_step = QPushButton("▶ Chạy Từng Bước")
        self.btn_step.clicked.connect(self.execute_next_step)

        self.btn_auto = QPushButton("⏩ Chạy Tự Động")
        self.btn_auto.clicked.connect(self.toggle_auto_run)

        self.btn_reset = QPushButton("↺ Đặt Lại")
        self.btn_reset.setStyleSheet("background-color: #ef4444; color: white;")
        self.btn_reset.clicked.connect(self.reset_simulation)

        layout_controls.addWidget(self.btn_step)
        layout_controls.addWidget(self.btn_auto)
        layout_controls.addWidget(self.btn_reset)

        layout_controls.addWidget(QLabel("Tốc độ:"))
        self.slider_speed = QSlider(Qt.Horizontal)
        self.slider_speed.setRange(200, 2000)
        self.slider_speed.setValue(1000)
        self.slider_speed.setInvertedAppearance(True)
        self.slider_speed.valueChanged.connect(self.update_timer_interval)
        layout_controls.addWidget(self.slider_speed)

        self.lbl_speed_val = QLabel("1000 ms")
        layout_controls.addWidget(self.lbl_speed_val)

        group_controls.setLayout(layout_controls)
        layout_main.addWidget(group_controls)

        self.status_badge = QLabel("SẴN SÀNG MÔ PHỎNG")
        self.status_badge.setAlignment(Qt.AlignCenter)
        self.status_badge.setFont(QFont("Arial", 11, QFont.Bold))
        self.status_badge.setStyleSheet("background-color: #94a3b8; color: white; border-radius: 6px; padding: 6px;")
        layout_main.addWidget(self.status_badge)

        layout_main.addWidget(QLabel("<b>Nhật ký các bước thực thi Thuật toán Banker:</b>"))
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(5)
        self.log_table.setHorizontalHeaderLabels([
            "Bước", "Tiến trình (Pi)", "Kiểm tra (Need ≤ Work)", "Work mới (Work + Alloc)", "Trạng thái"
        ])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout_main.addWidget(self.log_table)

        self.setLayout(layout_main)

    def load_data(self, data):
        self.dataset = data
        self.reset_simulation()
        self.fetch_steps_from_engine()

    def fetch_steps_from_engine(self):
        """Gọi engine thật ở engine/banker.py qua lớp cầu nối gui/engine_adapter.py.

        Không gọi thẳng engine để nếu sau này engine đổi, chỉ phải sửa một chỗ.
        """
        self.steps = []
        if not self.dataset:
            return

        loi = kiem_tra_du_lieu(self.dataset)
        if loi:
            QMessageBox.warning(self, "Dữ liệu không hợp lệ", loi)
            return

        self.trang_thai = tao_trang_thai(self.dataset)
        self.steps = cac_buoc_mo_phong(self.trang_thai)

    def execute_next_step(self):
        if not self.steps:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng ấn 'Kiểm tra & Tính Need' bên phân hệ nhập liệu trước!")
            return

        if self.current_step_idx >= len(self.steps):
            self.stop_auto_run()
            return

        step_data = self.steps[self.current_step_idx]
        row = self.log_table.rowCount()
        self.log_table.insertRow(row)

        self.log_table.setItem(row, 0, QTableWidgetItem(str(step_data["step"])))
        self.log_table.setItem(row, 1, QTableWidgetItem(step_data["process"]))
        self.log_table.setItem(row, 2, QTableWidgetItem(step_data["check"]))
        self.log_table.setItem(row, 3, QTableWidgetItem(step_data["work_new"]))
        self.log_table.setItem(row, 4, QTableWidgetItem(step_data["status"]))

        if step_data["is_safe"]:
            if self.current_step_idx == len(self.steps) - 1:
                seq_str = " ➔ ".join(step_data["safe_seq"])
                self.status_badge.setText(f"HỆ THỐNG AN TOÀN | Chuỗi: < {seq_str} >")
                self.status_badge.setStyleSheet("background-color: #16a34a; color: white; border-radius: 6px; padding: 6px;")
            else:
                self.status_badge.setText(f"ĐANG DUYỆT: {step_data['process']}")
                self.status_badge.setStyleSheet("background-color: #2563eb; color: white; border-radius: 6px; padding: 6px;")
            
            for col in range(5):
                self.log_table.item(row, col).setBackground(QColor("#dcfce7"))
        else:
            self.status_badge.setText("HỆ THỐNG BẤT AN TOÀN (CÓ THỂ XẢY RA DEADLOCK)")
            self.status_badge.setStyleSheet("background-color: #dc2626; color: white; border-radius: 6px; padding: 6px;")
            for col in range(5):
                self.log_table.item(row, col).setBackground(QColor("#fee2e2"))

        self.current_step_idx += 1

        if self.current_step_idx >= len(self.steps):
            self.stop_auto_run()

    def toggle_auto_run(self):
        if self.is_auto_running:
            self.stop_auto_run()
        else:
            if self.current_step_idx >= len(self.steps):
                self.reset_simulation()
            self.is_auto_running = True
            self.btn_auto.setText("⏸ Tạm Dừng")
            self.timer.start(self.slider_speed.value())

    def stop_auto_run(self):
        self.is_auto_running = False
        self.timer.stop()
        self.btn_auto.setText("⏩ Chạy Tự Động")

    def reset_simulation(self):
        self.stop_auto_run()
        self.current_step_idx = 0
        self.log_table.setRowCount(0)
        self.status_badge.setText("SẴN SÀNG MÔ PHỎNG")
        self.status_badge.setStyleSheet("background-color: #94a3b8; color: white; border-radius: 6px; padding: 6px;")
        if self.dataset:
            self.fetch_steps_from_engine()

    def update_timer_interval(self, value):
        self.lbl_speed_val.setText(f"{value} ms")
        if self.is_auto_running:
            self.timer.setInterval(value)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chương Trình Mô Phỏng Thuật Toán Banker - Nhóm 8")
        self.resize(1280, 680)

        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        self.input_module = TableInputModule()
        splitter.addWidget(self.input_module)

        self.sim_module = SimulationModule()
        splitter.addWidget(self.sim_module)

        # Panel yeu cau tai nguyen / giai phong / hoan tac / bieu do (TV6)
        self.request_module = BangYeuCauTaiNguyen()
        splitter.addWidget(self.request_module)

        splitter.setSizes([460, 560, 420])
        main_layout.addWidget(splitter)

        self.input_module.data_validated.connect(self.sim_module.load_data)
        self.input_module.data_validated.connect(self.nap_panel_yeu_cau)
        self.request_module.trang_thai_thay_doi.connect(self.dong_bo_sau_thay_doi)

        initial_data = self.input_module.get_current_data()
        self.sim_module.load_data(initial_data)
        self.nap_panel_yeu_cau(initial_data)

    def nap_panel_yeu_cau(self, dataset):
        """Nap du lieu vua nhap vao panel yeu cau tai nguyen."""
        loi = kiem_tra_du_lieu(dataset)
        if loi:
            self.request_module.dat_trang_thai(None)
            return
        self.request_module.dat_trang_thai(tao_trang_thai(dataset))

    def dong_bo_sau_thay_doi(self, trang_thai):
        """Sau khi cap phat / giai phong, chay lai mo phong tren trang thai moi."""
        self.sim_module.dataset = {
            "n": trang_thai.n,
            "m": trang_thai.m,
            "available": list(trang_thai.available),
            "max": [list(h) for h in trang_thai.max],
            "allocation": [list(h) for h in trang_thai.allocation],
            "need": [list(h) for h in trang_thai.need],
        }
        self.sim_module.reset_simulation()
        self.sim_module.fetch_steps_from_engine()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())