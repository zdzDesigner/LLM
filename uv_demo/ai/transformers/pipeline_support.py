from transformers.pipelines import SUPPORTED_TASKS


# print(SUPPORTED_TASKS.items())
supported_tasks = SUPPORTED_TASKS.items()
print(supported_tasks)


for key, val in supported_tasks:
    print(key)

# audio-classification
# automatic-speech-recognition
# text-to-audio
# feature-extraction
# text-classification
# token-classification
# question-answering
# table-question-answering
# visual-question-answering
# document-question-answering
# fill-mask
# summarization
# translation
# text2text-generation
# text-generation
# zero-shot-classification
# zero-shot-image-classification
# zero-shot-audio-classification
# image-classification
# image-feature-extraction
# image-segmentation
# image-to-text
# image-text-to-text
# object-detection
# zero-shot-object-detection
# depth-estimation
# video-classification
# mask-generation
# image-to-image
# keypoint-matching



