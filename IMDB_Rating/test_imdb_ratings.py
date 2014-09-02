"""
Run tests for imdb_ratings
"""
import unittest
import imdb_ratings
from imdb_ratings import GroupMovieByElements,condition


class TestSequenceFunctions(unittest.TestCase):
    """Run tests for imbd_ratings"""
    def setUp(self):
    	pass

    def test_movie_meets_condition(self):
        """Test if a movie meets the given condition"""
        temp_movie = '0000000124  939692   8.7  Inception (2010)'
        movie = GroupMovieByElements(temp_movie)
        assert condition(movie) is True

        '''
        for movie in mlist:
        	assertGreater(movie.rating,8.0)
        	assertGreaterEqual(movie.votes,1000)
        '''

    def test_movie_not_meet_condition(self):
        """Test if a movie does not meet the given condition"""
        temp_movie = '0000000125  1180295   9.2  The Shawshank Redemption (1994)'
        movie = GroupMovieByElements(temp_movie)
        assert condition(movie) is False

if __name__ == '__main__':
    unittest.main()
