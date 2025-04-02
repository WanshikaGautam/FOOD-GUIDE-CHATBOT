import openai

api_key = "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"

client = openai.OpenAI(api_key=api_key)

try:
    response = client.models.list()
    print("✅ API Key is working! Models available:", [model.id for model in response.data])
except openai.OpenAIError as e:
    print("❌ API Key Error:", e)
