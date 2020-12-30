from pyspark import SparkConf
from pyspark.sql import SparkSession
import re


def normalizeWords(text):
    return re.compile(r'\W+', re.UNICODE).split(text.lower())


if __name__ == "__main__":
    conf = SparkConf().setAppName("WordCount-App")

    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    # inp = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/udemy-spark-python/Book")
    inp = spark.sparkContext.textFile("hdfs://ns1/tmp/data/sources/book")
    # result = inp.flatMap(lambda x: x.split()).countByValue()
    # result = inp.flatMap(normalizeWords).countByValue()
    rdd = inp.flatMap(normalizeWords).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x+y)
    result = rdd.sortBy(lambda x: x[1], ascending=False).collect()

    count = 0
    for i in result:
        if count < 20 and i[0].encode('ascii', 'ignore'):
            print(f"{i[0]} -> {i[1]}")
        count = count + 1

    # sorted_result = {k: v for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True)}
    # Top ten most frequencies of words
    # count = 0
    # for key, value in sorted_result.items():
    #     if key.encode('ascii', 'ignore') and count < 10:
    #         print(f"{key} -> {value}")
    #     count = count + 1

