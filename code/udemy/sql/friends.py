from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import Row


def mapper(line):
    fields = line.split(",")
    return Row(id=int(fields[0]), name=fields[1], age=int(fields[2]), nfriends=int(fields[2]))


if __name__ == "__main__":
    conf = SparkConf()\
        .setAppName("FriendsSQL")\
        .setMaster("local")

    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    lines = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/fakefriends.csv")
    people = lines.map(mapper)

    df = spark.createDataFrame(people).cache()
    df.createOrReplaceTempView("people")

    result = spark.sql("select * from people where age >= 14 and age <= 18")
    for i in result.collect():
        print(i)

    print("*****************")

    df.groupBy("age").count().orderBy("age").show()