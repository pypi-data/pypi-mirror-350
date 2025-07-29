from .topk import TopK


class Precision(TopK):
    """
    Precision@k是链路预测中常用的评估指标之一，用于衡量模型在前k个预测结果中的准确率。

    计算方法
    1. 获取预测结果：模型为所有可能的未观察链接(或测试集中的链接)分配一个得分(概率或相似度)
    2. 排序：将所有未观察链接按照预测得分从高到低排序
    3. 选取top k：选择得分最高的前k个链接作为预测结果
    4. 统计是正样本的个数除于k
    """

    def __matmul__(self, k: int) -> float:
        values = []

        for edges in self.predict_group(k):
            one = 0
            for item in edges.items():
                if item.score < self.threshold:
                    continue

                edge = self.true.has_edge(item)
                if edge and edge.score == 1:
                    one += 1

            if self.exclude_zero and one == 0:
                continue

            values.append(one / len(edges))

        return self.mean(values)
