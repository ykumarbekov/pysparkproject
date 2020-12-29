from pyspark import SparkConf
from pyspark.sql import SparkSession


# Whole number that cannot be made by multiplying other whole numbers - is prime
# All whole numbers above 1 are either composite or prime
# Example: 2,3 is prime, 9 is composite
def isPrime(x: int) -> bool:
    if x == 0 or x == 1:
        return False
    k = x - 1
    while k > 1:
        if x % k == 0 and k != 1:
            return False
        k -= 1
    return True


if __name__ == "__main__":
    conf = SparkConf().setAppName("PrimeNumberApp")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    # for i in range(1, 11):
    #     if isPrime(i): print(i)
    n = spark.sparkContext\
        .parallelize(range(1, 500))\
        .filter(isPrime)\
        .collect()
    print("Prime numbers: {}".format(len(n)))
