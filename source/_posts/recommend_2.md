---
title: 开源推荐系统
date: 2019-01-01 00:00
tags: recommend
categories: 基础技术
---

# 开源推荐系统

## LightFM

LightFM是Python实现的推荐系统，综合了协同推荐和内容推荐。

[参考文档](https://lyst.github.io/lightfm/docs/quickstart.html)

[电影推荐示例](https://github.com/amkurian/movie-recommendation-system)


[模型:](https://lyst.github.io/lightfm/docs/lightfm.html)

```
class lightfm.LightFM(no_components=10, 
                        k=5, 
                        n=10, 
                        learning_schedule=’adagrad’, 
                        loss=’logistic’, 
                        learning_rate=0.05, 
                        rho=0.95, 
                        epsilon=1e-06, 
                        item_alpha=0.0, 
                        user_alpha=0.0,
                        max_sampled=10, 
                        random_state=None)
```

用法：

```
    data = load_data()
    
    # User to Item
    model = LightFM(loss='warp')
    model.fit(interactions=data["score_matrix"], item_features=data["item_feature_matrix"], epochs=10, num_threads=2,
              verbose=True)
    user_random_index = np.random.randint(low=0, high=data["user_count"], size=20)
    user_item_recommendation(model, data, user_random_index)

    # Item to Item
    model_item = LightFM(loss='warp')
    model_item.fit(interactions=data["score_matrix"], epochs=10, num_threads=2, verbose=True)
    item_random_index = np.random.randint(low=0, high=data["book_count"], size=20)
    item_item_recommendation(model_item, item_labels=data["book_labels"], item_index_list=item_random_index)
```



## [Crab](http://muricoca.github.io/crab/)

Crab - scikits.recommender: Recommender systems in Python

Crab as known as scikits.recommender is a Python framework for building recommender engines integrated with the world of scientific Python packages (numpy, scipy, matplotlib).

The engine aims to provide a rich set of components from which you can construct a customized recommender system from a set of algorithms and be usable in various contexts: ** science and engineering ** .

Features:	
Recommender Algorithms: User-Based Filtering and Item-Based Filtering
Work in progress: Slope One, SVD, Evaluation of Recommenders.
Planed: Sparse Matrices, REST API’s.

[示例文档](http://muricoca.github.io/crab/tutorial.html#introducing-recommendation-engines)

```
>>> from scikits.crab.models import MatrixPreferenceDataModel
>>> #Build the model
>>> model = MatrixPreferenceDataModel(movies.data)
>>>
>>> from scikits.crab.metrics import pearson_correlation
>>> from scikits.crab.similarities import UserSimilarity
>>> #Build the similarity
>>> similarity = UserSimilarity(model, pearson_correlation)
>>>
>>> from crab.recommenders.knn import UserBasedRecommender
>>> #Build the User based recommender
>>> recommender = UserBasedRecommender(model, similarity, with_preference=True)
>>> #Recommend items for the user 5 (Toby)
>>> recommender.recommend(5)
[(5, 3.3477895267131013), (1, 2.8572508984333034), (6, 2.4473604699719846)]
```

## Lenskit

LensKit是一套Java实现的推荐系统算法集合，支持包括KNN，FunkSVD和SlopeOne多种推荐算法。

[web site](http://lenskit.org)

[wiki](http://github.com/lenskit/lenskit/wiki/)

[Getting Started](http://lenskit.org/documentation/basics/getting-started/)


## [Oryx 2](http://oryx.io/)

Oryx 2 is a realization of the lambda architecture built on Apache Spark and Apache Kafka, but with specialization for real-time large scale machine learning. It is a framework for building applications, but also includes packaged, end-to-end applications for collaborative filtering, classification, regression and clustering.

![](http://oryx.io/img/Architecture.png)

Source [https://github.com/OryxProject/oryx]()

--- 

# 专题文章

[推荐系统 ](/recommend_0)

[1、推荐系统概述：策略，架构，数据，效果评估](/recommend_1)

[2、开源推荐系统](/recommend_2)

[3、LightFM算法](/recommend_3)

[4、小说推荐系统实战](/recommend_4)

[5、前端交互](/recommend_5)