from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col
def debug_stage(data, stage_name):
    print(f"--- {stage_name} ---")
    data.printSchema()
    data.show(truncate=False)




spark = SparkSession.builder.appName("MelbourneHousePricingPrediction").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
data = spark.read.csv("melbourne_housing_data.csv", header=True, inferSchema=True)

features = ['Suburb', 'Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 'YearBuilt', 'Price']
data = data.select(features)


data = data.na.drop(subset=['Suburb', 'Rooms', 'Bathroom', 'Price'])

numeric_columns = [c for c in data.columns if c != 'Suburb']


summary_stats = data.select(numeric_columns).summary("mean").collect()


mean_values = {numeric_columns[i]: float(summary_stats[0][i + 1]) for i in range(len(numeric_columns))}


data = data.na.fill(mean_values)
data = data.filter(data["Suburb"] != "")


# indexer = StringIndexer(inputCol="Suburb", outputCol="SuburbIndex")


# encoder = OneHotEncoder(inputCol="SuburbIndex", outputCol="SuburbVec")
indexer = StringIndexer(inputCol="Suburb", outputCol="SuburbIndex", handleInvalid="keep")
indexer_model = indexer.fit(data)
indexed_data = indexer_model.transform(data)
# debug_stage(indexed_data, "Index")

encoder = OneHotEncoder(inputCols=["SuburbIndex"], outputCols=["SuburbVec"])
encoded_data = encoder.fit(indexed_data).transform(indexed_data)


# debug_stage(encoded_data, "Encode")


numericCols = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 'YearBuilt']

assembler = VectorAssembler(inputCols=numericCols + ["SuburbVec"], outputCol="features")
assembled_data = assembler.transform(encoded_data)
# debug_stage(assembled_data, "Assembled Data")


scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
scaled_data = scaler.fit(assembled_data).transform(assembled_data)
# debug_stage(scaled_data, "Scaled Data")


lr = LinearRegression(featuresCol="scaledFeatures", labelCol="Price")


pipeline = Pipeline(stages=[indexer, encoder, assembler, scaler, lr])

train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)


model = pipeline.fit(train_data)


predictions = model.transform(test_data)



# debug_stage(predictions_filtered, "predictions")





evaluator = RegressionEvaluator(labelCol="Price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

r2_evaluator = RegressionEvaluator(labelCol="Price", predictionCol="prediction", metricName="r2")
r2 = r2_evaluator.evaluate(predictions)
print(f"R2 on test data = {r2}")


model.write().overwrite().save("/app/model/spark_melbourne_house_price_model")


spark.stop()
