# Chương 4.1 — Kiến trúc chương trình

Chủ sở hữu: TV1. Đây là bản nguồn của Chương 4.1 trong quyển báo cáo. Bốn biểu đồ dưới đây viết bằng Mermaid nên GitHub tự vẽ ra hình — mở file này trên web, chụp màn hình từng hình rồi chèn vào Word, không phải vẽ lại bằng draw.io.

## 1. Nguyên tắc thiết kế

Chương trình chia làm ba lớp tách rời:

| Lớp | Thư mục | Trách nhiệm | Phụ trách |
|---|---|---|---|
| Giao diện | gui/ | Nhận thao tác người dùng, hiển thị kết quả | TV5, TV6 |
| Xử lý | engine/ | Toàn bộ giải thuật Banker | TV4 |
| Dữ liệu | data/ | Bộ dữ liệu mẫu định dạng JSON | TV5 |

Lý do tách lớp xử lý khỏi lớp giao diện: engine không được phụ thuộc vào bất kỳ thư viện đồ hoạ nào, nhờ vậy chạy và kiểm thử tự động được từ dòng lệnh mà không cần mở cửa sổ. Đây cũng là điều kiện để TV8 viết bộ kiểm thử tự động cho thuật toán.

Hợp đồng dữ liệu giữa hai lớp nằm ở engine/banker_types.py, do TV1 định nghĩa và chốt trước khi TV4, TV5, TV6 bắt đầu viết code.

## 2. Hình 4.1 — Sơ đồ khối ba lớp

```mermaid
flowchart TD
U["Người dùng"] --> G1
U --> G2
U --> G3
subgraph G["Lớp giao diện - gui/"]
G1["Màn hình nhập liệu - TV5"]
G2["Màn hình mô phỏng - TV6"]
G3["Module xuất báo cáo - TV1"]
end
subgraph E["Lớp xử lý - engine/"]
E1["banker.py - giải thuật"]
E2["banker_types.py - hợp đồng dữ liệu"]
end
subgraph D["Lớp dữ liệu"]
D1["data/*.json"]
D2["Tệp báo cáo PDF hoặc Excel"]
end
G1 --> E2
G2 --> E1
G3 --> E2
E1 --> E2
G1 --> D1
G3 --> D2
```

## 3. Hình 4.2 — Biểu đồ ca sử dụng

```mermaid
flowchart LR
A(["Người dùng"])
A --- UC1["Nhập ma trận tài nguyên"]
A --- UC2["Nạp hoặc lưu bộ dữ liệu"]
A --- UC3["Kiểm tra trạng thái an toàn"]
A --- UC4["Chạy mô phỏng từng bước"]
A --- UC5["Gửi yêu cầu tài nguyên"]
A --- UC6["Kết thúc tiến trình"]
A --- UC7["Xuất báo cáo kết quả"]
UC1 -.-> UC8["Kiểm tra hợp lệ dữ liệu"]
UC3 -.-> UC9["Sinh chuỗi an toàn"]
UC5 -.-> UC3
```

Ca sử dụng đáng chú ý nhất là **Gửi yêu cầu tài nguyên**: nó luôn kéo theo ca **Kiểm tra trạng thái an toàn**, vì thuật toán phải giả lập cấp phát rồi mới quyết định chấp thuận hay bắt chờ.

## 4. Hình 4.3 — Biểu đồ lớp

```mermaid
classDiagram
class BankerState {
+list available
+list max
+list allocation
+int n
+int m
+need() list
+total() list
+copy() BankerState
+from_json_file(path) BankerState
+to_json_file(path)
}
class StepLog {
+int buoc
+list work_truoc
+int tien_trinh
+list need
+list allocation
+list work_sau
+list bo_qua
}
class SafetyResult {
+bool an_toan
+list chuoi
+list nhat_ky
+list treo
+chuoi_dep() str
}
class RequestResult {
+Verdict ket_luan
+str ly_do
+list nhat_ky
}
class Verdict {
CAP_PHAT
CHO
LOI
}
class LoiDuLieu {
+str ma
+str thong_diep
}
SafetyResult o-- StepLog
RequestResult o-- StepLog
RequestResult --> Verdict
BankerState ..> LoiDuLieu
```

Điểm thiết kế quan trọng: `need` **không phải** dữ liệu lưu trữ mà là thuộc tính tính ra từ `max - allocation` mỗi lần đọc. Nhờ vậy `Need = Max - Allocation` luôn đúng, không bao giờ lệch — đây là lỗi kinh điển khi cài giải thuật Banker.

## 5. Hình 4.4 — Biểu đồ tuần tự: gửi yêu cầu tài nguyên

```mermaid
sequenceDiagram
actor ND as Người dùng
participant GUI as Màn hình mô phỏng
participant EN as banker.py
participant ST as BankerState
ND->>GUI: Chọn P1, nhập Request 1 0 2
GUI->>EN: yeu_cau_tai_nguyen
EN->>ST: đọc need của P1
alt Request lớn hơn Need
EN-->>GUI: LOI - xin vượt quá nhu cầu khai báo
else Request lớn hơn Available
EN-->>GUI: CHO - không đủ tài nguyên rảnh
else Hợp lệ
EN->>ST: copy tạo bản sao thử
EN->>ST: giả lập cấp phát trên bản sao
EN->>EN: kiem_tra_an_toan
alt An toàn
EN->>ST: ghi đè trạng thái thật
EN-->>GUI: CAP_PHAT kèm nhật ký từng bước
else Không an toàn
EN->>ST: huỷ bản sao, giữ nguyên trạng thái cũ
EN-->>GUI: CHO - cấp vào sẽ không an toàn
end
end
GUI-->>ND: Hiển thị kết luận, lý do và bảng nhật ký
```

Nhánh **Không an toàn** là chỗ hay cài sai nhất: phải thao tác trên bản sao rồi mới ghi đè, tuyệt đối không sửa trực tiếp trạng thái thật rồi trừ ngược lại.

## 6. Phân chia tệp và người phụ trách

| Tệp | Nội dung | Phụ trách |
|---|---|---|
| engine/banker_types.py | Hợp đồng dữ liệu dùng chung | TV1 |
| engine/banker.py | Hai thủ tục chính của giải thuật | TV4 |
| engine/demo.py | Chạy thử từ dòng lệnh | TV4 |
| gui/ màn hình nhập liệu | Lưới ma trận, kiểm tra hợp lệ, tệp JSON | TV5 |
| gui/ màn hình mô phỏng | Nhật ký, chạy từng bước, yêu cầu tài nguyên | TV6 |
| gui/xuat_bao_cao.py | Xuất kết quả ra PDF hoặc Excel | TV1 |
| tests/test_banker.py | Bộ kiểm thử tự động | TV8 |
