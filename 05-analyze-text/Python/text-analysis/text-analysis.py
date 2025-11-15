from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Import namespaces


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(cog_key)
        client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)


        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detected_language = client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detected_language.primary_language.name))

            # Get sentiment
            sentiment_analysis = client.analyze_sentiment(documents=[text])[0]
            print('\nSentiment: {}'.format(sentiment_analysis.sentiment))

            # Get key phrases
            key_phrases = client.extract_key_phrases(documents=[text])[0]
            if len(key_phrases.key_phrases) > 0:
                print('\nKey Phrases:')
                for phrase in key_phrases.key_phrases:
                    print('\t{}'.format(phrase))

            # Get entities
            entities = client.recognize_entities(documents=[text])[0]
            if len(entities.entities) > 0:
                print('\nEntities:')
                for entity in entities.entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Get linked entities
            linked_entities = client.recognize_linked_entities(documents=[text])[0]
            if len(linked_entities.entities) > 0:
                print('\nLinked Entities:')
                for linked_entity in linked_entities.entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()