import unittest
from unittest.mock import patch
from data.models import StudentInfo, Students, Course
from services import students_service


class StudentsService_Should(unittest.TestCase):

    @patch('services.students_service.update_query')
    def test_change_account_info(self, mock_update_query):
        # Arrange
        mock_update_query.return_value = 1
        old_info = StudentInfo(
            id=1,
            email='teacher@abc.com',
            password='password',
            role='teacher',
            first_name='FirstName',
            last_name='LastName')

        new_info = StudentInfo(
            id=1,
            email='teacher@abc.com',
            password='new_password',
            role='teacher',
            first_name='NewFirstName',
            last_name='NewLastName')
        # Act
        result = students_service.change_account_info(old_info, new_info)
        # Assert
        self.assertEqual(result.password, new_info.password)
        self.assertEqual(result.first_name, new_info.first_name)
        self.assertEqual(result.last_name, new_info.last_name)

    @patch('services.students_service.insert_query')
    def test_enroll_student(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1
        mock_student = Students(id=1, users_id=1, first_name='Peter', last_name='Peter')
        mock_course = Course(id=1, title='title', description='description', level='premium', hidden=False,
                             author_id=mock_student.id, tags=None)
        # Act
        students_service.enroll_student(mock_course.id, mock_student.id)
        # Assert
        self.assertEqual(mock_student.id, 1)

    @patch('services.students_service.read_query')
    def test_check_if_student_is_enrolled(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 1)]
        mock_student = Students(id=1, users_id=1, first_name='Peter', last_name='Peter')
        mock_course = Course(id=1, title='title', description='description', level='premium', hidden=False,
                             author_id=mock_student.id, tags=None)
        # Act
        students_service.check_if_student_is_enrolled(mock_course.id, mock_student.id)
        # Assert
        self.assertEqual(mock_student.id, 1)
        self.assertEqual(mock_course.id, 1)
