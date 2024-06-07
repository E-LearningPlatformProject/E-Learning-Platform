import unittest
from unittest.mock import patch, MagicMock
from data.models import User
from services import users_service


class UsersService_Should(unittest.TestCase):

    @patch('services.users_service.read_query')
    def test_find_by_email(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'email@abc.com', 'password', 'teacher')]
        # Act
        user = users_service.find_by_email('email@abc.com')
        # Assert
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'email@abc.com')

    @patch('services.users_service.read_query')
    def test_find_student_info(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'student@abc.com', 'password', 'student', 'Peter', 'Peter')]
        # Act
        student = users_service.find_student_info('student@abc.com')
        # Assert
        self.assertEqual(student.email, 'student@abc.com')

    @patch('services.users_service.read_query')
    def test_find_teacher_info(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'teacher@abc.com', 'password', 'teacher', 'George', 'George', '0887301408',
                                         'GGeorge', 'true')]
        # Act
        teacher = users_service.find_teacher_info('teacher@abc.com')
        # Assert
        self.assertEqual(teacher.email, 'teacher@abc.com')

    @patch('services.users_service._hash_password')
    @patch('services.users_service.find_by_email')
    def test_try_login_successful(self, mock_find_by_email, mock_hash_password):
        # Arrange
        email = 'student@abc.com'
        password = 'password'
        hashed_password = 'hashed_password'

        mock_user = User(id=1, email=email, password=hashed_password, role='student')
        mock_find_by_email.return_value = mock_user
        mock_hash_password.return_value = hashed_password
        # Act
        result = users_service.try_login(email, password)
        # Assert
        self.assertEqual(result.email, email)

    @patch('services.users_service.insert_query')
    def test_create_student(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1
        # Act
        user = users_service.create_student('student@abc.com', 'password', 'Peter', 'Peter')
        # Assert
        self.assertEqual(user.email, 'student@abc.com')

    @patch('services.users_service.insert_query')
    def test_create_teacher(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1
        # Act
        user = users_service.create_teacher('teacher@abc.com', 'password', 'George', 'George', "0887301408", 'GGeorge')
        # Assert
        self.assertEqual(user.email, 'teacher@abc.com')

    @patch('services.users_service.jwt.encode')
    def test_create_token(self, mock_jwt_encode):
        # Arrange
        mock_jwt_encode.return_value = 'encoded_token'
        user = User(id=1, email='name', password='password', role='user')
        # Act
        token = users_service.create_token(user)
        # Assert
        self.assertEqual(token, 'encoded_token')

    @patch('services.users_service.jwt.decode')
    def test_is_authenticated(self, mock_jwt_decode):
        # Arrange
        mock_jwt_decode.return_value = {'id': 1, 'email': 'email@abc.com'}
        # Act
        mock_read_query = MagicMock()
        mock_read_query.return_value = [(1,)]
        # Assert
        with patch('services.users_service.read_query', mock_read_query):
            self.assertTrue(users_service.is_authenticated('valid_token'))
