# -*- coding: utf-8 -*-
"""Hợp đồng dữ liệu dùng chung giữa engine (TV4) và giao diện (TV5, TV6).

Chủ sở hữu: TV1.

Đây là nguồn đúng duy nhất về *hình dạng* của dữ liệu. Mọi thay đổi ở file này
đều phá vỡ code của ba người, nên phải báo trước trong nhóm và được TV1 duyệt.

Nguyên tắc thiết kế quan trọng nhất: ``need`` là thuộc tính **tính ra**, không
phải dữ liệu lưu trữ. Nhờ vậy ``Need = Max - Allocation`` luôn đúng và không thể
lệch nhau — đây là lỗi kinh điển khi cài giải thuật Banker.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple

Vector = List[int]
Matrix = List[List[int]]


# --------------------------------------------------------------------------
# Kết luận và lỗi
# --------------------------------------------------------------------------

class Verdict(Enum):
    """Ba kết cục có thể có của một yêu cầu tài nguyên.

    Ba giá trị này phải hiển thị bằng ba câu lý do KHÁC NHAU trên giao diện.
    Gộp chung một câu là dấu hiệu chưa hiểu thuật toán và bị trừ điểm.
    """

    CAP_PHAT = "CAP_PHAT"   # Cấp phát: trạng thái sau khi cấp vẫn an toàn
    CHO = "CHO"             # Chờ: không đủ tài nguyên rảnh, hoặc cấp vào sẽ không an toàn
    LOI = "LOI"             # Lỗi: yêu cầu vượt quá Need đã khai báo


class LoiDuLieu(Exception):
    """Dữ liệu đầu vào không hợp lệ.

    Giao diện bắt ngoại lệ này rồi hiển thị thẳng ``thong_diep`` cho người dùng,
    nên thông điệp phải viết bằng tiếng Việt và chỉ rõ ô nào sai.
    """

    def __init__(self, ma: str, thong_diep: str):
        super().__init__(f"[{ma}] {thong_diep}")
        self.ma = ma
        self.thong_diep = thong_diep


# --------------------------------------------------------------------------
# Nhật ký thực thi
# --------------------------------------------------------------------------

@dataclass
class StepLog:
    """Một vòng lặp của thủ tục kiểm tra an toàn.

    TV6 dùng đúng các trường này làm cột cho bảng nhật ký trên giao diện, và
    bảng đó phải khớp với bảng chạy tay trong Chương 2 của TV3.
    """

    buoc: int
    work_truoc: Vector
    tien_trinh: Optional[int]          # None khi không chọn được tiến trình nào
    need: Optional[Vector]
    allocation: Optional[Vector]
    work_sau: Vector
    bo_qua: List[Tuple[int, str]] = field(default_factory=list)   # (chỉ số, lý do)
    ghi_chu: str = ""


@dataclass
class SafetyResult:
    """Kết quả kiểm tra trạng thái an toàn."""

    an_toan: bool
    chuoi: List[int]                   # chuỗi an toàn, rỗng nếu không an toàn
    nhat_ky: List[StepLog] = field(default_factory=list)
    treo: List[int] = field(default_factory=list)   # tiến trình không kết thúc được

    def chuoi_dep(self, tien_to: str = "P") -> str:
        """Chuỗi an toàn dạng ``P1 → P3 → P4 → P2 → P0`` để hiện lên giao diện."""
        return " → ".join(f"{tien_to}{i}" for i in self.chuoi)


@dataclass
class RequestResult:
    """Kết quả xử lý một yêu cầu tài nguyên."""

    ket_luan: Verdict
    ly_do: str
    nhat_ky: List[StepLog] = field(default_factory=list)


# --------------------------------------------------------------------------
# Trạng thái hệ thống
# --------------------------------------------------------------------------

@dataclass
class BankerState:
    """Trạng thái cấp phát tài nguyên của hệ thống.

    Với ``n`` tiến trình và ``m`` loại tài nguyên:

    ==============  ==========  ====================================================
    Trường          Kích thước  Ý nghĩa
    ==============  ==========  ====================================================
    ``available``   m           Số thực thể mỗi loại còn rảnh
    ``max``         n × m       Nhu cầu tối đa tiến trình khai báo trước khi chạy
    ``allocation``  n × m       Số thực thể đang được cấp cho tiến trình
    ``need``        n × m       Tính ra: ``max - allocation``
    ==============  ==========  ====================================================
    """

    available: Vector
    max: Matrix
    allocation: Matrix
    ten_tai_nguyen: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.ten_tai_nguyen:
            self.ten_tai_nguyen = [chr(ord("A") + j) for j in range(len(self.available))]

    # -- kích thước -------------------------------------------------------

    @property
    def n(self) -> int:
        """Số tiến trình."""
        return len(self.max)

    @property
    def m(self) -> int:
        """Số loại tài nguyên."""
        return len(self.available)

    # -- Need: luôn tính ra, không bao giờ lưu ----------------------------

    @property
    def need(self) -> Matrix:
        """``Need = Max - Allocation``, tính lại mỗi lần đọc.

        Vì Need không được lưu, chỉ cần sửa ``allocation`` là Need tự đúng theo.
        Giao diện phải hiển thị bảng này ở chế độ chỉ đọc.
        """
        return [
            [self.max[i][j] - self.allocation[i][j] for j in range(self.m)]
            for i in range(self.n)
        ]

    @property
    def total(self) -> Vector:
        """Tổng số thực thể mỗi loại trong hệ thống — phải là hằng số."""
        return [
            self.available[j] + sum(self.allocation[i][j] for i in range(self.n))
            for j in range(self.m)
        ]

    # -- sao chép ---------------------------------------------------------

    def copy(self) -> "BankerState":
        """Bản sao sâu.

        TV4 dùng hàm này để giả lập cấp phát rồi khôi phục khi trạng thái kết
        quả không an toàn. Không được sửa trực tiếp rồi trừ ngược lại.
        """
        return BankerState(
            available=list(self.available),
            max=[list(hang) for hang in self.max],
            allocation=[list(hang) for hang in self.allocation],
            ten_tai_nguyen=list(self.ten_tai_nguyen),
        )

    # -- đọc ghi file .json ----------------------------------------------

    @classmethod
    def from_dict(cls, d: dict) -> "BankerState":
        return cls(
            available=d["available"],
            max=d["max"],
            allocation=d["allocation"],
            ten_tai_nguyen=d.get("ten_tai_nguyen", []),
        )

    def to_dict(self) -> dict:
        return {
            "n": self.n,
            "m": self.m,
            "ten_tai_nguyen": self.ten_tai_nguyen,
            "available": self.available,
            "max": self.max,
            "allocation": self.allocation,
        }

    @classmethod
    def from_json_file(cls, duong_dan: str) -> "BankerState":
        with open(duong_dan, encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def to_json_file(self, duong_dan: str) -> None:
        with open(duong_dan, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------
# Tiện ích
# --------------------------------------------------------------------------

def nho_hon_hoac_bang(x: Vector, y: Vector) -> bool:
    """So sánh vector theo từng thành phần: ``x <= y`` khi ``x[j] <= y[j]`` với mọi j.

    Đây là phép so sánh được dùng ở bước 2 của thủ tục kiểm tra an toàn. Chương 2
    của TV3 phải định nghĩa rõ phép này, nếu không mã giả sẽ mơ hồ.
    """
    return all(a <= b for a, b in zip(x, y))


def cong(x: Vector, y: Vector) -> Vector:
    return [a + b for a, b in zip(x, y)]


def tru(x: Vector, y: Vector) -> Vector:
    return [a - b for a, b in zip(x, y)]
