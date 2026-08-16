# -*- coding: utf-8 -*-
"""Giải thuật Banker — phần cài đặt.

Chủ sở hữu: TV4.

Đây là KHUNG. Các hàm bên dưới đã có sẵn chữ ký, tài liệu và mã giả trong phần
docstring; nhiệm vụ của TV4 là thay từng chỗ ``TODO`` bằng code thật, bám đúng
mã giả trong Chương 2 của TV3.

Hai quy tắc không được vi phạm:

1. File này **không được import bất kỳ thư viện giao diện nào** (PyQt, tkinter…).
   Engine phải chạy được từ dòng lệnh, tách rời hoàn toàn khỏi giao diện.
2. Mọi hàm phải trả về **nhật ký từng bước**, không chỉ trả về đúng/sai. Giao
   diện của TV6 cần nhật ký này để chiếu lại từng vòng lặp cho người xem.

Chạy thử:  ``python -m engine.demo``
Chạy test: ``python -m unittest discover -s tests -v``
"""

from __future__ import annotations

from typing import List

from .banker_types import (
    BankerState,
    LoiDuLieu,
    RequestResult,
    SafetyResult,
    StepLog,
    Vector,
    Verdict,
    cong,
    nho_hon_hoac_bang,
)


# --------------------------------------------------------------------------
# Kiểm tra tính hợp lệ của dữ liệu đầu vào
# --------------------------------------------------------------------------

def kiem_tra_hop_le(trang_thai: BankerState) -> None:
    """Ném ``LoiDuLieu`` nếu dữ liệu đầu vào sai.

    Các ràng buộc phải kiểm tra:

    - E01: ``max`` và ``allocation`` phải cùng số hàng, mỗi hàng đủ ``m`` cột.
    - E02: mọi giá trị phải là số nguyên không âm.
    - E03: ``0 <= allocation[i][j] <= max[i][j]`` với mọi i, j.

    Thông điệp lỗi phải chỉ rõ ô nào sai, ví dụ::

        Ô P2–B: đã cấp 4 nhưng khai báo tối đa 3

    Giao diện của TV5 hiển thị thẳng thông điệp này nên phải viết bằng tiếng Việt.
    """
    # TODO(TV4): cài đặt theo mô tả trên.
    raise NotImplementedError("TV4 cài đặt kiem_tra_hop_le()")


# --------------------------------------------------------------------------
# Thủ tục 1 — Kiểm tra trạng thái an toàn
# --------------------------------------------------------------------------

def kiem_tra_an_toan(trang_thai: BankerState) -> SafetyResult:
    """Thủ tục kiểm tra trạng thái an toàn.

    Mã giả (Chương 2, TV3)::

        1. Work <- Available;  Finish[i] <- false với mọi i;  chuoi <- []
        2. Tìm chỉ số i thoả:  Finish[i] = false VÀ Need[i] <= Work
           Nếu không tìm được -> sang bước 4
        3. Work <- Work + Allocation[i]
           Finish[i] <- true;  chuoi.thêm(Pi);  quay lại bước 2
        4. Nếu Finish[i] = true với mọi i -> (AN TOÀN, chuoi)
           ngược lại                       -> (KHÔNG AN TOÀN, rỗng)

    Độ phức tạp ``O(m * n^2)``: vòng ngoài lặp tối đa ``n`` lần, mỗi lần quét
    ``n`` tiến trình, mỗi phép so sánh vector tốn ``m``.

    Mỗi vòng lặp phải ghi một ``StepLog`` gồm: ``work_truoc``, tiến trình được
    chọn, ``need`` và ``allocation`` của nó, ``work_sau``, và danh sách tiến
    trình bị bỏ qua kèm lý do.

    Khi không chọn được tiến trình nào, ghi một ``StepLog`` cuối với
    ``tien_trinh=None`` và điền ``treo`` bằng các tiến trình còn lại — TV6 dùng
    thông tin này để hiện câu "Không tiến trình nào có Need <= Work".
    """
    # TODO(TV4): cài đặt theo mã giả trên.
    raise NotImplementedError("TV4 cài đặt kiem_tra_an_toan()")


# --------------------------------------------------------------------------
# Thủ tục 2 — Xử lý yêu cầu tài nguyên
# --------------------------------------------------------------------------

def yeu_cau_tai_nguyen(trang_thai: BankerState, i: int, request: Vector) -> RequestResult:
    """Thủ tục xử lý yêu cầu tài nguyên của tiến trình ``i``.

    Mã giả (Chương 2, TV3)::

        1. Nếu Request > Need[i]    -> LỖI: xin vượt quá nhu cầu đã khai báo
        2. Nếu Request > Available  -> CHỜ: hệ thống không đủ tài nguyên rảnh
        3. Giả lập cấp phát:
               Available     <- Available     - Request
               Allocation[i] <- Allocation[i] + Request
               (Need tự đúng theo vì là thuộc tính tính ra)
        4. Chạy kiem_tra_an_toan() trên trạng thái giả lập:
               an toàn       -> giữ nguyên, CẤP PHÁT
               không an toàn -> KHÔI PHỤC nguyên trạng, tiến trình phải CHỜ

    Bước 4 là chỗ hay cài sai nhất. Dùng ``trang_thai.copy()`` để thử, chỉ ghi
    đè trạng thái thật khi kết quả an toàn — không được sửa trực tiếp rồi trừ
    ngược lại.

    Ba kết cục phải có ba câu ``ly_do`` khác nhau, ví dụ::

        "Cấp phát: trạng thái sau khi cấp vẫn an toàn"
        "Chờ: không đủ tài nguyên rảnh, cần 3 đơn vị A nhưng chỉ còn 2"
        "Từ chối: yêu cầu vượt quá Need đã khai báo của P0"
    """
    # TODO(TV4): cài đặt theo mã giả trên.
    raise NotImplementedError("TV4 cài đặt yeu_cau_tai_nguyen()")


def giai_phong(trang_thai: BankerState, i: int, vector: Vector) -> None:
    """Tiến trình ``i`` trả bớt tài nguyên về hệ thống."""
    # TODO(TV4): trừ vào allocation[i], cộng vào available; chặn khi trả quá số đang giữ.
    raise NotImplementedError("TV4 cài đặt giai_phong()")


def ket_thuc_tien_trinh(trang_thai: BankerState, i: int) -> None:
    """Tiến trình ``i`` kết thúc, trả TOÀN BỘ ``allocation[i]`` về ``available``.

    TV6 gắn hàm này vào nút "Kết thúc tiến trình" — chính là mảnh còn thiếu để
    phần mềm mô phỏng trọn chu trình yêu cầu, sử dụng, giải phóng mà đề bài đòi hỏi.
    """
    # TODO(TV4): cài đặt.
    raise NotImplementedError("TV4 cài đặt ket_thuc_tien_trinh()")


# --------------------------------------------------------------------------
# Điểm cộng — liệt kê tất cả chuỗi an toàn
# --------------------------------------------------------------------------

def tat_ca_chuoi_an_toan(trang_thai: BankerState, gioi_han: int = 1000) -> List[List[int]]:
    """Liệt kê mọi chuỗi an toàn bằng quay lui.

    Chức năng ăn điểm cộng: chứng minh được chuỗi an toàn **không duy nhất**.
    Với ví dụ chuẩn, cả ``<P1,P3,P4,P2,P0>`` và ``<P1,P3,P4,P0,P2>`` đều hợp lệ.

    ``gioi_han`` chặn số chuỗi trả về để không treo khi ``n`` lớn — số chuỗi có
    thể tăng theo giai thừa.
    """
    # TODO(TV4): quay lui, mỗi bước thử mọi tiến trình chưa xong có Need <= Work.
    raise NotImplementedError("TV4 cài đặt tat_ca_chuoi_an_toan()")
