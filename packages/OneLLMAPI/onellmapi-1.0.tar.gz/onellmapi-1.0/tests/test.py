from openai import OpenAI
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中读取您的方舟API Key。
    api_key="3f43fdbd-6e2e-4964-a405-514b4b9e0cd8"
)
completion = client.chat.completions.create(
    # 替换为您的方舟推理接入点。
    model="<YOUR_ENDPOINT_ID>",
    messages = [
        {"role": "user", "content": "你好"},
    ]
)
print(completion.choices[0].message.content)