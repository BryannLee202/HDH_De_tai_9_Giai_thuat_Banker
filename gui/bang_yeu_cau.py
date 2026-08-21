# -*- coding: utf-8 -*-
"""Bảng yêu cầu tài nguyên, giải phóng, hoàn tác và biểu đồ tài nguyên.

Chủ sở hữu: TV6.

Đây là năm chức năng còn thiếu ở bản giao diện đầu tiên. Đề bài yêu cầu phần mềm
mô phỏng **đầy đủ các yêu cầu của thuật toán**, nghĩa là phải có trọn chu trình
yêu cầu — sử dụng — giải phóng, chứ không chỉ mỗi nút kiểm tra an toàn:

1. Gửi yêu cầu tài nguyên, ba kết cục với **ba câu lý do khác nhau**
2. Kết thúc tiến trình, trả toàn bộ tài nguyên về hệ thống
3. Hoàn tác về trạng thái trước đó
4. Biểu đồ cột tài nguyên đã cấp / còn rảnh
5. Đồ thị phân bổ tài nguyên — phục vụ Chương 3 của TV7

Không dùng matplotlib để khỏi thêm thư viện ngoài; biểu đồ vẽ bằng QPainter.
"""

from __future__ import annotations

from typing import List, Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QComboBox, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

from engine.banker import (
    giai_phong,
    ket_thuc_tien_trinh,
    kiem_tra_an_toan,
    yeu_cau_tai_nguyen,
)
from engine.banker_types import BankerState, Verdict

MAU = {
    Verdict.CAP_PHAT: ("#16a34a", "CẤP PHÁT"),
    Verdict.CHO: ("#d97706", "CHỜ"),
    Verdict.LOI: ("#dc2626", "LỖI"),
}


# --------------------------------------------------------------------------
# Biểu đồ cột tài nguyên
# --------------------------------------------------------------------------

class BieuDoTaiNguyen(QWidget):
    """Cột ngang cho mỗi loại tài nguyên: phần đã cấp và phần còn rảnh."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trang_thai: Optional[BankerState] = None
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def cap_nhat(self, trang_thai: Optional[BankerState]) -> None:
        self.trang_thai = trang_thai
        self.update()

    def paintEvent(self, event):  # noqa: N802 (tên do Qt quy định)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if self.trang_thai is None:
            p.setPen(QColor("#6b7280"))
            p.drawText(self.rect(), Qt.AlignCenter, "Chưa có dữ liệu")
            return

        tt = self.trang_thai
        tong = tt.total
        le_trai, cao_cot, khoang = 46, 20, 10
        rong = max(self.width() - le_trai - 70, 40)

        for j in range(tt.m):
            y = 8 + j * (cao_cot + khoang)
            da_cap = tong[j] - tt.available[j]
            ti_le = (da_cap / tong[j]) if tong[j] else 0.0

            p.setPen(QColor("#111827"))
            p.setFont(QFont("Segoe UI", 9, QFont.Bold))
            p.drawText(6, y + cao_cot - 5, tt.ten_tai_nguyen[j])

            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(QColor("#e5e7eb")))
            p.drawRect(le_trai, y, rong, cao_cot)
            p.setBrush(QBrush(QColor("#2563eb")))
            p.drawRect(le_trai, y, int(rong * ti_le), cao_cot)

            p.setPen(QColor("#374151"))
            p.setFont(QFont("Segoe UI", 8))
            p.drawText(le_trai + rong + 8, y + cao_cot - 5,
                       "{}/{}".format(da_cap, tong[j]))


# --------------------------------------------------------------------------
# Đồ thị phân bổ tài nguyên
# --------------------------------------------------------------------------

class DoThiPhanBo(QWidget):
    """Đồ thị phân bổ tài nguyên: tiến trình hình tròn, tài nguyên hình vuông.

    Mũi tên từ tài nguyên sang tiến trình là **cạnh cấp phát**, từ tiến trình
    sang tài nguyên là **cạnh yêu cầu**. TV7 dùng hình này cho Chương 3.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trang_thai: Optional[BankerState] = None
        self.setMinimumHeight(210)

    def cap_nhat(self, trang_thai: Optional[BankerState]) -> None:
        self.trang_thai = trang_thai
        self.update()

    def paintEvent(self, event):  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if self.trang_thai is None or self.trang_thai.n == 0:
            p.setPen(QColor("#6b7280"))
            p.drawText(self.rect(), Qt.AlignCenter, "Chưa có dữ liệu")
            return

        tt = self.trang_thai
        n, m = min(tt.n, 8), tt.m
        r = 15
        y_p, y_r = 34, self.height() - 40
        buoc_p = max(self.width() // (n + 1), 1)
        buoc_r = max(self.width() // (m + 1), 1)

        vi_tri_p = [((i + 1) * buoc_p, y_p) for i in range(n)]
        vi_tri_r = [((j + 1) * buoc_r, y_r) for j in range(m)]

        p.setFont(QFont("Segoe UI", 8))
        for j, (x, y) in enumerate(vi_tri_r):
            p.setPen(QPen(QColor("#374151"), 1))
            p.setBrush(QBrush(QColor("#fde68a")))
            p.drawRect(x - r, y - r, 2 * r, 2 * r)
            p.setPen(QColor("#111827"))
            p.drawText(x - r, y - r, 2 * r, 2 * r, Qt.AlignCenter,
                       tt.ten_tai_nguyen[j])

        for i, (x, y) in enumerate(vi_tri_p):
            p.setPen(QPen(QColor("#374151"), 1))
            p.setBrush(QBrush(QColor("#bfdbfe")))
            p.drawEllipse(x - r, y - r, 2 * r, 2 * r)
            p.setPen(QColor("#111827"))
            p.drawText(x - r, y - r, 2 * r, 2 * r, Qt.AlignCenter,
                       "P{}".format(i))

        need = tt.need
        for i in range(n):
            xp, yp = vi_tri_p[i]
            for j in range(m):
                xr, yr = vi_tri_r[j]
                if tt.allocation[i][j] > 0:      # cạnh cấp phát: R -> P
                    p.setPen(QPen(QColor("#16a34a"), 1.6))
                    p.drawLine(xr, yr - r, xp, yp + r)
                elif need[i][j] > 0:             # cạnh yêu cầu: P -> R
                    p.setPen(QPen(QColor("#dc2626"), 1, Qt.DashLine))
                    p.drawLine(xp, yp + r, xr, yr - r)

        p.setPen(QColor("#6b7280"))
        p.setFont(QFont("Segoe UI", 8))
        p.drawText(6, 14, "Xanh liền: cạnh cấp phát R→P   ·   Đỏ đứt: cạnh yêu cầu P→R")


# --------------------------------------------------------------------------
# Bảng điều khiển
# --------------------------------------------------------------------------

class BangYeuCauTaiNguyen(QWidget):
    """Panel gửi yêu cầu, giải phóng, kết thúc tiến trình và hoàn tác."""

    trang_thai_thay_doi = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trang_thai: Optional[BankerState] = None
        self.lich_su: List[BankerState] = []
        self.ket_qua_yeu_cau: list = []
        self._dung_giao_dien()

    # -- dựng giao diện ---------------------------------------------------

    def _dung_giao_dien(self) -> None:
        ngoai = QVBoxLayout(self)

        hop = QGroupBox("Yêu cầu tài nguyên")
        v = QVBoxLayout(hop)

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Tiến trình:"))
        self.combo_p = QComboBox()
        h1.addWidget(self.combo_p)
        h1.addWidget(QLabel("Vector yêu cầu:"))
        self.o_request = QLineEdit()
        self.o_request.setPlaceholderText("ví dụ: 1 0 2")
        h1.addWidget(self.o_request, 1)
        v.addLayout(h1)

        h2 = QHBoxLayout()
        self.nut_gui = QPushButton("Gửi yêu cầu")
        self.nut_giai_phong = QPushButton("Giải phóng")
        self.nut_ket_thuc = QPushButton("Kết thúc tiến trình")
        self.nut_hoan_tac = QPushButton("Hoàn tác")
        self.nut_hoan_tac.setEnabled(False)
        for nut in (self.nut_gui, self.nut_giai_phong,
                    self.nut_ket_thuc, self.nut_hoan_tac):
            h2.addWidget(nut)
        v.addLayout(h2)

        self.nhan_ket_qua = QLabel("Chưa gửi yêu cầu nào.")
        self.nhan_ket_qua.setWordWrap(True)
        self.nhan_ket_qua.setStyleSheet(
            "padding:8px; border-radius:6px; background:#f3f4f6; color:#111827;")
        v.addWidget(self.nhan_ket_qua)
        ngoai.addWidget(hop)

        hop2 = QGroupBox("Tài nguyên đã cấp / tổng")
        v2 = QVBoxLayout(hop2)
        self.bieu_do = BieuDoTaiNguyen()
        v2.addWidget(self.bieu_do)
        ngoai.addWidget(hop2)

        hop3 = QGroupBox("Đồ thị phân bổ tài nguyên")
        v3 = QVBoxLayout(hop3)
        self.do_thi = DoThiPhanBo()
        v3.addWidget(self.do_thi)
        ngoai.addWidget(hop3)

        self.nut_gui.clicked.connect(self.gui_yeu_cau)
        self.nut_giai_phong.clicked.connect(self.thuc_hien_giai_phong)
        self.nut_ket_thuc.clicked.connect(self.thuc_hien_ket_thuc)
        self.nut_hoan_tac.clicked.connect(self.hoan_tac)

    # -- dữ liệu ----------------------------------------------------------

    def dat_trang_thai(self, trang_thai: Optional[BankerState]) -> None:
        """Nạp trạng thái mới, xoá lịch sử hoàn tác."""
        self.trang_thai = trang_thai
        self.lich_su = []
        self.ket_qua_yeu_cau = []
        self.nut_hoan_tac.setEnabled(False)
        self.combo_p.clear()
        if trang_thai is not None:
            self.combo_p.addItems(["P{}".format(i) for i in range(trang_thai.n)])
        self._ve_lai()

    def _ve_lai(self) -> None:
        self.bieu_do.cap_nhat(self.trang_thai)
        self.do_thi.cap_nhat(self.trang_thai)
        if self.trang_thai is not None:
            self.trang_thai_thay_doi.emit(self.trang_thai)

    def _luu_de_hoan_tac(self) -> None:
        if self.trang_thai is not None:
            self.lich_su.append(self.trang_thai.copy())
            self.nut_hoan_tac.setEnabled(True)

    def _doc_vector(self) -> Optional[List[int]]:
        """Đọc vector từ ô nhập, chấp nhận cách nhau bằng dấu cách hoặc phẩy."""
        if self.trang_thai is None:
            QMessageBox.warning(self, "Chưa có dữ liệu",
                                "Hãy nhập ma trận ở màn hình bên trái trước.")
            return None
        raw = self.o_request.text().replace(",", " ").split()
        try:
            vec = [int(x) for x in raw]
        except ValueError:
            QMessageBox.warning(self, "Sai định dạng",
                                "Vector chỉ gồm các số nguyên, cách nhau bằng dấu cách.")
            return None
        if len(vec) != self.trang_thai.m:
            QMessageBox.warning(
                self, "Sai số phần tử",
                "Cần đúng {} số, đang nhập {}.".format(self.trang_thai.m, len(vec)))
            return None
        if any(x < 0 for x in vec):
            QMessageBox.warning(self, "Giá trị âm", "Không nhận số âm.")
            return None
        return vec

    # -- hành động --------------------------------------------------------

    def gui_yeu_cau(self) -> None:
        vec = self._doc_vector()
        if vec is None:
            return
        i = self.combo_p.currentIndex()

        self._luu_de_hoan_tac()
        kq = yeu_cau_tai_nguyen(self.trang_thai, i, vec)
        self.ket_qua_yeu_cau.append(kq)

        mau, nhan = MAU[kq.ket_luan]
        self.nhan_ket_qua.setText("{} — {}".format(nhan, kq.ly_do))
        self.nhan_ket_qua.setStyleSheet(
            "padding:8px; border-radius:6px; color:white; background:{};".format(mau))

        if kq.ket_luan is not Verdict.CAP_PHAT:
            # trạng thái không đổi thì không cần giữ mốc hoàn tác
            self.lich_su.pop()
            self.nut_hoan_tac.setEnabled(bool(self.lich_su))
        self._ve_lai()

    def thuc_hien_giai_phong(self) -> None:
        vec = self._doc_vector()
        if vec is None:
            return
        i = self.combo_p.currentIndex()
        self._luu_de_hoan_tac()
        try:
            giai_phong(self.trang_thai, i, vec)
        except Exception as e:
            self.lich_su.pop()
            self.nut_hoan_tac.setEnabled(bool(self.lich_su))
            QMessageBox.warning(self, "Không giải phóng được", str(e))
            return
        self.nhan_ket_qua.setText(
            "ĐÃ GIẢI PHÓNG — P{} trả lại {} về hệ thống.".format(i, tuple(vec)))
        self.nhan_ket_qua.setStyleSheet(
            "padding:8px; border-radius:6px; color:white; background:#0e7490;")
        self._ve_lai()

    def thuc_hien_ket_thuc(self) -> None:
        if self.trang_thai is None:
            return
        i = self.combo_p.currentIndex()
        giu = list(self.trang_thai.allocation[i])
        self._luu_de_hoan_tac()
        ket_thuc_tien_trinh(self.trang_thai, i)
        self.nhan_ket_qua.setText(
            "KẾT THÚC — P{} trả toàn bộ {} về hệ thống. "
            "Available giờ là {}.".format(
                i, tuple(giu), tuple(self.trang_thai.available)))
        self.nhan_ket_qua.setStyleSheet(
            "padding:8px; border-radius:6px; color:white; background:#4338ca;")
        self._ve_lai()

    def hoan_tac(self) -> None:
        if not self.lich_su:
            return
        self.trang_thai = self.lich_su.pop()
        self.nut_hoan_tac.setEnabled(bool(self.lich_su))
        self.nhan_ket_qua.setText("Đã hoàn tác về trạng thái trước đó.")
        self.nhan_ket_qua.setStyleSheet(
            "padding:8px; border-radius:6px; background:#f3f4f6; color:#111827;")
        self._ve_lai()

    # -- tiện ích cho module xuất báo cáo của TV1 -------------------------

    def du_lieu_bao_cao(self):
        """Trả về (trang_thai, ket_qua_an_toan, lich_su_yeu_cau) cho ``xuat_html``."""
        if self.trang_thai is None:
            return None, None, []
        return (self.trang_thai,
                kiem_tra_an_toan(self.trang_thai),
                self.ket_qua_yeu_cau)
