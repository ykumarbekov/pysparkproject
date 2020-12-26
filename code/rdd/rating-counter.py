from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setAppName("RatingHistogram").setMaster("local")
sc = SparkContext.getOrCreate(conf=conf)

lines = sc.textFile("/Users/ykumarbekov/projects/samples/ml-latest-small/ratings.csv")
ratings = lines\
    .map(lambda x: x.split(",")[2])\
    .filter(lambda x: x != 'rating')\
    .map(lambda x: int(float(x)))
result = ratings.countByValue()

sortedResult = collections.OrderedDict(sorted(result.items()))
for key, value in sortedResult.items():
    print(f'{key} {value}')

