from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials



def main():

    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Detect faces in an image
        image_file = os.path.join('images','people.jpg')
        AnalyzeFaces(image_file)

    except Exception as ex:
        print(ex)

def AnalyzeFaces(image_file):
    print('Analyzing', image_file)

    # Specify features to be retrieved (faces)
    features = [VisualFeatureTypes.faces]
    
    # Get image analysis
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data, features)

    # Get faces
    if analysis.faces:
        print(len(analysis.faces), 'faces detected.')

        # Prepare image for drawing
        fig = plt.figure(figsize=(8, 6))
        plt.axis('off')
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        color = 'lightgreen'
        face_count = 0

        for face in analysis.faces:
            face_count += 1
            print('\nFace {}:'.format(face_count))
            
            # Draw and annotate face
            r = face.face_rectangle
            bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
            draw = ImageDraw.Draw(image)
            draw.rectangle(bounding_box, outline=color, width=5)

            # Check if age is available, otherwise show gender if available
            if face.age is not None:
                annotation = 'Person aged approximately {}'.format(face.age)
                print(' - Age: {}'.format(face.age))
            else:
                annotation = 'Face {}'.format(face_count)
                print(' - Age: Not available')
            
            # Print gender if available
            if hasattr(face, 'gender') and face.gender is not None:
                print(' - Gender: {}'.format(face.gender))
                annotation += ' ({})'.format(face.gender)
            
            plt.annotate(annotation, (r.left, r.top), backgroundcolor=color)

        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'detected_faces.jpg'
        fig.savefig(outputfile)

        print('\nResults saved in', outputfile)



if __name__ == "__main__":
    main()