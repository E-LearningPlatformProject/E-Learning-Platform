import unittest
from unittest.mock import patch
from data.models import Tag, Course
from services import tags_service


class TagsService_Sould(unittest.TestCase):

    @patch('services.tags_service.read_query')
    def test_get_tags_by_course_id(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title')]
        mock_tag = Tag(id=1, title='title')
        mock_course = Course(id=1, title='title', description='description', level='premium', hidden=False,
                            image='image', author_id=1, tags=None)
        # Act
        tags_service.get_tags_by_course_id(mock_course.id)
        # Assert
        self.assertEqual(mock_tag.title, 'title')

    @patch('services.tags_service.read_query')
    def test_get_tags_by_name(self, mock_read_query):
        # Arrange
        tags = ['tag1']
        mock_read_query.return_value = [(1,)]
        # Act
        result = tags_service.get_tags_by_name(tags)
        # Assert
        self.assertEqual(result, [(1,)])

    @patch('services.tags_service.update_query')
    def test_delete(self, mock_update_query):
        # Arrange
        course_id = 1
        mock_update_query.return_value = 1
        # Act
        tags_service.delete(course_id)
        # Assert
        mock_update_query.assert_called_once_with(
            'DELETE FROM courses_has_tags WHERE course_id = ?', (course_id,)
        )