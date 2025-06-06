from sklearn.metrics import f1_score, precision_score, recall_score
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact
import sys

def get_classification_score(y_true, y_pred)->ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_classification_artifact = ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
        return model_classification_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)