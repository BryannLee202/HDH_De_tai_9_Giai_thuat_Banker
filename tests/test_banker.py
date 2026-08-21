# -*- coding: utf-8 -*-
"""Bộ kiểm thử tự động cho engine.

Chủ sở hữu: TV8.

Nguyên tắc kiểm thử: **người viết test không nên là người viết code**. TV8 giữ
file này, TV4 giữ ``engine/``. Nói được điều này khi bảo vệ là một điểm cộng.

Kết quả kỳ vọng dưới đây lấy từ bảng chạy tay trong Chương 2 của TV3 — TUYỆT ĐỐI
không tự suy đoán, cũng không sửa test cho khớp với code.

Chạy:  ``python -m unittest discover -s tests -v``

Toàn bộ test sẽ đỏ cho tới khi TV4 cài xong engine. Đó là đúng: test viết trước,
code viết sau.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.banker import (  # noqa: E402
    kiem_tra_an_toan,
    kiem_tra_hop_le,
    yeu_cau_tai_nguyen,
)
from engine.banker_types import BankerState, LoiDuLieu, Verdict  # noqa: E402


def vi_du_chuan() -> BankerState:
    """5 tiến trình, 3 loại tài nguyên. Tổng hệ thống A=10, B=5, C=7."""
    return BankerState(
        available=[3, 3, 2],
        max=[[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        allocation=[[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    )


class TestCauTrucDuLieu(unittest.TestCase):

    def test_need_tinh_dung(self):
        self.assertEqual(
            vi_du_chuan().need,
            [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]],
        )

    def test_total_la_hang_so(self):
        self.assertEqual(vi_du_chuan().total, [10, 5, 7])


class TestKiemTraAnToan(unittest.TestCase):

    def test_tc01_trang_thai_ban_dau_an_toan(self):
        kq = kiem_tra_an_toan(vi_du_chuan())
        self.assertTrue(kq.an_toan)
        self.assertEqual(kq.chuoi, [1, 3, 4, 2, 0])

    def test_tc01_co_ghi_nhat_ky_tung_buoc(self):
        kq = kiem_tra_an_toan(vi_du_chuan())
        self.assertEqual(len(kq.nhat_ky), 5, "phai ghi du 5 vong lap")
        self.assertEqual(kq.nhat_ky[0].work_truoc, [3, 3, 2])
        self.assertEqual(kq.nhat_ky[-1].work_sau, [10, 5, 7])

    def test_tc06_khong_con_tai_nguyen_ranh_thi_khong_an_toan(self):
        tt = vi_du_chuan()
        tt.available = [0, 0, 0]
        kq = kiem_tra_an_toan(tt)
        self.assertFalse(kq.an_toan)
        self.assertEqual(kq.chuoi, [])
        self.assertTrue(kq.treo, "phai liet ke cac tien trinh con treo")

    def test_tc07_moi_need_bang_khong_thi_an_toan_ngay(self):
        tt = vi_du_chuan()
        tt.max = [list(hang) for hang in tt.allocation]
        kq = kiem_tra_an_toan(tt)
        self.assertTrue(kq.an_toan)
        self.assertEqual(len(kq.chuoi), 5)

    def test_tc08_bien_mot_tien_trinh_mot_tai_nguyen(self):
        tt = BankerState(available=[1], max=[[2]], allocation=[[1]])
        self.assertTrue(kiem_tra_an_toan(tt).an_toan)


class TestYeuCauTaiNguyen(unittest.TestCase):

    def test_tc02_p1_xin_1_0_2_duoc_cap_phat(self):
        tt = vi_du_chuan()
        kq = yeu_cau_tai_nguyen(tt, 1, [1, 0, 2])
        self.assertEqual(kq.ket_luan, Verdict.CAP_PHAT)
        self.assertEqual(tt.available, [2, 3, 0])
        self.assertEqual(tt.allocation[1], [3, 0, 2])

    def test_tc03_p4_xin_3_3_0_phai_cho_vi_thieu_tai_nguyen(self):
        tt = vi_du_chuan()
        yeu_cau_tai_nguyen(tt, 1, [1, 0, 2])          # sau TC02, Available = (2,3,0)
        kq = yeu_cau_tai_nguyen(tt, 4, [3, 3, 0])
        self.assertEqual(kq.ket_luan, Verdict.CHO)

    def test_tc04_p0_xin_0_2_0_bi_tu_choi_vi_khong_an_toan(self):
        """Đủ tài nguyên rảnh, nhưng cấp vào thì trạng thái không còn an toàn."""
        tt = vi_du_chuan()
        yeu_cau_tai_nguyen(tt, 1, [1, 0, 2])
        kq = yeu_cau_tai_nguyen(tt, 0, [0, 2, 0])
        self.assertEqual(kq.ket_luan, Verdict.CHO)

    def test_tc04_trang_thai_khong_bi_hong_sau_khi_tu_choi(self):
        """Rollback phải nguyên vẹn — đây là chỗ hay cài sai nhất."""
        tt = vi_du_chuan()
        yeu_cau_tai_nguyen(tt, 1, [1, 0, 2])
        truoc = (list(tt.available), [list(h) for h in tt.allocation])
        yeu_cau_tai_nguyen(tt, 0, [0, 2, 0])
        self.assertEqual(tt.available, truoc[0])
        self.assertEqual(tt.allocation, truoc[1])

    def test_tc05_xin_vuot_qua_need_thi_bao_loi(self):
        tt = vi_du_chuan()
        kq = yeu_cau_tai_nguyen(tt, 2, [7, 0, 0])     # Need[2] = (6,0,0)
        self.assertEqual(kq.ket_luan, Verdict.LOI)

    def test_ba_ket_cuc_co_ba_ly_do_khac_nhau(self):
        tt = vi_du_chuan()
        a = yeu_cau_tai_nguyen(tt, 1, [1, 0, 2]).ly_do
        b = yeu_cau_tai_nguyen(tt, 4, [3, 3, 0]).ly_do
        c = yeu_cau_tai_nguyen(tt, 2, [7, 0, 0]).ly_do
        self.assertEqual(len({a, b, c}), 3, "ba ket cuc phai co ba cau ly do rieng")


class TestDuLieuKhongHopLe(unittest.TestCase):

    def test_tc09_allocation_vuot_qua_max(self):
        tt = vi_du_chuan()
        tt.allocation[2] = [9, 0, 3]                  # Max[2] = (9,0,2)
        with self.assertRaises(LoiDuLieu):
            kiem_tra_hop_le(tt)

    def test_tc09_gia_tri_am(self):
        tt = vi_du_chuan()
        tt.available = [-1, 3, 2]
        with self.assertRaises(LoiDuLieu):
            kiem_tra_hop_le(tt)

    def test_tc09_so_cot_khong_khop(self):
        tt = vi_du_chuan()
        tt.max[0] = [7, 5]
        with self.assertRaises(LoiDuLieu):
            kiem_tra_hop_le(tt)

    def test_vi_du_chuan_phai_hop_le(self):
        kiem_tra_hop_le(vi_du_chuan())               # không được ném lỗi


if __name__ == "__main__":
    unittest.main(verbosity=2)

    def test_tc18_p0_giai_phong_giup_p1_chay(self):
        banker = BankerState(
            available=[2, 2],
            max_claim=[[2, 2], [4, 4]],
            allocation=[[1, 1], [1, 1]],
        )
        kq = kiem_tra_an_toan(banker)
        self.assertTrue(kq.an_toan)
        self.assertEqual(kq.chuoi, [0, 1])

    def test_tc19_xin_vua_du_bang_available(self):
        tt = vi_du_chuan()
        kq = yeu_cau_tai_nguyen(tt, 1, [1, 2, 2])
        self.assertNotEqual(kq.ket_luan, Verdict.CHO)

    def test_tc20_p1_xin_rong(self):
        tt = vi_du_chuan()
        kq = yeu_cau_tai_nguyen(tt, 1, [0, 0, 0])
        self.assertEqual(kq.ket_luan, Verdict.CAP_PHAT)
        self.assertEqual(tt.available, [3, 3, 2])

    def test_tc21_allocation_ban_dau_toan_khong(self):
        banker = BankerState(
            available=[10, 5, 7],
            max_claim=[[7, 5, 3], [3, 2, 2]],
            allocation=[[0, 0, 0], [0, 0, 0]],
        )
        kq = kiem_tra_an_toan(banker)
        self.assertTrue(kq.an_toan)

    def test_tc22_tien_trinh_khong_ton_tai(self):
        tt = vi_du_chuan()
        with self.assertRaises(IndexError):
            yeu_cau_tai_nguyen(tt, 99, [1, 0, 0])
