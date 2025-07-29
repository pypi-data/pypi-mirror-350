import base64
import litellm

filename = "tests/test.pdf"
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
    response = litellm.completion(
        # model="gpt-4o",
        # model="anthropic/claude-3-5-sonnet-20240620",
        model="gemini/gemini-1.5-flash",
        messages=[{"role": "user", "content": [file, {"type": "text", "text": text}]}],
    )
    print(response.choices[0].message.content)
    
