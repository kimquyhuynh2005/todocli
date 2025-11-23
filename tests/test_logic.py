import pytest
from unittest.mock import patch, MagicMock
from src.task_manager import add_task, list_tasks, update_task, delete_task

# --- FIXTURES (Dữ liệu giả lập dùng chung) ---
@pytest.fixture
def mock_storage():
    """Giả lập load_tasks và save_tasks cho mọi bài test"""
    with patch('src.task_manager.load_tasks') as mock_load, \
         patch('src.task_manager.save_tasks') as mock_save:
        yield mock_load, mock_save

@pytest.fixture
def sample_data():
    """Dữ liệu mẫu: 1 task thường, 1 task đã xong, 1 task không có deadline"""
    return [
        {'id': 1, 'title': 'Task A', 'status': 'todo', 'due_to': '2025-01-01'},
        {'id': 2, 'title': 'Task B', 'status': 'done', 'due_to': '2025-02-01'},
        {'id': 3, 'title': 'Task C', 'status': 'todo', 'due_to': None} 
    ]

# --- 1. TEST ADD (THÊM) ---

def test_add_task_empty_list(mock_storage):
    """Edge Case: Thêm task khi chưa có dữ liệu nào (Danh sách rỗng)"""
    mock_load, mock_save = mock_storage
    mock_load.return_value = [] # Giả vờ file rỗng

    add_task("First Task")

    # Kiểm tra: ID phải bắt đầu từ 1
    saved_args = mock_save.call_args[0][0]
    assert len(saved_args) == 1
    assert saved_args[0]['id'] == 1
    assert saved_args[0]['title'] == "First Task"

def test_add_task_increment_id(mock_storage, sample_data):
    """Base Case: Thêm task khi đã có dữ liệu (ID phải tăng lên)"""
    mock_load, mock_save = mock_storage
    mock_load.return_value = sample_data # ID lớn nhất đang là 3

    add_task("Next Task")

    saved_args = mock_save.call_args[0][0]
    # Task mới phải có ID = 3 + 1 = 4
    assert saved_args[-1]['id'] == 4

# --- 2. TEST LIST (XEM & SẮP XẾP) ---

def test_list_tasks_filter(mock_storage, sample_data):
    """Base Case: Lọc theo trạng thái"""
    mock_load, _ = mock_storage
    mock_load.return_value = sample_data

    # Lọc 'done' -> Chỉ lấy task ID 2
    results = list_tasks(status_filter='done')
    assert len(results) == 1
    assert results[0]['id'] == 2

def test_list_tasks_sorting(mock_storage):
    """Edge Case: Kiểm tra logic sắp xếp (None xuống đáy)"""
    mock_load, _ = mock_storage
    # Dữ liệu lộn xộn: Task không hạn (None) đang đứng đầu
    unordered_data = [
        {'id': 1, 'title': 'No Date', 'status': 'todo', 'due_to': None},
        {'id': 2, 'title': 'Has Date', 'status': 'todo', 'due_to': '2025-01-01'}
    ]
    mock_load.return_value = unordered_data

    results = list_tasks()

    # Kỳ vọng: Task có ngày (ID 2) phải lên đầu, Task None (ID 1) xuống dưới
    assert results[0]['id'] == 2 
    assert results[1]['id'] == 1

# --- 3. TEST UPDATE (SỬA) ---

def test_update_task_success(mock_storage, sample_data):
    """Base Case: Cập nhật thành công"""
    mock_load, mock_save = mock_storage
    mock_load.return_value = sample_data

    # Sửa Task 1: Đổi tên và trạng thái
    result = update_task(1, new_status='in-progress', title='New Name')

    assert result is True
    saved_args = mock_save.call_args[0][0]
    # Kiểm tra dữ liệu đã thay đổi chưa
    assert saved_args[0]['status'] == 'in-progress'
    assert saved_args[0]['title'] == 'New Name'

def test_update_task_not_found(mock_storage, sample_data):
    """Edge Case: Cập nhật ID không tồn tại"""
    mock_load, mock_save = mock_storage
    mock_load.return_value = sample_data

    # Cố update ID 999
    result = update_task(999, new_status='done')

    assert result is False
    mock_save.assert_not_called() # Không được gọi hàm lưu

# --- 4. TEST DELETE (XÓA) ---

def test_delete_task_success(mock_storage, sample_data):
    """Base Case: Xóa thành công"""
    mock_load, mock_save = mock_storage
    mock_load.return_value = sample_data

    # Xóa Task 2
    result = delete_task(2)

    assert result is True
    saved_args = mock_save.call_args[0][0]
    assert len(saved_args) == 2 # 3 cái xóa 1 còn 2
    # Kiểm tra ID 2 không còn trong danh sách
    ids = [t['id'] for t in saved_args]
    assert 2 not in ids

def test_delete_task_not_found(mock_storage, sample_data):
    """Edge Case: Xóa ID không tồn tại"""
    mock_load, mock_save = mock_storage
    mock_load.return_value = sample_data

    # Xóa ID 999
    result = delete_task(999)

    assert result is False
    mock_save.assert_not_called() # Không lưu gì cả