import unittest
from unittest.mock import patch
from data.models import CreateCourse, Course, CoursesTagsResponeModel
from services import courses_service


class CoursesService_Sould(unittest.TestCase):

    @patch('services.courses_service.read_query')
    def test_all_non_premium(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'description', 'non_premium', None)]
        mock_course = CoursesTagsResponeModel(id=1, title='title', description='description',
                                                  level='non_premium', tags=None )
        # Act
        course = courses_service.all_non_premium()
        # Assert
        self.assertEqual([mock_course], list(course))

    @patch('services.courses_service.read_query')
    def test_all_non_premium_with_search(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(2, 'title2', 'description2', 'non_premium', None)]
        mock_course1 = CoursesTagsResponeModel(id=1, title='title', description='description',
                                                  level='non_premium', tags=None)
        mock_course2 = CoursesTagsResponeModel(id=2, title='title2', description='description2',
                                               level='non_premium', tags=None)
        # Act
        course = courses_service.all_non_premium('title2')
        # Assert
        self.assertEqual([mock_course2], list(course))

    @patch('services.courses_service.read_query')
    def test_all_non_hidden(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'description', 'non_premium', None)]
        mock_course = CoursesTagsResponeModel(id=1, title='title', description='description',
                                              level='non_premium', tags=None)
        # Act
        course = courses_service.all_non_hidden()
        # Assert
        self.assertEqual([mock_course], list(course))

    @patch('services.courses_service.read_query')
    def test_all_non_hidden_with_search(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(2, 'title2', 'description2', 'non_premium', None)]
        mock_course1 = CoursesTagsResponeModel(id=1, title='title', description='description',
                                               level='non_premium', tags=None)
        mock_course2 = CoursesTagsResponeModel(id=2, title='title2', description='description2',
                                               level='non_premium', tags=None)
        # Act
        course = courses_service.all_non_hidden('title2')
        # Assert
        self.assertEqual([mock_course2], list(course))

    @patch('services.courses_service.read_query')
    def test_all(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'description', 'non_premium', None)]
        mock_course = CoursesTagsResponeModel(id=1, title='title', description='description',
                                              level='non_premium', tags=None)
        # Act
        course = courses_service.all()
        # Assert
        self.assertEqual([mock_course], list(course))

    @patch('services.courses_service.read_query')
    def test_all_with_search(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(2, 'title2', 'description2', 'non_premium', None)]
        mock_course1 = CoursesTagsResponeModel(id=1, title='title', description='description',
                                               level='non_premium', tags=None)
        mock_course2 = CoursesTagsResponeModel(id=2, title='title2', description='description2',
                                               level='non_premium', tags=None)
        # Act
        course = courses_service.all('title2')
        # Assert
        self.assertEqual([mock_course2], list(course))

    @patch('services.courses_service.read_query')
    def test_t_private(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'description', 'non_premium', None)]
        mock_course = CoursesTagsResponeModel(id=1, title='title', description='description',
                                              level='non_premium', tags=None)
        # Act
        course = courses_service.t_private(1)
        # Assert
        self.assertEqual([mock_course], list(course))

    @patch('services.courses_service.insert_query')
    @patch('services.courses_service.tags_service.get_tags_by_name')
    @patch('services.courses_service.tags_service.create')
    def test_create_with_tags(self, mock_create_tags, mock_get_tags_by_name, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1  
        mock_get_tags_by_name.return_value = [(1,), (2,)] 
        mock_course = CreateCourse(id=1, title='title', description='description', level='non_premium', tags='tag1,tag2')
        # Act
        course = courses_service.create(mock_course, 1)
        # Assert
        self.assertEqual(course.id, 1)

    @patch('services.courses_service.update_query')
    def test_update(self, mock_update_query):
        # Arrange
        mock_update_query.return_value = 1
        old_info = Course(
            id=1,
            title='title',
            description='description',
            role='teacher',
            level='non_private',
            hidden=False,
            author_id=1,
            tags=None)

        new_info = Course(
            id=1,
            title='new_title',
            description='new_description',
            role='teacher',
            level='non_private',
            hidden=True,
            author_id=1,
            tags='tag1')
        # Act
        result = courses_service.update(old_info, new_info)
        # Assert
        self.assertEqual(result.title, new_info.title)
        self.assertEqual(result.description, new_info.description)
        self.assertEqual(result.hidden, new_info.hidden)
        self.assertEqual(result.tags, new_info.tags)

    @patch('services.courses_service.read_query')
    def test_exists(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1,)]
        # Act
        result = courses_service.exists(1)
        # Assert
        self.assertTrue(result)

    @patch('services.courses_service.read_query')
    def test_get_by_id(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'title', 'description', 'non_private', False, 1, 'tag1,tag2')]

        expected_course = Course(
            id=1,
            title='title',
            description='description',
            level='non_private',
            hidden=False,
            author_id=1,
            tags='tag1,tag2')
        # Act
        course = courses_service.get_by_id(expected_course.id)
        # Assert
        self.assertEqual(course, expected_course)


    @patch('services.courses_service.read_query')
    def test_course_authorID(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1,)]
        mock_course = Course(
            id=1,
            title='title',
            description='description',
            level='non_private',
            hidden=False,
            author_id=1,
            tags='tag1,tag2')
        # Act
        result = courses_service.get_course_authorID(mock_course.author_id)
        # Assert
        self.assertEqual(result, 1)

    @patch('services.courses_service.read_query')
    def test_is_hidden(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1,)]
        mock_course = Course(
            id=1,
            title='title',
            description='description',
            level='non_private',
            hidden=True,
            author_id=1,
            tags='tag1,tag2')
        # Act
        result = courses_service.is_hidden(mock_course.id)
        # Assert
        self.assertTrue(result)

    @patch('services.courses_service.update_query')
    def test_delete(self, mock_update_query):
        # Arrange
        course_id = 1
        mock_update_query.return_value = 1
        # Act
        courses_service.delete(course_id)
        # Assert
        mock_update_query.assert_called_once_with(
            'DELETE FROM courses WHERE id = ?', (course_id,)
        )