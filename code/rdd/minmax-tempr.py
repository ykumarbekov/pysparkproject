from pyspark import SparkConf
from pyspark.sql import SparkSession


def parser(line):
    fields = line.split(',')
    stationID = fields[0]
    entryType = fields[2]
    f = float(fields[3]) * 0.1 * (9 / 5) + 32
    temper = float(fields[3]) * 0.1 * (9 / 5) + 32
    # temper = (f - 32) * (5 / 9)
    return stationID, entryType, temper


def getEntryType(fields):
    if 'TMAX' in fields[1]:
        return True
    else:
        return False


if __name__ == "__main__":
    conf = SparkConf().setAppName("MinMaxTemperatures").setMaster("local")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    lines = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/1800.csv")
    rdd = lines.map(parser).filter(getEntryType).map(lambda x: (x[0], x[2]))
    result = rdd.reduceByKey(lambda x, y: max(x, y)).collect()

    for i in result:
        print(f"{i[0]} -> {round(i[1],2)}F")
