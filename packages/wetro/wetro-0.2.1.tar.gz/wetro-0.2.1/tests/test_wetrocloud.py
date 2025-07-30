import unittest
from wetro import Wetrocloud
import time
import os

# To run the tests:
# $ python -m unittest test_wetrocloud.py

# To run only one test
# $ python -m unittest test_wetrocloud.TestWetrocloudAPI.test_get_all_collections

class TestWetrocloudAPI(unittest.TestCase):

    def setUp(self):
        self.collection_id = "my_unique_collection_id"
        self.resource_id = "my_unique_resource_id"
        # Initialize the Wetrocloud client with your real API key
        self.client = Wetrocloud(api_key="wtc-sk-8f956b955c76a1049aa87b11e5f589104baf7e73")

    # Create collection
    def test_create_collection(self):
        # Test the create_collection method
        collection_id = "my_unique_collection_id_12345678"

        # Create a new collection
        response = self.client.collection.create_collection(collection_id=collection_id)
        self.collection_id = collection_id  # Store the collection ID for later use
        print("Create Collection Response:", response)

        self.assertEqual(response.collection_id, collection_id)


    # def test_create_or_get_collection(self):
    #     # Test the get_or_create_collection_id method (creating or fetching a collection)
    #     collection_id = "my_unique_collection_id"

    #     # Create or get collection
    #     response = self.client.collection.get_or_create_collection_id(collection_id=collection_id)
    #     print("Get or Create Collection Response:", response)

    #     self.assertEqual(response.collection_id, collection_id)

    # Get all collections
    def test_get_all_collections(self):
        # Test getting all collections
        response = self.client.collection.get_collection_list()
        print("Get All Collections Response:", response)
        
        self.assertIsNotNone(response.count)

    # Insert resource
    def test_insert_resource(self):
        # Test inserting a web resource into the collection
        collection_id = self.collection_id
        resource_url = "https://medium.com/@wetrocloud/are-image-models-getting-out-of-hand-068b13090556"
        
        # Insert the resource
        response = self.client.collection.insert_resource(collection_id=collection_id, resource=resource_url, type="web")
        print("Insert Resource Response:", response)

        self.resource_id= response.resource_id  # Store the resource ID for later use   
        
        self.assertIsNotNone(response.resource_id)
        self.assertEqual(response.success, True)

        # Upload Insert resource
    def test_upload_insert_resource(self):
        # Test inserting a web resource into the collection
        collection_id = self.collection_id
        resource_url = "./tests/test-resources/1.pdf"
        
        # Insert the resource
        response = self.client.collection.insert_resource(collection_id=collection_id, resource=resource_url, type="file")
        print("Insert Resource Response:", response)

        self.resource_id= response.resource_id  # Store the resource ID for later use   
        
        self.assertIsNotNone(response.resource_id)
        self.assertEqual(response.success, True)

    # Query collection
    def test_query_collection(self):
        # Test querying a collection
        collection_id = self.collection_id
        request_query = "What are the key points of the article?"
        
        # Query the collection
        response = self.client.collection.query_collection(collection_id=collection_id, request_query=request_query)
        print("Query Collection Response:", response)
        
        self.assertEqual(response.success, True)
        self.assertIsNotNone(response.response)

    # Query collection with JSON schema
    def test_query_collection_with_schema_and_rules(self):
        # Define the JSON schema and rules
        json_schema = [{"point_number": "<int>", "point": "<str>"}]
        rules = ["Only 5 points", "Strictly return JSON only"]

        # Query the collection with schema and rules
        response = self.client.collection.query_collection(
            collection_id=self.collection_id,
            request_query="What are the key points of the article?",
            json_schema=json_schema,
            json_schema_rules=rules
        )
        
        print("Query Collection Response:", response)

        self.assertEqual(response.success, True)
        self.assertIsNotNone(response.response)


    def test_streaming_response(self):
        # Query the collection with the stream flag set to True
        streaming_response = self.client.collection.query_collection(
            collection_id=self.collection_id,
            request_query="Give me a detailed summary of the article",
            stream=True
        )

        # Initialize a variable to store the complete response
        full_response = ""

        # Process the streaming response
        for chunk in streaming_response:
            # Check that the chunk has a 'response' attribute and that it's a string
            self.assertTrue(hasattr(chunk, 'response'))
            self.assertIsInstance(chunk.response, str)

            # Print or accumulate the chunk in the full response
            full_response += chunk.response

        # Ensure the full response is not empty (to confirm data was streamed)
        self.assertGreater(len(full_response), 0)

        # Optionally, print the full response for review
        print("Full streamed response:", full_response)


    def test_chat_with_history(self):
        # Define the initial chat history
        chat_history = [
            {"role": "user", "content": "What is this collection about?"}, 
            {"role": "system", "content": "It stores research papers on AI technology."}
        ]

        # Define the new message to continue the conversation
        new_message = "Can you explain the latest paper's methodology?"

        # Continue the conversation with context
        chat_response = self.client.collection.chat(
            collection_id=self.collection_id,
            message=new_message,
            chat_history=chat_history
        )
        
        # Print the chat response
        print("Chat Response:", chat_response)

        # Assert the response has the expected structure
        self.assertEqual(chat_response.success, True)
        self.assertIsNotNone(chat_response.response)

    # Delete resource
    def test_delete_resource(self):
        # Test querying a collection
        collection_id = self.collection_id
        resource_id = self.resource_id

        # Delete the resource
        response = self.client.collection.delete_resource(resource_id=resource_id, collection_id=collection_id)
        print("Delete Resource Response:", response)

        self.assertEqual(response.success, True)

    # Delete collection
    def test_delete_collection(self):
        # Test deleting a collection
        collection_id = self.collection_id

        # Delete the collection
        response = self.client.collection.delete_collection(collection_id=collection_id)
        print("Delete Collection Response:", response)

        self.assertEqual(response.success, True)



    def test_text_generation(self):
        # Define the input messages for the text generation
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": "Write a short poem about technology."}
        ]
        
        # Call the generate_text method to get the response from the specified model
        response = self.client.generate_text(
            messages=messages,
            model="gpt-4"  # Specify the model here
        )
        
        # Print the response for review
        print("Generated Text:", response)

        # Assert that the response contains a valid text
        self.assertEqual(response.success, True)
        self.assertIsNotNone(response.response)

    
    # Categorize data
    def test_data_categorization(self):
        # Define the resource (content to categorize)
        resource = "match review: John Cena vs. The Rock."
        
        # Define the json_schema for categorization
        json_schema = {"label": "string"}

        # Define the possible categories
        categories = ["wrestling", "entertainment", "sports", "news"]

        # Call the categorize method
        categorize_response = self.client.categorize(
            resource=resource,
            type="text",  # Specify that the resource type is text
            json_schema=json_schema,
            categories=categories,
            prompt="Categorize the text to see which category it best fits"
        )

        # Print the categorize response for review
        print("Categorize Response:", categorize_response)

        # Assert that the response contains the expected status
        self.assertEqual(categorize_response.success, True)
        self.assertIsNotNone(categorize_response.response)

    
    # Image to text
    def test_image_to_text(self):
        # Define the image URL and the query to ask about the image
        image_url = "https://images.squarespace-cdn.com/content/v1/54822a56e4b0b30bd821480c/45ed8ecf-0bb2-4e34-8fcf-624db47c43c8/Golden+Retrievers+dans+pet+care.jpeg"
        request_query = "What animal is in this image?"

        # Call the image_to_text method to extract text from the image and answer the query
        ocr_response = self.client.image_to_text(
            image_url=image_url,
            request_query=request_query
        )
        
        # Print the OCR response for review
        print("OCR Response:", ocr_response)

        # Assert that the response contains the expected status and answer
        self.assertEqual(ocr_response.success, True)
        self.assertIsNotNone(ocr_response.response)


    # Data extraction
    def test_data_extraction(self):
        # Define the website URL from which data will be extracted
        website_url = "https://medium.com/@wetrocloud/are-image-models-getting-out-of-hand-068b13090556"

        # Define the json_schema for the expected structured data
        json_schema ={"title" : "<string>", "models" : "<string>"}

        # Call the extract method to get structured data from the website
        extract_response = self.client.extract(
            website=website_url,
            json_schema=json_schema
        )
        
        # Print the extraction response for review
        print("Extract Response:", extract_response)

        # Assert that the response contains the expected status and answer
        self.assertEqual(extract_response.success, True)
        self.assertIsNotNone(extract_response.response)


    def tearDown(self):
        # Optional: Clean up after tests, like deleting the collection or resources.
        # Be careful with this as it will actually delete your collection.
        # self.client.collection.delete_collection(collection_id="my_unique_collection_id")
        pass


if __name__ == "__main__":
    unittest.main()
