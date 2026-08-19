import json
import random
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMessageBox, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)

class TableInputModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Phân Hệ Nhập Liệu - Thuật Toán Banker")
        self.resize(800, 620)

        layout_main = QVBoxLayout()

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

        btn_init = QPushButton("Khởi tạo ma trận")
        btn_init.clicked.connect(self.generate_matrix_grid)
        layout_config.addWidget(btn_init)

        group_config.setLayout(layout_config)
        layout_main.addWidget(group_config)

        layout_main.addWidget(QLabel("<b>Bảng Available (Tài nguyên hiện có):</b>"))
        self.grid_available = QTableWidget()
        layout_main.addWidget(self.grid_available)

        layout_tables = QHBoxLayout()
        
        box_max = QVBoxLayout()
        box_max.addWidget(QLabel("<b>Bảng Max (Tối đa):</b>"))
        self.grid_max = QTableWidget()
        box_max.addWidget(self.grid_max)
        layout_tables.addLayout(box_max)

        box_alloc = QVBoxLayout()
        box_alloc.addWidget(QLabel("<b>Bảng Allocation (Đã cấp):</b>"))
        self.grid_alloc = QTableWidget()
        box_alloc.addWidget(self.grid_alloc)
        layout_tables.addLayout(box_alloc)

        box_need = QVBoxLayout()
        box_need.addWidget(QLabel("<b>Bảng Need (Cần thêm):</b>"))
        self.grid_need = QTableWidget()
        box_need.addWidget(self.grid_need)
        layout_tables.addLayout(box_need)

        layout_main.addLayout(layout_tables)

        self.display_total = QLabel("<b>Tổng tài nguyên (Total):</b> Chưa tính toán")
        layout_main.addWidget(self.display_total)

        layout_actions = QHBoxLayout()

        btn_process = QPushButton("Tính Need & Kiểm tra")
        btn_process.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold;")
        btn_process.clicked.connect(self.process_need_calculation)
        layout_actions.addWidget(btn_process)

        btn_rand = QPushButton("Sinh ngẫu nhiên")
        btn_rand.clicked.connect(self.randomize_dataset)
        layout_actions.addWidget(btn_rand)

        btn_export = QPushButton("Lưu file (.json)")
        btn_export.clicked.connect(self.export_to_json)
        layout_actions.addWidget(btn_export)

        btn_import = QPushButton("Mở file (.json)")
        btn_import.clicked.connect(self.import_from_json)
        layout_actions.addWidget(btn_import)

        layout_main.addLayout(layout_actions)
        self.setLayout(layout_main)

        self.generate_matrix_grid()

    def generate_matrix_grid(self):
        val_n = self.input_n.value()
        val_m = self.input_m.value()

        headers_col = [chr(65 + idx) for idx in range(val_m)]
        headers_row = [f"P{idx}" for idx in range(val_n)]

        self.grid_available.setRowCount(1)
        self.grid_available.setColumnCount(val_m)
        self.grid_available.setHorizontalHeaderLabels(headers_col)
        self.grid_available.setVerticalHeaderLabels(["Available"])

        for grid in [self.grid_max, self.grid_alloc, self.grid_need]:
            grid.setRowCount(val_n)
            grid.setColumnCount(val_m)
            grid.setHorizontalHeaderLabels(headers_col)
            grid.setVerticalHeaderLabels(headers_row)

        for r in range(val_n):
            for c in range(val_m):
                cell_item = QTableWidgetItem("0")
                cell_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.grid_need.setItem(r, c, cell_item)
                
                if not self.grid_max.item(r, c): 
                    self.grid_max.setItem(r, c, QTableWidgetItem("0"))
                if not self.grid_alloc.item(r, c): 
                    self.grid_alloc.setItem(r, c, QTableWidgetItem("0"))

        for c in range(val_m):
            if not self.grid_available.item(0, c): 
                self.grid_available.setItem(0, c, QTableWidgetItem("0"))

        self.grid_max.cellChanged.connect(self.validate_cell_entry)
        self.grid_alloc.cellChanged.connect(self.validate_cell_entry)

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
                        error_details.append(f"Tiến trình P{r} (Tài nguyên {chr(65+c)}): Đã cấp ({alloc_val}) > Tối đa ({max_val})")
                        self.grid_alloc.item(r, c).setBackground(Qt.red)
                    else:
                        calc_need = max_val - alloc_val
                        self.grid_need.item(r, c).setText(str(calc_need))
                        self.grid_alloc.item(r, c).setBackground(Qt.white)
                except ValueError:
                    is_faulty = True
                    error_details.append(f"Ô P{r}-{chr(65+c)}: Kiểu dữ liệu không hợp lệ")

        if is_faulty:
            QMessageBox.critical(self, "Lỗi Dữ Liệu", "Phát hiện ô dữ liệu chưa chính xác:\n\n" + "\n".join(error_details))
            return False

        totals = []
        for c in range(val_m):
            free_val = int(self.grid_available.item(0, c).text())
            used_val = sum(int(self.grid_alloc.item(r, c).text()) for r in range(val_n))
            totals.append(f"{chr(65+c)} = {free_val + used_val}")

        self.display_total.setText(f"<b>Tổng tài nguyên (Total = Available + Sum(Alloc)):</b> {', '.join(totals)}")
        QMessageBox.information(self, "Thành Công", "Đã tính xong bảng Need và Tổng tài nguyên hệ thống!")
        return True

    def randomize_dataset(self):
        val_n = self.input_n.value()
        val_m = self.input_m.value()

        self.grid_max.cellChanged.disconnect()
        self.grid_alloc.cellChanged.disconnect()

        for c in range(val_m):
            self.grid_available.item(0, c).setText(str(random.randint(2, 6)))

        for r in range(val_n):
            for c in range(val_m):
                limit = random.randint(3, 10)
                used = random.randint(0, limit)
                self.grid_max.item(r, c).setText(str(limit))
                self.grid_alloc.item(r, c).setText(str(used))

        self.grid_max.cellChanged.connect(self.validate_cell_entry)
        self.grid_alloc.cellChanged.connect(self.validate_cell_entry)
        self.process_need_calculation()

    def export_to_json(self):
        if not self.process_need_calculation():
            return

        file_dest, _ = QFileDialog.getSaveFileName(self, "Lưu tập dữ liệu", "data/input.json", "JSON Files (*.json)")
        if file_dest:
            val_n, val_m = self.input_n.value(), self.input_m.value()
            payload = {
                "n": val_n, 
                "m": val_m,
                "available": [int(self.grid_available.item(0, c).text()) for c in range(val_m)],
                "max": [[int(self.grid_max.item(r, c).text()) for c in range(val_m)] for r in range(val_n)],
                "allocation": [[int(self.grid_alloc.item(r, c).text()) for c in range(val_m)] for r in range(val_n)]
            }
            with open(file_dest, "w", encoding="utf-8") as f_out:
                json.dump(payload, f_out, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Thông Báo", "Lưu file thành công!")

    def import_from_json(self):
        file_src, _ = QFileDialog.getOpenFileName(self, "Mở tập dữ liệu", "data/", "JSON Files (*.json)")
        if file_src:
            with open(file_src, "r", encoding="utf-8") as f_in:
                payload = json.load(f_in)

            self.input_n.setValue(payload["n"])
            self.input_m.setValue(payload["m"])
            self.generate_matrix_grid()

            self.grid_max.cellChanged.disconnect()
            self.grid_alloc.cellChanged.disconnect()

            for c in range(payload["m"]):
                self.grid_available.item(0, c).setText(str(payload["available"][c]))

            for r in range(payload["n"]):
                for c in range(payload["m"]):
                    self.grid_max.item(r, c).setText(str(payload["max"][r][c]))
                    self.grid_alloc.item(r, c).setText(str(payload["allocation"][r][c]))

            self.grid_max.cellChanged.connect(self.validate_cell_entry)
            self.grid_alloc.cellChanged.connect(self.validate_cell_entry)
            self.process_need_calculation()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TableInputModule()
    view.show()
    sys.exit(app.exec_())