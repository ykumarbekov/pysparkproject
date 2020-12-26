from pyspark import SparkConf
from pyspark.sql import SparkSession
import math
import sys


def loadMovieNames(path):
    movieNames = {}
    with open(path) as f:
        for line in f:
            fields = line.split(",")
            if fields[0] != 'movieId' and fields[1] != 'title':
                movieNames[int(fields[0])] = fields[1]  # .decode('ascii', 'ignore')
    return movieNames


def computeCosineSimilarity(ratingPairs):
    numPairs = 0
    sum_xx = sum_yy = sum_xy = 0
    for ratingX, ratingY in ratingPairs:
        sum_xx += ratingX * ratingX
        sum_yy += ratingY * ratingY
        sum_xy += ratingX * ratingY
        numPairs += 1

    numerator = sum_xy
    denominator = math.sqrt(sum_xx) * math.sqrt(sum_yy)

    score = 0
    if denominator:
        score = (numerator / (float(denominator)))

    return score, numPairs


def makePairs(userRatings):
    ratings = userRatings[1]
    (movie1, rating1) = ratings[0]
    (movie2, rating2) = ratings[1]
    return (movie1, movie2), (rating1, rating2)


# Python 3 doesn't let you pass around unpacked tuples, you can't use: filterDuplicates(user, ratings)
def filterDuplicates(userRatings):
    ratings = userRatings[1]
    (movie1, rating1) = ratings[0]
    (movie2, rating2) = ratings[1]
    return movie1 < movie2


def parsingRatings(line):
    fields = line.split(",")
    if fields[0] != 'userId' and fields[1] != 'movieId' and fields[2] != 'rating':
        return int(fields[0]), int(fields[1]), int(round(float(fields[2])))


if __name__ == "__main__":
    conf = SparkConf().setAppName("MoviesSimilarities").setMaster("local[*]")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    print("Loading movie names")
    nameDict = loadMovieNames("/Users/ykumarbekov/projects/samples/ml-latest-small/movies.csv")

    data = spark.sparkContext.textFile("/Users/ykumarbekov/projects/samples/ml-latest-small/ratings-10000.csv")
    # to key / value pairs: userId => movieId, rating
    # ratings = data.map(parsingRatings).filter(lambda x: x is not None).map(lambda l: (l[0], (l[1], l[2])))
    # Remove bad ratings, filter all that less than 2
    ratings = data.map(parsingRatings).filter(lambda x: x is not None)\
        .filter(lambda x: x[2] > 2)\
        .map(lambda l: (l[0], (l[1], l[2])))
    # print(ratings.take(5))
    # self-join to find every combination
    # userId => (movieId, rating), (movieId, rating)) and we removed duplicates
    joinedRatings = ratings.join(ratings).filter(filterDuplicates)

    # collect all ratings for each movie pair and compute similarity
    moviePairRatings = joinedRatings.map(makePairs).groupByKey()

    moviePairSimilarities = moviePairRatings.mapValues(computeCosineSimilarity).cache()
    # print(moviePairSimilarities.take(5))

    if len(sys.argv) > 1:
        movieID = int(sys.argv[1])
        scoreThreshold = 0.97
        coOccurenceThreshold = 50

        filtered = moviePairSimilarities\
            .filter(lambda x: (x[0][0] == movieID or x[0][1] == movieID)
                    and x[1][0] > scoreThreshold and x[1][1] > coOccurenceThreshold)

        results = filtered.map(lambda pairSim: (pairSim[1], pairSim[0])).sortByKey(ascending=False).take(10)

        print("Top 10 similar movies for " + nameDict[movieID])
        for result in results:
            (sim, pair) = result
            # Display the similarity result that isn't the movie we're looking at
            similarMovieID = pair[0]
            if similarMovieID == movieID:
                similarMovieID = pair[1]
            print(nameDict[similarMovieID] + "\tscore: " + str(sim[0]) + "\tstrength: " + str(sim[1]))
