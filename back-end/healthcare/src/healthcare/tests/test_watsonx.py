from ibm_watson_machine_learning.foundation_models import Model
parameters = {"decoding_method": "greedy", "max_new_tokens": 500}
llm = Model(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials={
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": "<YOUR_API_KEY>",
    },
    project_id="<YOUR_PROJECT_ID>",
    params=parameters,
)

response = llm.generate_text(prompt="""Who is barack obama """, raw_response=True)
print(response)