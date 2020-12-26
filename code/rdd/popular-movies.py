from pyspark import SparkConf
from pyspark.sql import SparkSession


def parsing(line):
    fields = line.split(",")
    return int(fields[0]), int(fields[1])


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
    movies = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/ml-latest-small/ratings.csv")
    # Get Movies rating: the most popular movies
    # userId, movieId, rating, timestamp

    rating = movies.filter(lambda x: x != 'userId,movieId,rating,timestamp')\
        .map(parsing).map(lambda x: (x[1], 1)).reduceByKey(lambda x, y: x+y)\
        .sortBy(lambda x: x[1], ascending=False)

    # Uses Broadcast variable: Movies {movieId,title}
    # Broadcast variables allow the programmer to keep a read-only variable cached on each machine
    # nameDict contains dictionary, key - movieId; value - title
    nameDict = spark.sparkContext.broadcast(
        loadMovieNames("/Users/ykumarbekov/projects/samples/ml-latest-small/movies.csv"))

    result = rating.map(lambda x: (nameDict.value[x[0]], x[1]))
    for k in result.take(10):
        print(f"{k[0]}: {k[1]}")
