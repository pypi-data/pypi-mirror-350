from slimagents import Agent
from pydantic import BaseModel, Optional
from typing import List


class OrderItem(BaseModel):
    Beskrivelse: str
    Antall: Optional[float] = None
    Enhetspris: Optional[float] = None
    Totalpris_ink_MVA: Optional[float] = None

class OrderConfirmation(BaseModel):
    Ordrenummer: Optional[str]
    Leveransedato: Optional[str]
    Ankomsttid: Optional[str]
    Serveringstid: Optional[str]
    Kunde: Optional[str]
    Adresse: Optional[str]
    Kundens_referanse: Optional[str]
    Kunde_tlf: Optional[str]
    Kontaktperson: Optional[str]
    Postnr: Optional[str]
    Poststed: Optional[str]
    Order_Items: List[OrderItem] = []
    Total: Optional[float] = None


pdf_converter = Agent(
    instructions="Your task is to convert PDF files to Markdown.",
    model="gemini/gemini-2.0-flash",
)

# response = agent.run_sync("Who are you?")
# print(response.value)

with open("./temp/Enchiladas med salat.pdf", "rb") as pdf_file:
    response = pdf_converter.run_sync(pdf_file)
    print(response.value)



# def foo(a, b, c=3, /, *, d):
#     print(a, b, c)

# foo(1, 2, 3)