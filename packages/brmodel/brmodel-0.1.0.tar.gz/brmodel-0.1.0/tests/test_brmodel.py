import unittest
from brmodel.cold_recommend import recommend_based_rating
import pandas as pd
import numpy as np
class TestRecommendBasedRating(unittest.TestCase):
    def setUp(self):
        # 准备测试数据
        # self.ratings_data = pd.DataFrame({
        #     'user_id': [1, 1, 2, 2, 3, 3, 2],
        #     'book_id': [101, 102, 101, 103, 102, 104, 105],
        #     'rating': [4.0, 3.0, 5.0, 2.0, 4.0, 3.0, 3.0]
        # })
        self.ratings_data = pd.read_csv('data/review_202503310958.csv')

        
    def test_recommend_normal_case(self):
        # 测试正常情况下的推荐
        result = recommend_based_rating(data=self.ratings_data, target_user_id=4, k=2)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
            

if __name__ == '__main__':
    unittest.main()
