# ✅ Todo CLI - Smart Task Manager

Một ứng dụng quản lý công việc dòng lệnh (Command Line Interface) mạnh mẽ, hiện đại, được xây dựng bằng Python.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)

## ✨ Tính năng nổi bật

* **🚀 Nhanh & Nhẹ:** Hoạt động tức thì trên Terminal.
* **🎨 Giao diện đẹp:** Sử dụng thư viện `Rich` để hiển thị bảng màu, icon trạng thái và cảnh báo.
* **🧠 Thông minh:**
    * Tự động tính toán thời gian còn lại (`Remaining Time`).
    * Cảnh báo màu đỏ khi quá hạn (`Overdue`).
    * Sắp xếp thông minh: Task gấp xếp trước, task không deadline xếp sau.
* **⚡ Mạnh mẽ:**
    * Hỗ trợ lệnh tắt `todo` cài sâu vào hệ thống.
    * Cập nhật và Xóa hàng loạt (Batch Operations).

## 🛠️ Cài đặt

1.  **Clone dự án:**
    ```bash
    git clone https://github.com/kimquyhuynh2005/todo-cli.git
    cd todo-cli
    ```

2.  **Tạo môi trường ảo (Khuyên dùng):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Cài đặt ứng dụng:**
    ```bash
    pip install -e .
    ```

## 📖 Hướng dẫn sử dụng

| Hành động | Câu lệnh mẫu |
| :--- | :--- |
| **Thêm mới** | `todo add "Học Python" --due 2025-12-30` |
| **Xem danh sách** | `todo list` (hoặc `todo ls`) |
| **Lọc trạng thái** | `todo list --status todo` |
| **Cập nhật** | `todo update 1 --status done` |
| **Xóa** | `todo delete 1` (hoặc `todo del all`) |

## 🧪 Chạy Test
Dự án được kiểm thử tự động bằng **Pytest**. Để chạy test:
```bash
pip install pytest
pytest tests/