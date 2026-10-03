"""Run the lab benchmark on the AWS CPU node, using the real Kaggle dataset."""
import json
import platform
import time
from pathlib import Path
from datetime import datetime, timezone

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def main():
    start = time.perf_counter()
    data = pd.read_csv("creditcard.csv")
    load_seconds = time.perf_counter() - start
    assert data.shape == (284807, 31), f"Unexpected dataset shape: {data.shape}"
    assert int(data.Class.sum()) == 492, "Unexpected fraud count"
    x, y = data.drop(columns="Class"), data.Class
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=42)
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.2, stratify=y_train, random_state=42)
    model = lgb.LGBMClassifier(n_estimators=1000, learning_rate=0.05,
        num_leaves=31, n_jobs=2, random_state=42, verbosity=-1)
    start = time.perf_counter()
    model.fit(x_train, y_train, eval_set=[(x_val, y_val)], eval_metric="auc",
        callbacks=[lgb.early_stopping(50, first_metric_only=True), lgb.log_evaluation(100)])
    training_seconds = time.perf_counter() - start
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    row, batch = x_test.iloc[:1], x_test.iloc[:1000]
    for _ in range(10):
        model.predict_proba(row)
        model.predict_proba(batch)
    latencies, batch_times = [], []
    for _ in range(200):
        start = time.perf_counter()
        model.predict_proba(row)
        latencies.append(time.perf_counter() - start)
    for _ in range(30):
        start = time.perf_counter()
        model.predict_proba(batch)
        batch_times.append(time.perf_counter() - start)
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(), "instance_type": "t3.medium", "region": "us-east-1",
        "dataset": "mlg-ulb/creditcardfraud", "rows": len(data), "fraud_rows": int(y.sum()),
        "train_rows": len(x_train), "validation_rows": len(x_val), "test_rows": len(x_test),
        "random_seed": 42, "classification_threshold": 0.5,
        "load_data_seconds": load_seconds, "training_seconds": training_seconds,
        "best_iteration": model.best_iteration_,
        "auc_roc": roc_auc_score(y_test, probabilities),
        "accuracy": accuracy_score(y_test, predictions),
        "f1_score": f1_score(y_test, predictions, zero_division=0),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "inference_latency_1_row_ms": float(np.median(latencies) * 1000),
        "inference_latency_p95_ms": float(np.percentile(latencies, 95) * 1000),
        "inference_1000_rows_ms": float(np.median(batch_times) * 1000),
        "inference_throughput_rows_per_second": float(1000 / np.median(batch_times)),
        "timing_method": "predict_proba including Python overhead; 10 warmups, median of 200 single-row and 30 batch calls",
        "lightgbm_version": lgb.__version__,
    }
    Path("benchmark_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)
    model.booster_.save_model("lightgbm_model.txt")


if __name__ == "__main__":
    main()
