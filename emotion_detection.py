import requests
import json


def emotion_detector(text_to_analyze):
    if not text_to_analyze:
        # Handle blank entries
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code != 200:
        # Handle the invalid responses
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    else:
        return emotion_predictor(response.text)


def emotion_predictor(response):
    formatted_response = json.loads(response)
    emotion_data = formatted_response['emotionPredictions'][0]['emotion']
    emotions = {
        'anger': emotion_data.get('anger', 0),
        'disgust': emotion_data.get('disgust', 0),
        'fear': emotion_data.get('fear', 0),
        'joy': emotion_data.get('joy', 0),
        'sadness': emotion_data.get('sadness', 0)
    }
    dominant_emotion = max(emotions, key=emotions.get)
    emotions['dominant_emotion'] = dominant_emotion
    return emotions


# For testing purpose
if __name__ == "__main__":
    text = "I love this new technology."
    print(emotion_detector(text))
