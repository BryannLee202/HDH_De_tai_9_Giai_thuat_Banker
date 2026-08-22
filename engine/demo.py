# -*- coding: utf-8 -*-
"""Chay engine tu dong lenh, khong can giao dien.

Chu so huu: TV4.

Muc dich: chung minh engine tach roi hoan toan khoi giao dien. Chay:

    python -m engine.demo

Ket qua mong doi voi bo du lieu chuan: AN TOAN, chuoi <P1, P3, P4, P2, P0>.
"""

import os

from .banker import kiem_tra_an_toan, kiem_tra_hop_le
from .banker_types import BankerState

DU_LIEU = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "vi-du-chuan.json")


def main() -> None:
    tt = BankerState.from_json_file(DU_LIEU)
    kiem_tra_hop_le(tt)

    print(f"n = {tt.n} tien trinh, m = {tt.m} loai tai nguyen")
    print(f"Available = {tt.available}")
    print(f"Total     = {tt.total}")
    print("Need      =")
    for i, hang in enumerate(tt.need):
        print(f"  P{i}: {hang}")

    kq = kiem_tra_an_toan(tt)
    print()
    if kq.an_toan:
        print("KET LUAN: AN TOAN")
        print("Chuoi an toan:", kq.chuoi_dep())
    else:
        print("KET LUAN: KHONG AN TOAN")
        print("Tien trinh con treo:", kq.treo)

    print("\nNhat ky tung buoc:")
    for b in kq.nhat_ky:
        print(f"  Buoc {b.buoc}: Work {b.work_truoc} -> chon P{b.tien_trinh} -> {b.work_sau}")


if __name__ == "__main__":
    main()
