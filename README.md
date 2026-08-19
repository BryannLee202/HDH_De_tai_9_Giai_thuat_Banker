# Bài tập lớn Hệ điều hành — Đề tài 9: Giải thuật Banker

Mô phỏng giải thuật Banker (deadlock avoidance) bằng phần mềm có giao diện, kèm quyển báo cáo.

| | |
|---|---|
| **Phần** | Deadlock |
| **Đề tài** | Giải thuật Banker |
| **Đối chứng so sánh** | Giải thuật đồ thị phân bổ tài nguyên (đề tài 10) |
| **Sản phẩm** | Quyển báo cáo + phần mềm có giao diện |
| **Nhân lực** | 8 thành viên · 4 tuần |

Kế hoạch phân công đầy đủ: [`docs/Phan-cong-De-tai-9-Giai-thuat-Banker.pdf`](docs/Phan-cong-De-tai-9-Giai-thuat-Banker.pdf)

---

## Phân công và nhánh làm việc

| TV | Họ tên | Nhiệm vụ | Nhánh | Thư mục sở hữu |
|---|---|---|---|---|
| TV1 | *Lê Minh Tài* | Nhóm trưởng · hợp đồng dữ liệu · kiến trúc · module xuất báo cáo | `tv1-kien-truc` | `engine/banker_types.py`, `docs/`, `report/chuong-4-tv1/` |
| TV2 | *Nguyễn Đức Khải* | Chương lý thuyết Deadlock | `tv2-chuong-ly-thuyet` | `report/chuong-1-tv2/` |
| TV3 | *Đặng Hoàng Phong* | Đặc tả thuật toán · mã giả · chạy tay | `tv3-dac-ta-thuat-toan` | `report/chuong-2-tv3/` |
| TV4 | *Nguyễn Minh Trí* | Engine — mã nguồn lõi | `tv4-engine` | `engine/` |
| TV5 |  Trần Đức Tân | Giao diện — nhập liệu và dữ liệu | `tv5-gui-nhap-lieu` | `gui/`, `data/` |
| TV6 | *Nguyễn Thái* | Giao diện — mô phỏng và trực quan | `tv6-gui-mo-phong` | `gui/` |
| TV7 | *Văn Hoàng* | Chương so sánh hai giải thuật | `tv7-chuong-so-sanh` | `report/chuong-3-tv7/` |
| TV8 | Nguyễn Thảo| Kiểm thử · chương kết quả · phản biện | `tv8-kiem-thu` | `tests/`, `report/chuong-5-tv8/` |

---

## Bảng làm việc chi tiết

### TV1 — Nhóm trưởng · Kiến trúc phần mềm · nhánh `tv1-kien-truc` · **có code**

**Kiến thức cần có:** Git nâng cao (nhánh, pull request, gộp mã) · UML (sơ đồ khối, ca sử dụng, biểu đồ lớp, biểu đồ tuần tự) · Python mức đọc ghi file và xuất PDF · Word (mục lục tự động, đánh số hình theo chương).

1. `git clone` rồi `git checkout tv1-kien-truc`
2. Điền tên 8 người vào bảng phân công phía trên
3. Vẽ 4 biểu đồ thiết kế bằng draw.io, lưu vào `docs/`
4. Viết module xuất báo cáo PDF/Excel trong `gui/`
5. Commit, push, mở pull request
6. Duyệt pull request của 7 người còn lại — **chỉ TV1 được bấm Merge**

### TV2 — Chương lý thuyết Deadlock · nhánh `tv2-chuong-ly-thuyet` · **không code**

**Kiến thức cần có:** 4 điều kiện Coffman · 4 hướng xử lý deadlock · phân biệt deadlock / starvation / livelock · bài toán 5 triết gia và khoá chéo semaphore · draw.io · cách trích dẫn tài liệu.

**Không cần cài đặt gì.** Vào repo trên web → đổi nhánh sang `tv2-chuong-ly-thuyet` → mở `report/chuong-1-tv2/` → **Add file → Upload files** → kéo `chuong-1.docx` vào → gõ mô tả → **Commit changes**.

### TV3 — Đặc tả thuật toán · nhánh `tv3-dac-ta-thuat-toan` · **không code** *(ưu tiên số 1)*

**Kiến thức cần có:** phải nắm thuật toán Banker **chắc hơn cả người viết code** — hai thủ tục kiểm tra an toàn và xử lý yêu cầu, phép so sánh vector theo từng thành phần, cách tính độ phức tạp `O(m·n²)`, và chạy tay ma trận không sai số.

**Không cần cài đặt gì**, upload qua web như TV2 vào `report/chuong-2-tv3/`. File `chuong-2.docx` bắt buộc phải có: mã giả 2 thủ tục, lưu đồ, **bảng chạy tay đủ 5 vòng lặp**, và 3 kịch bản yêu cầu với 3 lý do khác nhau. Sau đó họp 30 phút bàn giao mã giả cho TV4.

### TV4 — Engine · nhánh `tv4-engine` · **có code, nhiều nhất**

**Kiến thức cần có:** Python (lớp, dataclass, mảng hai chiều, ngoại lệ) · **sao chép sâu** — thiếu kiến thức này là hỏng bước rollback · thư viện `unittest` · hiểu mã giả của TV3.

1. `git checkout tv4-engine`
2. Chạy `python -m unittest discover -s tests -v` → thấy 16 test đỏ, đó là danh sách việc
3. Mở `engine/banker.py`, thay từng chỗ `TODO` bằng code thật
4. Thứ tự: `kiem_tra_hop_le` → `kiem_tra_an_toan` → `yeu_cau_tai_nguyen` → `giai_phong` → `tat_ca_chuoi_an_toan`
5. Mỗi hàm xong là một commit
6. Xong khi cả 16 test xanh

### TV5 — Giao diện nhập liệu · nhánh `tv5-gui-nhap-lieu` · **có code**

**Kiến thức cần có:** PyQt5 (bảng dữ liệu, ô nhập số, hộp thoại chọn file) · bắt sự kiện khi người dùng gõ để kiểm tra ngay · đọc ghi JSON · sinh số ngẫu nhiên có ràng buộc.

1. `git checkout tv5-gui-nhap-lieu`
2. **Họp với TV6 chốt bố cục hai vùng trước khi viết dòng code nào**
3. Tạo `gui/cua_so_chinh.py`, dựng khung cửa sổ
4. Làm lưới nhập, kiểm tra hợp lệ, tính `Need`
5. Làm menu Mở / Lưu, nạp 3 bộ mẫu trong `data/`

### TV6 — Giao diện mô phỏng · nhánh `tv6-gui-mo-phong` · **có code**

**Kiến thức cần có:** PyQt5 (bảng, bộ đếm thời gian, tín hiệu và khe cắm) · tô màu và tô sáng ô trong bảng · vẽ hình bằng matplotlib hoặc vẽ tay · ngăn xếp lịch sử để làm nút Hoàn tác.

1. `git checkout tv6-gui-mo-phong`
2. Tuần 1 dựng bảng nhật ký với dữ liệu giả, **không cần chờ TV4**
3. Ghép engine thật khi TV4 xong
4. Làm chạy từng bước, chạy tự động, panel yêu cầu tài nguyên
5. Làm nút Kết thúc tiến trình và Hoàn tác
6. Quay video demo — **để trên Google Drive, không commit vào repo**

### TV7 — Chương so sánh · nhánh `tv7-chuong-so-sanh` · **code ít**

**Kiến thức cần có:** giải thuật đồ thị phân bổ tài nguyên và ba loại cạnh · phát hiện chu trình trong đồ thị có hướng · **vì sao có chu trình chưa chắc đã deadlock** · vẽ biểu đồ bằng Excel hoặc matplotlib.

1. Vẽ 2 hình đồ thị đối chứng bằng draw.io
2. Lập bảng so sánh 7 tiêu chí, viết lời bình cho **từng dòng**
3. Chạy script đo của TV4 với `n` = 10, 20, 50, 100, 200
4. Vẽ biểu đồ thời gian, đối chiếu với đường cong `n²`
5. Upload `chuong-3.docx` vào `report/chuong-3-tv7/`

### TV8 — Kiểm thử · nhánh `tv8-kiem-thu` · **có code, mức nhẹ**

**Kiến thức cần có:** cách viết một ca kiểm thử (đầu vào — kỳ vọng — thực tế) · `unittest` ở mức đọc hiểu và thêm ca mới · GitHub Issues · chụp màn hình và trình bày bảng kết quả.

1. `git checkout tv8-kiem-thu`
2. Đọc 16 ca có sẵn trong `tests/test_banker.py`
3. Thêm tối thiểu 5 ca của riêng mình
4. Chạy phần mềm thật, chụp màn hình từng ca
5. Mỗi lỗi mở một issue, theo dõi đến khi đóng
6. Upload `chuong-5.docx` và soạn 15 câu hỏi phản biện

---

## Tài liệu học theo vai trò

### Dùng chung cho cả 8 người

| Tài liệu | Ở đâu |
|---|---|
| Kế hoạch phân công đầy đủ (có mã giả, bộ test, khung so sánh) | `docs/Phan-cong-De-tai-9-Giai-thuat-Banker.pdf` — **mục 03 là phần ai cũng phải nắm** |
| Ảnh đề bài gốc | `docs/de-bai/de-bai-goc.jpg` |
| Silberschatz, Galvin, Gagne — *Operating System Concepts*, chương **Deadlocks** | https://www.os-book.com — sách gốc của toàn bộ đề tài này |
| Slide bài giảng của thầy | Nguồn sát đề nhất. Nếu ký hiệu trong slide khác sách thì **theo slide**, vì thầy chấm theo đó |

### TV1 — Nhóm trưởng · Kiến trúc

- **Trong repo:** `engine/banker_types.py` — file bạn sở hữu, đã chạy được; đọc để giải thích cho TV4, TV5, TV6 khi họ hỏi
- Nhánh và pull request trên GitHub — https://docs.github.com/en/pull-requests
- Vẽ UML — https://app.diagrams.net (menu **Shape → UML** có sẵn mẫu biểu đồ lớp, ca sử dụng, tuần tự)
- Xuất Excel — https://openpyxl.readthedocs.io · Xuất PDF — https://docs.reportlab.com
- Đóng gói file chạy — https://pyinstaller.org/en/stable/
- Word mục lục tự động: thẻ **References → Table of Contents**; đánh số hình: **Insert Caption**

### TV2 — Chương lý thuyết

- Silberschatz, chương Deadlocks, **các mục đầu**: mô hình hệ thống, 4 điều kiện Coffman, 4 hướng xử lý
- Bài toán 5 triết gia nằm ở chương **Synchronization** của cùng cuốn sách, không nằm ở chương Deadlocks
- Vẽ hình — https://app.diagrams.net (nhớ lưu cả file nguồn `.drawio` để chứng minh tự vẽ)
- Cách trích dẫn: chọn một chuẩn duy nhất (IEEE hoặc APA) rồi dùng **References → Insert Citation** của Word

### TV3 — Đặc tả thuật toán *(ưu tiên số 1)*

- **Quan trọng nhất, trong repo:** `engine/banker.py` — **mã giả đầy đủ của cả hai thủ tục đã nằm sẵn trong phần chú thích của từng hàm**. Bạn không phải tra sách, chỉ cần viết lại cho đầy đủ và giải thích trong Word
- **Trong repo:** `tests/test_banker.py` — 16 ca kiểm thử với kết quả kỳ vọng cụ thể. Đây chính là những con số bạn phải chạy tay ra được
- Silberschatz, mục **Banker's Algorithm** — phần Safety Algorithm và Resource-Request Algorithm
- Ví dụ chuẩn 5 tiến trình × 3 tài nguyên: `data/vi-du-chuan.json`

### TV4 — Engine

- **Trong repo, theo thứ tự đọc:** `engine/banker_types.py` (hợp đồng dữ liệu) → `engine/banker.py` (mã giả trong chú thích) → `tests/test_banker.py` (đặc tả bạn phải thoả)
- Kiểu dữ liệu dataclass — https://docs.python.org/3/library/dataclasses.html
- **Sao chép sâu** — https://docs.python.org/3/library/copy.html · thiếu kiến thức này là hỏng bước rollback
- Kiểm thử — https://docs.python.org/3/library/unittest.html

### TV5 — Giao diện nhập liệu

- Tài liệu PyQt5 — https://www.riverbankcomputing.com/static/Docs/PyQt5/
- Bảng dữ liệu `QTableWidget` — https://doc.qt.io/qt-5/qtablewidget.html
- Ô nhập số `QSpinBox`, hộp thoại chọn file `QFileDialog` — tra cùng trang doc.qt.io
- Đọc ghi JSON — https://docs.python.org/3/library/json.html
- **Trong repo:** 3 file trong `data/` chính là định dạng bạn phải đọc và ghi. `banker_types.py` **đã có sẵn** `from_json_file()` và `to_json_file()` — đừng viết lại

### TV6 — Giao diện mô phỏng

- Bộ đếm thời gian `QTimer` cho chế độ chạy tự động — https://doc.qt.io/qt-5/qtimer.html
- Tô màu ô bảng: dùng `QTableWidgetItem.setBackground()`
- Thanh trượt tốc độ `QSlider` — https://doc.qt.io/qt-5/qslider.html
- Vẽ biểu đồ — https://matplotlib.org/stable/ (tìm mục nhúng matplotlib vào Qt)
- **Trong repo:** lớp `StepLog` trong `banker_types.py` chính là cấu trúc các cột của bảng nhật ký. Cứ theo đó mà dựng bảng

### TV7 — Chương so sánh

- Silberschatz, mục **Resource-Allocation Graph** — phần lý thuyết đồ thị và phần dùng đồ thị để tránh deadlock (có cạnh nhu cầu nét đứt)
- Kiến thức nền: phát hiện chu trình trong đồ thị có hướng
- Vẽ đồ thị — https://app.diagrams.net · Vẽ biểu đồ số liệu: Excel cũng được, không bắt buộc dùng code
- **Trong repo:** xin TV4 script đo thời gian và TV5 nút sinh dữ liệu ngẫu nhiên. Số liệu phải đo thật

### TV8 — Kiểm thử

- **Trong repo:** `tests/test_banker.py` — 16 ca đã viết sẵn, đọc để học cách viết thêm ca mới
- Thư viện kiểm thử — https://docs.python.org/3/library/unittest.html
- Báo lỗi bằng GitHub Issues — https://docs.github.com/en/issues
- Giá trị kỳ vọng **lấy từ bảng chạy tay của TV3**, không tự suy đoán và không sửa test cho khớp với code

---

## Cấu trúc thư mục

```
engine/    Thuật toán Banker, không phụ thuộc giao diện
gui/       Giao diện phần mềm
tests/     Kiểm thử tự động
data/      Bộ dữ liệu mẫu .json
docs/      Đề bài, kế hoạch, biểu đồ thiết kế
report/    Quyển báo cáo — mỗi chương một thư mục riêng
```

**Quy tắc quan trọng nhất:** mỗi thư mục có đúng một chủ sở hữu, và **chỉ chủ sở hữu được sửa file bên trong**.

File Word là file nhị phân — Git không merge được. Hai người cùng sửa một file `.docx` sẽ tạo ra xung đột không gỡ được, buộc phải bỏ hẳn một bản. Chia thư mục theo người là cách duy nhất để chuyện đó không bao giờ xảy ra.

---

## Bắt đầu làm việc

### Bước 1 — Khai báo danh tính (làm một lần, trên máy của chính mình)

Email phải **trùng với email đăng ký GitHub**, nếu không commit sẽ không gắn được vào tài khoản của bạn và không hiện trong biểu đồ đóng góp — đúng thứ giáo viên nhìn vào để đánh giá.

```bash
git config --global user.name "Họ Tên Thật"
```

```bash
git config --global user.email "email-github-cua-ban@gmail.com"
```

### Bước 2 — Tải repo về máy

```bash
git clone https://github.com/BryannLee202/HDH_De_tai_9_Giai_thuat_Banker.git
```

### Bước 3 — Sang nhánh của mình

Tám nhánh đã được tạo sẵn trên GitHub, nên **không dùng `-b`** — chỉ cần chuyển sang là Git tự nối với nhánh trên mạng:

```bash
git checkout tv4-engine
```

### Bước 4 — Làm việc, rồi lưu lên

```bash
git add . && git commit -m "TV4: cai dat ham kiem_tra_an_toan" && git push
```

### Bước 5 — Tạo pull request

Vào GitHub, bấm **Compare & pull request**, gán TV1 duyệt. **Không ai đẩy thẳng vào `main`.**

---

## Nếu bạn không code (TV2, TV3, TV7)

Không cần dùng dòng lệnh. Chọn một trong hai cách:

- **GitHub Desktop** — cài đặt, đăng nhập, kéo file vào rồi bấm nút. Đơn giản nhất nếu bạn nộp file thường xuyên.
- **Ngay trên web GitHub** — vào đúng thư mục chương của mình, bấm **Add file → Upload files**, kéo file `.docx` vào, gõ mô tả rồi bấm **Commit changes**. Xong.

Cả hai cách đều tính là commit của bạn, miễn là bạn đăng nhập bằng tài khoản của chính mình.

---

## Quy ước commit

Mở đầu bằng mã thành viên, viết không dấu để tránh lỗi phông trên máy khác:

```
TV3: bo sung vi du chay tay 5 vong lap
TV5: chan du lieu khi Allocation vuot qua Max
TV8: them 5 ca kiem thu bien
```

**Mỗi người tối thiểu 5 commit, rải đều 4 tuần.** Commit dồn hết vào đêm trước hạn nộp thì nhìn lịch sử là biết ngay.

---

## Quy tắc chung

- Repo để chế độ **private** trong lúc làm.
- Bật khoá nhánh `main` ở **Settings → Branches** để không ai đẩy thẳng vào.
- **Không commit video demo** — GitHub chặn file trên 100 MB. Để trên Google Drive rồi dán link vào mục dưới đây.
- Họp 2 buổi mỗi tuần, biên bản lưu ở `report/bien-ban-hop/`.
- Hạn nội bộ sớm hơn hạn nộp 3 ngày.

---

## Chạy chương trình

```bash
python -m engine.demo
```

Kết quả mong đợi với bộ dữ liệu chuẩn: trạng thái **an toàn**, chuỗi `<P1, P3, P4, P2, P0>`.

Chạy kiểm thử:

```bash
python -m unittest discover -s tests -v
```

---

## Video demo

*(TV6 dán link Google Drive vào đây)*
