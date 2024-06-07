import unittest
from unittest.mock import patch
from data.models import Vote
from services import ratings_service


class RatingsService_Sould(unittest.TestCase):

    @patch('services.ratings_service.insert_query')
    def test_vote(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1
        mock_vote = Vote(course_id=1, rating=5)
        student_id = 1
        # Act
        ratings_service.vote(mock_vote, student_id)
        # Assert
        mock_insert_query.assert_called_once_with(
            'INSERT INTO ratings (courses_id, students_id, rating) VALUES (?, ?, ?)',
            (mock_vote.course_id, student_id, mock_vote.rating))    
    
    @patch('services.ratings_service.read_query')
    def test_check_if_student_had_vote(self, mock_read_query):
        mock_read_query.return_value = [(1, 1)]
        course_id = 1
        student_id = 1
        # Act
        result = ratings_service.check_if_student_had_vote(course_id, student_id)
        # Assert
        self.assertTrue(result)

    @patch('services.ratings_service.read_query')
    def test_average_rating_with_ratings(self, mock_read_query):
        # Arrange
        course_id = 1
        expected_average = 4.5
        mock_read_query.return_value = [(expected_average,)]
        # Act
        result = ratings_service.average_rating(course_id)
        # Assert
        self.assertEqual(result, expected_average)

    @patch('services.ratings_service.update_query')
    def test_delete(self, mock_update_query):
        # Arrange
        course_id = 1
        mock_update_query.return_value = 1
        # Act
        ratings_service.delete(course_id)
        # Assert
        mock_update_query.assert_called_once_with(
            'DELETE FROM ratings WHERE courses_id = ?', (course_id,)
        )