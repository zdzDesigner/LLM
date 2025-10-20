from transformers import pipeline

# classifier = pipeline("sentiment-analysis")
classifier = pipeline("text-classification")

result = classifier("i like this")

print(result)
