from ibm_watson_machine_learning.foundation_models import Model
parameters = {"decoding_method": "greedy", "max_new_tokens": 500}
llm = Model(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials={
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": "HXH_RXb1FZFh2n4smop9Dafkq5WOu4paoxfGg85CySe5",
    },
    project_id="093e8338-ef72-48e3-a769-5608761ce50e",
    params=parameters,
)

response = llm.generate_text(prompt="""Who is barack obama """, raw_response=True)
print(response)