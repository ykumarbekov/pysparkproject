from pyspark import SparkConf
from pyspark.sql import SparkSession


def loadMovieNames(path):
    movieNames = {}
    with open(path) as f:
        for line in f:
            fields = line.split(",")
            if fields[0] != 'movieId' and fields[1] != 'title':
                movieNames[int(fields[0])] = fields[1]
    return movieNames


if __name__ == "__main__":
    conf = SparkConf().setAppName("PopularMovies").setMaster("local")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    rating = spark.read\
        .format("csv")\
        .load("/Users/ykumarbekov/projects/samples/ml-latest-small/ratings.csv", header=True, sep=",")

    moviesDict = loadMovieNames("/Users/ykumarbekov/projects/samples/ml-latest-small/movies.csv")

    topMovies = rating.groupBy("movieId").count().orderBy("count", ascending=False).cache()
    top10 = topMovies.take(10)

    print("TOP 10 Movies: ")
    for k in top10:
        if int(k[0]) in moviesDict:
            print(f"{moviesDict[int(k[0])]} - {k[1]}")
        else:
            print(f"Unknown - {k[1]}")
