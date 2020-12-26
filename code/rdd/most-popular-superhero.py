from pyspark import SparkConf
from pyspark.sql import SparkSession


def countCoOccurences(line):
    el = line.split()
    return int(el[0]), len(el) - 1


def parseNames(line):
    fields = line.split('\"')
    return int(fields[0]), fields[1].encode("utf-8")


if __name__ == "__main__":
    conf = SparkConf().setAppName("MostPopularSuperHero").setMaster("local")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    names = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/marvel_names")
    namesRDD = names.map(parseNames)

    lines = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/marvel_graph")
    pairings = lines.map(countCoOccurences)
    # print(pairings.take(5))
    totalFriendsByCharacter = pairings.reduceByKey(lambda x, y: x+y)
    flipped = totalFriendsByCharacter.map(lambda x: (x[1], x[0]))
    mostPopular = flipped.max()

    mostPopularName = namesRDD.lookup(mostPopular[1])[0]
    print(f"{mostPopularName.decode('utf-8')} and occurences: {mostPopular[0]}")
