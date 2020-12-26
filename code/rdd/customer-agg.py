from pyspark import SparkConf
from pyspark.sql import SparkSession


def parser(line):
    fields = line.split(',')
    customerId = int(fields[0])
    amount = float(fields[2])
    return customerId, amount


if __name__ == "__main__":
    conf = SparkConf().setAppName("CustomerAgg").setMaster("local")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    inp = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/customer-orders.csv")
    result = inp.map(parser)\
        .reduceByKey(lambda x, y: x+y)\
        .map(lambda x: (x[0], round(x[1], 2)))\
        .sortBy(lambda x: x[1], ascending=False).collect()

    for i in result:
        print(f"CustomerID: {i[0]} Total amount: {i[1]}")
