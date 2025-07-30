from slimagents.core import Agent

filename = "temp/Get_Started_With_Smallpdf.pdf"
with open(filename, "rb") as f:
    ocr = Agent(
        model="gpt-4o-mini",
        # model="anthropic/claude-3-5-sonnet-20240620",
        # model="gemini/gemini-1.5-flash",
    )
    response = ocr.run_sync(f, "Extract the text from the PDF file in markdown format. Don't include any other text or formatting.")
    print(response.value)