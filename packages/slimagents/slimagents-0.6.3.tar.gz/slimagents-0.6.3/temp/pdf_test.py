import base64

from openai import Client

filename = "temp/Get_Started_With_Smallpdf.pdf"
with open(filename, "rb") as f:
    file_content = f.read()
    base64_content = base64.b64encode(file_content).decode('utf-8')
    file_data = f"data:application/pdf;base64,{base64_content}"
    file = {
        "type": "file",
        "file": {
            "filename": filename,
            "file_data": file_data,
        },
    }
    text = "Extract the text from the PDF file in markdown format. Don't include any other text or formatting."
    openai_client = Client()
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": [file, {"type": "text", "text": text}]}],
    )
    print(response.choices[0].message.content)

    # file_content = f.read()
    # base64_content = base64.b64encode(file_content).decode('utf-8')
    # file_data = f"data:application/pdf;base64,{base64_content}"
    # file = {
    #     "type": "file",
    #     "file": {
    #         "filename": "test.pdf",
    #         "file_data": file_data,
    #     },
    # }


    # from slimagents import Agent
    # agent = Agent(model="gpt-4o-mini")

    # result = agent.run_sync(file, "Extract the text from the PDF file.")
    # print(result.value)
    
    # import litellm
    # response = litellm.completion(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": [file, {"type": "text", "text": text}]}],
    # )
    # print(response.choices[0].message.content)
    
