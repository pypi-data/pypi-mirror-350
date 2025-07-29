from .topk import TopK


class Hits(TopK):
    """
       在链路预测中，Hits(Hyperlink-Induced Topic Search)是一种常用的评估指标，用于衡量预测结果的准确性。
       Hits指标通常分为Hits@k的形式，表示在前k个预测结果中正确预测的比例。

       Hits指标的计算方法:

       1. 对于测试集中的每个正样本(真实存在的链接)，模型会为其生成一个分数或排名。
       2. 对于每个正样本，模型还会生成一组负样本(不存在的链接)并同样计算分数。
       3. 将所有样本(正样本和负样本)按预测分数排序。
       4. 检查正样本在前k个预测结果中出现的次数。
       5. Hits@k = 正样本出现在前k个预测中的次数 / 总正样本数
    """

    def __matmul__(self, k: int) -> float:
        values = []

        for predicts in self.predict_group(k):
            positive = 0
            for predict in predicts:
                edge = self.true.has_edge(predict)
                if edge and edge.score == 1:
                    positive = 1
                    break

            values.append(positive)

        return self.mean(values)


HR = Hits
