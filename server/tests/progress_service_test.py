import unittest
from unittest.mock import patch
from services import progress_service


class ProgressService_Sould(unittest.TestCase):

    @patch('services.progress_service.read_query')    
    def test_progress(self, mock_read_query):
        # Arrange
        student_id = 1
        course_id = 1
        expected_progress = 75
        mock_read_query.return_value = [(expected_progress,)]
        
        # Act
        result = progress_service.progress(student_id, course_id)
        
        # Assert
        self.assertEqual(result, expected_progress)

    @patch('services.progress_service.update_query')
    def test_delete(self, mock_update_query):
        # Arrange
        section_id = 1
        mock_update_query.return_value = 1
        # Act
        progress_service.delete(section_id)
        # Assert
        mock_update_query.assert_called_once_with('DELETE FROM progress WHERE sections_id = ?', (section_id,))

    @patch('services.progress_service.update_query')
    def test_delete_by_course(self, mock_update_query):
        # Arrange
        course_id = 1
        mock_update_query.return_value = 1
        # Act
        progress_service.delete_by_course_id(course_id)
        # Assert
        mock_update_query.assert_called_once_with('''
                DELETE p
                FROM progress p
                JOIN sections s ON p.sections_id = s.id
                WHERE s.course_id = ?;
            ''', (course_id,))