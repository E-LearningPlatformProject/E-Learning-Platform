import unittest
from unittest.mock import Mock, patch
from common.responses import Unauthorized, BadRequest, Forbidden
from data.models import Role
from routers import students as students_router


mock_students_service = Mock()
mock_courses_service = Mock()
mock_teachers_service = Mock()
mock_progress_service = Mock()
mock_ratings_service = Mock()

students_router.students_service = mock_students_service
students_router.courses_service = mock_courses_service
students_router.teachers_service = mock_teachers_service
students_router.progress_service = mock_progress_service
students_router.ratings_service = mock_ratings_service

def fake_student():
    student = Mock()
    student.role = Role.STUDENT
    student.email = 'student@abc.com'
    student.id = 1
    return student

class StudentsRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_students_service.reset_mock()
        mock_courses_service.reset_mock()
        mock_teachers_service.reset_mock()
        mock_progress_service.reset_mock()
        mock_ratings_service.reset_mock()

    def test_update_student_info_when_no_token(self):
        # Act
        result = students_router.update_student_info(student=Mock(), x_token=None)
        # Assert
        self.assertIsInstance(result, Unauthorized)

    def test_update_student_info_when_valid_token(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            student_info = Mock()
            existing_student = fake_student()
            get_user_func.return_value = existing_student
            mock_students_service.change_account_info.return_value = 'Success'
            # Act
            result = students_router.update_student_info(student=student_info, x_token='valid_token')
            # Assert
            mock_students_service.change_account_info.assert_called_with(existing_student, student_info)
            self.assertEqual(result, 'Success')

    def test_enroll_student_when_no_token(self):
        # Act
        result = students_router.enroll_student_into_course(course_id=1, x_token=None)
        # Assert
        self.assertIsInstance(result, Unauthorized)

    def test_enroll_student_when_course_not_exists(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            get_user_func.return_value = fake_student()
            mock_courses_service.exists.return_value = False
            # Act
            result = students_router.enroll_student_into_course(course_id=1, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, BadRequest)

    def test_enroll_student_when_user_not_student(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = Mock()
            user.role = Role.TEACHER
            get_user_func.return_value = user
            mock_courses_service.exists.return_value = True
            # Act
            result = students_router.enroll_student_into_course(course_id=1, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, Forbidden)

    def test_get_progress_when_no_token(self):
        # Act
        result = students_router.get_progress(course_id=1, x_token=None)
        # Assert
        self.assertIsInstance(result, Unauthorized)

    def test_get_progress_when_course_not_exists(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            get_user_func.return_value = fake_student()
            mock_courses_service.exists.return_value = False
            # Act
            result = students_router.get_progress(course_id=1, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, BadRequest)

    def test_get_progress_when_user_not_student(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = Mock()
            user.role = Role.TEACHER
            get_user_func.return_value = user
            mock_courses_service.exists.return_value = True
            # Act
            result = students_router.get_progress(course_id=1, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, Forbidden)

    def test_get_progress_when_not_enrolled(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            student = fake_student()
            get_user_func.return_value = student
            mock_courses_service.exists.return_value = True
            mock_students_service.check_if_student_is_enrolled.return_value = False
            # Act
            result = students_router.get_progress(course_id=1, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, Unauthorized)

    def test_get_progress_when_valid(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            student = fake_student()
            get_user_func.return_value = student
            mock_courses_service.exists.return_value = True
            mock_students_service.check_if_student_is_enrolled.return_value = True
            mock_progress_service.progress.return_value = 75
            # Act
            result = students_router.get_progress(course_id=1, x_token='valid_token')
            # Assert
            self.assertEqual(result, 'Your progress is 75% for Course with ID: 1')

    def test_vote_when_no_token(self):
        # Act
        result = students_router.vote(vote=Mock(), x_token=None)
        # Assert
        self.assertIsInstance(result, Unauthorized)

    def test_vote_when_course_not_exists(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            get_user_func.return_value = fake_student()
            mock_courses_service.exists.return_value = False
            vote = Mock()
            vote.course_id = 1
            # Act
            result = students_router.vote(vote=vote, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, BadRequest)

    def test_vote_when_user_not_student(self):
        with patch('routers.students.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = Mock()
            user.role = Role.TEACHER
            get_user_func.return_value = user
            mock_courses_service.exists.return_value = True
            vote = Mock()
            vote.course_id = 1
            vote.rating = 5
            # Act
            result = students_router.vote(vote=vote, x_token='valid_token')
            # Assert
            self.assertIsInstance(result, Forbidden)


