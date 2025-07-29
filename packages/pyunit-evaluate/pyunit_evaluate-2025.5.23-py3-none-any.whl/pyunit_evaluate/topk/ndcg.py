import math

from .topk import TopK


class NDCG(TopK):
    """
    NDCG@k (Normalized Discounted Cumulative Gain at k) 是链路预测中常用的评估指标，用于衡量预测结果的质量和排序效果。

    计算步骤
    1. 获取预测结果和真实值
    2. 对预测结果排序
    3. 计算 DCG@k  = Σ (rᵢ / log₂(i + 1)) for i = 1 to k
    4. 计算 IDCG@k = Σ (1 / log₂(i + 1)) for i = 1 to min(k, number_of_positive_edges)
    5. 计算 NDCG@k = DCG@k / IDCG@k

    """

    def __matmul__(self, k: int) -> float:
        values = []

        for edges in self.predict_group(k):
            dcg, i_dcg = 0, 0
            for idx, item in enumerate(edges.items(), start=1):
                # 判断是正样本
                edge = self.true.has_edge(item)
                if edge and edge.score == 1:
                    dcg += item.score / math.log2(idx + 1)
                    i_dcg += 1 / math.log2(idx + 1)

            if self.exclude_zero and dcg == 0:
                continue

            values.append(dcg / i_dcg if i_dcg != 0 else 0)
        return self.mean(values)
