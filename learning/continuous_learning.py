# continuous_learning.py
# 持續學習機制模組 - 基於LLM的RWA智能合約安全檢核框架

import logging
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class LearningEvent:
    timestamp: str
    event_type: str
    details: Dict[str, Any]

@dataclass
class PerformanceMetrics:
    timestamp: str
    accuracy: float
    false_positive_rate: float
    coverage_rate: float
    processing_time: float

class ContinuousLearningSystem:
    """
    持續學習系統
    - 監控模型性能
    - 適應新威脅
    - 更新監管知識
    - 生成學習建議
    """

    def __init__(self):
        self.learning_history: List[LearningEvent] = []
        self.performance_history: List[PerformanceMetrics] = []
        self.model_versions: List[str] = []
        self.performance_threshold = 0.1  # 準確度下降閾值
        logger.info("持續學習系統初始化完成")

    def monitor_performance(self, predictions: List[Any], ground_truth: List[Any], processing_time: float) -> PerformanceMetrics:
        """
        監控性能：計算準確度、誤報率、覆蓋率，並決定是否觸發模型更新
        """
        # 真實標籤集
        truth_set = {(gt.vulnerability_type, gt.location) for gt in ground_truth}
        pred_set = {(p.vulnerability_type, p.location) for p in predictions}

        tp = len(truth_set & pred_set)
        fp = len(pred_set - truth_set)
        fn = len(truth_set - pred_set)

        accuracy = tp / len(truth_set) if truth_set else 0.0
        false_positive_rate = fp / len(predictions) if predictions else 0.0
        coverage_rate = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        metrics = PerformanceMetrics(
            timestamp=datetime.now().isoformat(),
            accuracy=round(accuracy, 3),
            false_positive_rate=round(false_positive_rate, 3),
            coverage_rate=round(coverage_rate, 3),
            processing_time=round(processing_time, 3)
        )
        self.performance_history.append(metrics)
        logger.info(f"性能監控：accuracy={metrics.accuracy}, fp_rate={metrics.false_positive_rate}, coverage={metrics.coverage_rate}")

        # 決定是否更新
        if self._should_update_model():
            self._update_model(metrics)

        return metrics

    def adapt_to_new_threat(self, threat_data: Dict[str, Any]) -> LearningEvent:
        """
        適應新威脅：記錄威脅特徵並更新模式庫
        """
        event = LearningEvent(
            timestamp=datetime.now().isoformat(),
            event_type="new_threat",
            details=threat_data
        )
        self.learning_history.append(event)
        logger.info(f"新威脅事件記錄：{threat_data.get('threat_type')}")
        return event

    def update_regulatory_knowledge(self, reg_data: Dict[str, Any]) -> LearningEvent:
        """
        更新監管知識：新增或修改合規要求
        """
        event = LearningEvent(
            timestamp=datetime.now().isoformat(),
            event_type="regulatory_update",
            details=reg_data
        )
        self.learning_history.append(event)
        logger.info(f"監管知識更新事件：{reg_data.get('jurisdiction')}")
        return event

    def generate_insights(self) -> Dict[str, Any]:
        """
        生成學習洞察：性能趨勢、新威脅統計、建議
        """
        insights = {}
        if not self.performance_history:
            insights['message'] = '無績效歷史'
            return insights

        accuracies = [m.accuracy for m in self.performance_history]
        fprs = [m.false_positive_rate for m in self.performance_history]

        insights['accuracy_trend'] = 'up' if accuracies[-1] > accuracies[0] else 'down'
        insights['average_accuracy'] = round(np.mean(accuracies), 3)
        insights['average_false_positive_rate'] = round(np.mean(fprs), 3)

        threat_events = [e for e in self.learning_history if e.event_type == 'new_threat']
        insights['new_threats'] = len(threat_events)

        if accuracies[-1] < (accuracies[0] - self.performance_threshold):
            insights['recommendation'] = '建議重新訓練模型或調整參數'
        else:
            insights['recommendation'] = '模型性能穩定，繼續監控'

        logger.info("學習洞察生成完成")
        return insights

    def _should_update_model(self) -> bool:
        """
        根據最後5次性能，判斷是否觸發模型更新
        """
        if len(self.performance_history) < 5:
            return False
        recent = [m.accuracy for m in self.performance_history[-5:]]
        prev = [m.accuracy for m in self.performance_history[:-5]]
        return (np.mean(prev) - np.mean(recent)) > self.performance_threshold

    def _update_model(self, metrics: PerformanceMetrics):
        """
        模型更新函數：可擴展為實際重訓或微調
        """
        version_tag = f"v{len(self.model_versions)+1}-{metrics.timestamp}"
        self.model_versions.append(version_tag)
        logger.warning(f"觸發模型更新：新版本 {version_tag}")

# 測試入口
if __name__ == '__main__':
    cls = ContinuousLearningSystem()
    # 模擬性能監控
    from vulnerability_discriminator import SecurityFinding
    fake_preds = [SecurityFinding('重入攻擊','HIGH',0.9,'Line 10','...','...', 'CWE-362','','')]
    fake_truth = fake_preds.copy()
    metrics = cls.monitor_performance(fake_preds, fake_truth, 0.05)
    print(metrics)
    # 模擬新威脅
    event = cls.adapt_to_new_threat({'threat_type':'new_reentrancy','patterns':['call.value']})
    print(event)
    # 生成洞察
    insights = cls.generate_insights()
    print(insights)
```