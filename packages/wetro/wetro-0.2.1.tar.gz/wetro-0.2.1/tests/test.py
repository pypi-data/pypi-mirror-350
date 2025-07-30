from wetro import WetroRAG, WetroTools, Wetrocloud
import os

def main():
    pass
    # Test RAG operations via SDK
    print("=== Testing RAG Operations via SDK ===")
    # wetro_client = Wetrocloud(api_key="c80d5cb1f295297ef77eb82f42aafe09b71625e1",base_url="http://127.0.0.1:8000")
    wetro_client = Wetrocloud(api_key="wtc-sk-8f956b955c76a1049aa87b11e5f589104baf7e73")
    # wetro_client.collection.get_or_create_collection_id("test_collection_sdk")
    # collection_resp = wetro_client.collection.create_collection("test__sdk040425")
    # print("SDK Create Collection Response: %s", collection_resp.model_dump())
    # all_collection_resp = wetro_client.collection.get_collection_list()
    # print("SDK Get All Collection Response: %s", all_collection_resp.model_dump())
    
    # insert_resp = wetro_client.collection.insert_resource(resource="https://medium.com/@wetrocloud/are-image-models-getting-out-of-hand-068b13090556", type="web", collection_id="unique_collection_id_1")
    # print("SDK Insert Response: %s", insert_resp.model_dump())
    # print(os.path.abspath("test-resources/1.pdf"))
   
    # insert_resp = wetro_client.collection.insert_resource(resource="./tests/test-resources/1.pdf", type="file", collection_id="unique_collection_id_1")
    # print("SDK Insert Response: %s", insert_resp.model_dump())
    
    # Test basic query
    # query_resp = wetro_client.collection.query_collection(request_query="What is the collection about?", collection_id="test__sdk040425")
    # print("SDK Query Response: %s", query_resp.model_dump())
    
    # Test streaming query
    # print("SDK Streaming Query Responses:")
    # stream_resp = wetro_client.collection.query_collection(request_query="Streaming test", stream=True, collection_id="test_collection_sdk")
    # for chunk in stream_resp:
    #     print(chunk.model_dump())
    
    # # Test structured query
    # structured_query = wetro_client.collection.query_collection(
    #     request_query="What is this about?",
    #     json_schema={"title": "string", "summary": "string"},
    #     json_schema_rules=["Summaries the collection"],
    #     collection_id="test_collection_sdk"
    # )
    # print("SDK Structured Query Response: %s", structured_query.model_dump())
    
    # chat_history= [{"role": "user", "content": "What is this all about?"}]
    # chat_resp = wetro_client.collection.chat(message="What is this all about?", chat_history=chat_history, collection_id="test_collection_sdk")
    # print("SDK Chat Response: %s", chat_resp.model_dump())

    # delete_resource_resp = wetro_client.collection.delete_resource(insert_resp.resource_id, collection_id="test_collection_sdk")
    # print("SDK Delete Resource Response: %s", delete_resource_resp.model_dump())
    
    # delete_resp = wetro_client.collection.delete_collection(collection_id="test_collection_sdk")
    # print("SDK Delete Response: %s", delete_resp.model_dump())
    
    # # Test Tools operations via SDK
    # print("=== Testing Tools Operations via SDK ===")

    # categorize_resp = wetro_client.categorize(
    #     resource="Match review: Example vs. Test.",
    #     type="text",
    #     json_schema={"label": "string"},
    #     categories=["sports", "entertainment"],
    #     prompt="Categorize the text to see which category it best fits"
    # )
    # print("SDK Categorize Response: %s", categorize_resp.model_dump())
    
    # generate_resp = wetro_client.generate_text(
    #     messages=[{"role": "user", "content": "What is a large language model?"}],
    #     model="gpt-4"
    # )
    # print("SDK Generate Text Response: %s", generate_resp.model_dump())
    
    # ocr_resp = wetro_client.image_to_text(
    #     image_url="https://images.squarespace-cdn.com/content/v1/54822a56e4b0b30bd821480c/45ed8ecf-0bb2-4e34-8fcf-624db47c43c8/Golden+Retrievers+dans+pet+care.jpeg",
    #     request_query="What animal is in this image?"
    # )
    # print("SDK Image to Text Response: %s", ocr_resp.model_dump())
    
    # extract_resp = wetro_client.extract(
    #     website="https://medium.com/@wetrocloud/are-image-models-getting-out-of-hand-068b13090556",
    #     json_schema={"title" : "<string>", "models" : "<string>"}
    # )
    # print("SDK Extract Data Response: %s", extract_resp.model_dump())

    # markdown_response = wetro_client.markdown_converter(
    #     link="https://medium.com/@wetrocloud/are-image-models-getting-out-of-hand-068b13090556",
    #     resource_type="web"
    # )
    # print(markdown_response)
    markdown_response = wetro_client.markdown_converter(
        link="https://res.cloudinary.com/dfcunvtqz/image/upload/v1746792329/handwritten_note_3_mzx4sc.png",
        resource_type="image"
    )
    print(markdown_response)

    transcript_response = wetro_client.transcript(
        link="https://www.youtube.com/watch?v=4c9_zZJlZRw&ab_channel=TayoAina",
        resource_type="youtube"
    )
    print(transcript_response)

if __name__ == "__main__":
    main()
