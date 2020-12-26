from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as f


def parser(line):
    columns = line.split(',')
    # columns[2] - age / columns[3] - number of friends
    return int(columns[2]), int(columns[3])


if __name__ == "__main__":
    conf = SparkConf().setAppName("FriendsByAge").setMaster("local")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    # Average friends by age
    # DataSet: 1,Jean-Luc,26,2 => (26,2) (age, friends)
    # SQL: select age, count(friends) ... group by age
    # RDD: rdd.map(r => ((r._3,r._4),1)).reduceByKey((r1,r2) => r1+r2
    lines = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/fakefriends.csv")
    # *********************************
    # Convert RDD => DataFrame, set headers
    # df = lines.map(parser).toDF(["age", "friends"])
    # df1 = df.groupBy("age").agg(f.sum("friends").alias("total"), f.count("friends").alias("count"))
    # df2 = df1.select("age", f.round(f.col("total")/f.col("count")).alias("average"))
    # Result: [Row(age=33, friends=385), Row(age=26, friends=2),...
    # Transform to Dict: [{'age': 26, 'average': 242.0}, {'age': 29, 'average': 216.0},...
    # dc = df2.rdd.map(lambda r: r.asDict()).collect()
    # result = [(r['age'], r['average']) for r in dc]
    # for i in result:
    #     print(i)
    # *********************************
    rdd = lines.map(parser).mapValues(lambda x: (x, 1))
    rdd1 = rdd.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
    result = rdd1.mapValues(lambda x: x[0] / x[1]).collect()
    for i in result:
        print(f"({i[0]}, {round(i[1])})")


