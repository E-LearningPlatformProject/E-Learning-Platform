import unittest
from unittest.mock import patch, Mock
from data.models import Role, Section
from routers import sections as section_router

mock_courses_service = Mock()
mock_sections_service = Mock()
mock_progress_service = Mock()
mock_students_service = Mock()

section_router.courses_service = mock_courses_service
section_router.sections_service = mock_sections_service
section_router.progress_service = mock_progress_service
section_router.students_service = mock_students_service

def fake_user(role=Role.STUDENT, user_id=1):
    user = Mock()
    user.role = role
    user.id = user_id
    return user

class SectionRouterTests(unittest.TestCase):

    def setUp(self):
        mock_courses_service.reset_mock()
        mock_sections_service.reset_mock()
        mock_progress_service.reset_mock()
        mock_students_service.reset_mock()

    def test_get_section_unauthorized(self):
        # Act
        result = section_router.get_section(section_id=1, x_token=None)
        # Assert
        self.assertEqual(result.status_code, 401)

    def test_get_section_when_valid(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user()
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = Section(
                id=1,
                course_id=1,
                title="Test Section",
                type_file="pdf",
                source="test_source")
            mock_courses_service.is_hidden.return_value = False
            mock_students_service.check_if_student_is_enrolled.return_value = True
            # Act
            result = section_router.get_section(section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            mock_courses_service.is_hidden.assert_called_with(1)
            mock_students_service.check_if_student_is_enrolled.assert_called_with(1, 1)
            mock_progress_service.create.assert_called_with(1, 1)
            self.assertEqual(result, Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source"))

    def test_get_section_not_found(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user()
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = None
            # Act
            result = section_router.get_section(section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            self.assertEqual(result.status_code, 400)

    def test_get_section_forbidden(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user()
            get_user_func.return_value = user
            mock_courses_service.is_hidden.return_value = True
            mock_sections_service.get_by_id.return_value = Section(
                id=1,
                course_id=1,
                title="Test Section",
                type_file="pdf",
                source="test_source")
            # Act
            result = section_router.get_section(section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            mock_courses_service.is_hidden.assert_called_with(1)
            self.assertEqual(result.status_code, 403)

    def test_create_section_when_valid(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.TEACHER)
            get_user_func.return_value = user
            mock_courses_service.exists.return_value = True
            mock_courses_service.get_course_authorID.return_value = user.id
            mock_sections_service.create.return_value = Section(id=1,
                                                                course_id=1,
                                                                title="Test Section",
                                                                type_file="pdf",
                                                                source="test_source")

            section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
            # Act
            result = section_router.create_section(section=section, course_id=1, x_token='valid_token')
            # Assert
            mock_courses_service.exists.assert_called_with(1)
            mock_courses_service.get_course_authorID.assert_called_with(1)
            mock_sections_service.create.assert_called_with(section, 1)
            self.assertEqual(result, Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source"))

    def test_create_section_unauthorized(self):
        # Act
        mock_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
        result = section_router.create_section(section=mock_section, course_id=1, x_token=None)
        # Assert
        self.assertEqual(result.status_code, 401)

    def test_create_section_course_not_exists(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.TEACHER)
            get_user_func.return_value = user
            mock_courses_service.exists.return_value = False
            # Act
            mock_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
            result = section_router.create_section(section=mock_section, course_id=1, x_token='valid_token')
            # Assert
            mock_courses_service.exists.assert_called_with(1)
            self.assertEqual(result.status_code, 400)

    def test_create_section_forbidden(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.STUDENT)
            get_user_func.return_value = user
            mock_courses_service.exists.return_value = True
            # Act
            mock_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
            result = section_router.create_section(section=mock_section, course_id=1, x_token='valid_token')
            # Assert
            mock_courses_service.exists.assert_called_with(1)
            self.assertEqual(result.status_code, 403)

    def test_update_section_when_valid(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.TEACHER)
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = Section(id=1,
                                                                course_id=1,
                                                                title="Test Section",
                                                                type_file="pdf",
                                                                source="test_source")
            mock_courses_service.get_course_authorID.return_value = user.id
            mock_sections_service.update.return_value = Section(id=1,
                                                                course_id=1,
                                                                title="Test Section",
                                                                type_file="pdf",
                                                                source="test_source")

            new_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
            # Act
            result = section_router.update_section(new_section=new_section, section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            mock_courses_service.get_course_authorID.assert_called_with(1)
            mock_sections_service.update.assert_called_with(Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source"), new_section)
            self.assertEqual(result, Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source"))

    def test_update_section_unauthorized(self):
        # Act
        mock_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
        result = section_router.update_section(new_section=mock_section, section_id=1, x_token=None)
        # Assert
        self.assertEqual(result.status_code, 401)

    def test_update_section_not_found(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.TEACHER)
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = None
            # Act
            mock_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
            result = section_router.update_section(new_section=mock_section, section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            self.assertEqual(result.status_code, 400)

    def test_update_section_forbidden(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.STUDENT)
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = Section(id=1,
                                                                course_id=1,
                                                                title="Test Section",
                                                                type_file="pdf",
                                                                source="test_source")
            # Act
            mock_section = Section(id=1, course_id=1, title="Test Section", type_file="pdf", source="test_source")
            result = section_router.update_section(new_section=mock_section, section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            self.assertEqual(result.status_code, 403)

    def test_remove_section_when_valid(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.TEACHER)
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = Section(id=1,
                                                                    course_id=1,
                                                                    title="Test Section",
                                                                    type_file="pdf",
                                                                    source="test_source")
            mock_courses_service.get_course_authorID.return_value = user.id
            mock_progress_service.delete.return_value = None
            mock_sections_service.delete.return_value = None
            # Act
            result = section_router.remove_section(section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            mock_courses_service.get_course_authorID.assert_called_with(1)
            mock_progress_service.delete.assert_called_with(1)
            mock_sections_service.delete.assert_called_with(1)
            self.assertEqual(result.status_code, 200)

    def test_remove_section_unauthorized(self):
        # Act
        result = section_router.remove_section(section_id=1, x_token=None)
        # Assert
        self.assertEqual(result.status_code, 401)

    def test_remove_section_forbidden(self):
        with patch('routers.sections.get_user_or_raise_401') as get_user_func:
            # Arrange
            user = fake_user(role=Role.STUDENT)
            get_user_func.return_value = user
            mock_sections_service.get_by_id.return_value = Section(id=1,
                                                                course_id=1,
                                                                title="Test Section",
                                                                type_file="pdf",
                                                                source="test_source")
            # Act
            result = section_router.remove_section(section_id=1, x_token='valid_token')
            # Assert
            mock_sections_service.get_by_id.assert_called_with(1)
            self.assertEqual(result.status_code, 403)