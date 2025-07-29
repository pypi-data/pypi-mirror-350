"""A function for clustering prediction markets."""
from itertools import chain

from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

from .cluster_model import ClusterModel
from .prediction_market_model import PredictionMarketModel


def _cleanup_cluster(cluster_model: ClusterModel) -> ClusterModel:
    prediction_markets = {}
    for prediction_market in cluster_model.markets:
        key = "_".join([prediction_market.question, prediction_market.market])
        if key not in prediction_markets:
            prediction_markets[key] = []
        prediction_markets[key].append(prediction_market)
    return ClusterModel(markets=[PredictionMarketModel(
        question=x[0].question,
        end_dt=x[0].end_dt,
        outcomes=list(chain.from_iterable([y.outcomes for y in x])),
        market=x[0].market,
    ) for x in prediction_markets.values()])

def _skip_cluster(cluster_model: ClusterModel) -> bool:
    markets = set()
    for prediction_market in cluster_model.markets:
        markets.add(prediction_market.market)
    return len(markets) <= 1


def cluster(prediction_markets: list[PredictionMarketModel], distance_threshold: float=0.375) -> list[ClusterModel]:
    """Cluster the prediction markets to link same outcomes."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([x.question for x in prediction_markets])
    clustering_model = AgglomerativeClustering(
        n_clusters=None, distance_threshold=distance_threshold
    )
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_
    clustered_questions = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_questions:
            clustered_questions[cluster_id] = []
        clustered_questions[cluster_id].append(prediction_markets[sentence_id])
    clusters = [ClusterModel(markets=x) for x in clustered_questions.values() if len(x) > 1]
    clusters = [_cleanup_cluster(x) for x in clusters]
    return [x for x in clusters if len(x.markets) > 1 and not _skip_cluster(x)]
