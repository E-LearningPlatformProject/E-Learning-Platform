import unittest
from unittest.mock import patch
from data.models import Section
from services import sections_service


class SectionsService_Sould(unittest.TestCase):

    @patch('services.sections_service.insert_query')
    def test_create(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1 
        mock_section = Section(id=1, title='title', type_file='file', course_id=1, source='source')
        # Act
        sections_service.create(mock_section, 1)
        # Assert
        self.assertEqual(mock_section.id, 1)

    @patch('services.sections_service.read_query')
    def test_get_sections(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'file', 1, 'source')]
        mock_section = Section(id=1, title='title', type_file='file', course_id=1, source='source')
        course_id = 1
        # Act
        result = sections_service.get_sections(course_id)
        # Assert
        self.assertEqual(list(result), [mock_section])

    @patch('services.sections_service.read_query')
    def test_get_by_id(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'file', 1, 'source')]
        mock_section = Section(id=1, title='title', type_file='file', course_id=1, source='source')
        # Act
        section = sections_service.get_by_id(mock_section.id)
        # Assert
        self.assertEqual(section, mock_section)

    @patch('services.sections_service.update_query')
    def test_update(self, mock_update_query):
        # Arrange
        mock_update_query.return_value = 1
        old_info = Section(id=1, title='title', type_file='file', course_id=1, source='source')

        new_info = Section(id=1, title='new_title', type_file='new_file', course_id=1, source='new_source')
        # Act
        result = sections_service.update(old_info, new_info)
        # Assert
        self.assertEqual(result.title, new_info.title)
        self.assertEqual(result.type_file, new_info.type_file)
        self.assertEqual(result.source, new_info.source)

    @patch('services.sections_service.read_query')
    def test_exists(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1,)]
        # Act
        result = sections_service.exists(1)
        # Assert
        self.assertTrue(result)

    @patch('services.sections_service.update_query')
    def test_delete(self, mock_update_query):
        # Arrange
        section_id = 1
        mock_update_query.return_value = 1
        # Act
        sections_service.delete(section_id)
        # Assert
        mock_update_query.assert_called_once_with(
            'DELETE FROM sections WHERE id = ?', (section_id,)
        )
    
    @patch('services.sections_service.update_query')
    def test_delete_by_course_id(self, mock_update_query):
        # Arrange
        course_id = 1
        mock_update_query.return_value = 1
        # Act
        sections_service.delete_by_course_id(course_id)
        # Assert
        mock_update_query.assert_called_once_with(
            'DELETE FROM sections WHERE course_id = ?', (course_id,)
        )