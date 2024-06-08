import unittest
from unittest.mock import patch
from data.models import Teachers, User, TeacherInfo, Course
from services import teachers_service


class TeachersService_Sould(unittest.TestCase):

    @patch('services.teachers_service.update_query')
    def test_change_account_info(self, mock_update_query):
        # Arrange
        mock_update_query.return_value = 1
        old_info = TeacherInfo(
            id=1,
            email='teacher@abc.com',
            password='password',
            role='teacher',
            first_name='FirstName',
            last_name='LastName',
            phone_number='0887301408',
            linked_in_account='OldAccount',
            is_approved=True,
            image='image',)

        new_info = TeacherInfo(
            id=1,
            email='teacher@abc.com',
            password='new_password',
            role='teacher',
            first_name='NewFirstName',
            last_name='NewLastName',
            phone_number='0888888888',
            linked_in_account='NewAccount',
            is_approved=True,
            image='new_image',)
        # Act
        result = teachers_service.change_account_info(old_info, new_info)
        # Assert
        self.assertEqual(result.password, new_info.password)
        self.assertEqual(result.first_name, new_info.first_name)
        self.assertEqual(result.last_name, new_info.last_name)
        self.assertEqual(result.phone_number, new_info.phone_number)
        self.assertEqual(result.linked_in_account, new_info.linked_in_account)
        self.assertEqual(result.image, new_info.image)

    @patch('services.teachers_service.read_query')
    def test_check_if_is_approved_returnsTrue(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1,)]
        mock_teacher = Teachers(id=1, phone_number='0887301408', linked_in_account='GGorge', is_approved=True, users_id=1,
                           first_name='George', last_name='George', image='image')
        # Act
        result = teachers_service.check_if_is_approved(mock_teacher.id)
        # Assert
        self.assertTrue(result)

    @patch('services.teachers_service.read_query')
    def test_check_if_is_approved_returnsFalse(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(0,)]
        mock_teacher = Teachers(id=1, phone_number='0887301408', linked_in_account='GGorge', is_approved=False, users_id=1,
                           first_name='George', last_name='George', image='image')
        # Act
        result = teachers_service.check_if_is_approved(mock_teacher.id)
        # Assert
        self.assertFalse(result)

    @patch('services.teachers_service.read_query')
    def test_get_teacher_email(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [('teacher@abc.com',)]
        mock_user = User(id=1, email='teacher@abc.com', password='password', role='teacher')
        mock_teacher = Teachers(id=1, phone_number='0887301408', linked_in_account='GGorge', is_approved=True, users_id=1,
                           first_name='George', last_name='George', image='image')
        mock_course = Course(id=1, title='title', description='description', level='premium', hidden=False, image='image', author_id=mock_teacher.id, tags=None)
        # Act
        result = teachers_service.get_teacher_email(mock_course.id)
        # Assert
        self.assertEqual(result, mock_user.email)
