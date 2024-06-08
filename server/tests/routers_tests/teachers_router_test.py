import unittest
from unittest.mock import Mock, patch
from common.responses import Unauthorized, BadRequest, Forbidden
from data.models import Role
from routers import teachers as teachers_router


mock_teachers_service = Mock()


teachers_router.teachers_service = mock_teachers_service


def fake_teacher():
    teacher = Mock()
    teacher.role = Role.TEACHER
    teacher.email = 'teacher@abc.com'
    teacher.id = 1
    return teacher

class TeachersRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        
        mock_teachers_service.reset_mock()
        

    def test_update_teacher_info_when_no_token(self):
        # Act
        result = teachers_router.update_teacher_info(teacher=Mock(), x_token=None)
        # Assert
        self.assertIsInstance(result, Unauthorized)

    def test_update_teacher_info_when_valid_token(self):
        with patch('routers.teachers.get_user_or_raise_401') as get_user_func:
            # Arrange
            teacher_info = Mock()
            existing_teacher = fake_teacher()
            get_user_func.return_value = existing_teacher
            mock_teachers_service.change_account_info.return_value = 'Success'
            # Act
            result = teachers_router.update_teacher_info(teacher=teacher_info, x_token='valid_token')
            # Assert
            mock_teachers_service.change_account_info.assert_called_with(existing_teacher, teacher_info)
            self.assertEqual(result, 'Success')
