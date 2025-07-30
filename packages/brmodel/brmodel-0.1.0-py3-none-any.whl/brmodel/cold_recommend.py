from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# 构建图书id和图书名称的映射
# book_id_map = {}
# for d in read_from_excel_allcols('data/豆瓣书籍汇总.xlsx', [0], 1):
#     book_id = d[0]
#     book_name = d[1]
#     book_id_map[int(book_id)] = book_name
#     rating = d[6]
# user_rating_map = collections.defaultdict(list)
# book_comment_map = collections.defaultdict(list)
# for d in read_csv('data/review_202503310958.csv',True):
#     user_id = int(d['user_id'])
#     book_id = int(d['book_id'])
#     rating = float(d['rating'])
#     comment = d['comment']
#     user_rating_map[user_id].append({book_id_map[book_id]:rating})
#     book_comment_map[book_id].append(comment)
def recommend_based_rating(target_user_id:int, data: pd.DataFrame, k:int):
    # 构建用户-书籍评分矩阵
    ratings_matrix = data.pivot_table(index='user_id', columns='book_id', values='rating')

    # 计算用户之间的相似度
    user_similarity = cosine_similarity(ratings_matrix.fillna(0))

    # 选择目标用户
    # target_user_id = 903

    # 找到与目标用户最相似的K个用户
    # k = 5
    similar_users = ratings_matrix.index[user_similarity[target_user_id].argsort()[-k - 1:-1]].tolist()

    # 获取这些相似用户喜欢的书籍及其权重
    book_weights = {}
    for similar_user in similar_users:
        # 获取相似用户的评分
        user_ratings = ratings_matrix.loc[similar_user]
        # 获取相似用户在相似度矩阵中的索引
        similar_user_idx = ratings_matrix.index.get_loc(similar_user)
        similarity_score = user_similarity[ratings_matrix.index.get_loc(target_user_id)][similar_user_idx]  # 相似度分数
        for book_id, rating in user_ratings.items():
            if pd.notnull(rating):  # 只考虑有评分的书籍
                if book_id not in book_weights:
                    book_weights[book_id] = 0
                book_weights[book_id] += rating * similarity_score  # 加权评分

    # 去除目标用户已经评分的书籍
    already_rated_books = ratings_matrix.columns[ratings_matrix.loc[target_user_id] > 0]
    recommended_books = {book: weight for book, weight in book_weights.items() if book not in already_rated_books}

    # 按权重排序并返回 Top 5 推荐书籍
    top5_recommendations = sorted(recommended_books.items(), key=lambda x: x[1], reverse=True)[:k]
    top5_books = [book for book, weight in top5_recommendations]
    # print(f'用户{str(target_user_id)}的历史评分数据：')
    # for i in  user_rating_map[target_user_id]:
    #     print(i)
    return top5_books
    # print("推荐给目标用户的 Top 5 书籍:", [book_id_map[i] for i in top5_books])
def recommend_based_comment():
    # 假设我们已经从图片中加载了数据并将其转换为了包含'书名', '评论'的数据框
    data = pd.read_csv('data/review_202503310958.csv')
    data = data.groupby('book_id')['comment'].apply(lambda x: ' '.join(x)).reset_index()  # 把评价拼起来

    # 使用TF-IDF向量化评论
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(data['comment'])

    # 计算书籍间的相似度 基于文字评价去计算
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_recommendations(title, cosine_sim=cosine_sim):
        # 获取目标书籍的索引
        idx = data[data['book_id'] == title].index[0]

        # 获取所有书籍与该书籍的相似度分数
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 对相似度分数排序
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 排除目标书籍本身
        sim_scores = [score for score in sim_scores if score[0] != idx]

        # 获取前K个最相似书籍的索引
        sim_scores = sim_scores[:100]  # 取前10个

        # 提取书籍索引
        book_indices = [i[0] for i in sim_scores]

        # 返回推荐书籍列表（去重并返回前5本）
        return data['book_id'].iloc[book_indices].unique()[:5]

    book_id = 1000810
    # 示例调用
    print(f'图书{book_id_map[book_id]}的相关评论为：')
    for i in book_comment_map[book_id]:
        print(i)
    print([book_id_map[id] for id in get_recommendations(book_id)])

if __name__ == '__main__':
    res = recommend_based_rating(target_user_id=903, data=pd.DataFrame(), k=5)
    print(res)
    # print('-----------------------------------------------------------------')
    # recommend_based_comment()

