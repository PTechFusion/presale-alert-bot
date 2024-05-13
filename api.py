from fastapi import FastAPI
from pydantic import BaseModel
from utils.config import *

from utils.bot import bot, create_presale_message
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add a CORS middleware with the origins allowed


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://helldiver.vip"],  # Allow your front-end domain
    allow_credentials=True,
    allow_methods=["POST"],  # Specify the methods
    allow_headers=["Content-Type"],  # Specify which headers are allowed
    expose_headers=["Access-Control-Allow-Origin"],  # Ensure this header is exposed
)


class Transaction(BaseModel):
    Tx_Hash: str
    Amount_In: float
    Tokens_Bought: int
    Wallet: str
    Input_Unit: str

@app.post("/transaction/")
async def process_transaction(transaction: Transaction):
    data = {}
    result = contract.functions.getpriceAndStage().call()
    stage_number = result[1]
    stage_price = Web3.from_wei(int(result[0]),'ether')
    message = create_presale_message(transaction.Amount_In, transaction.Tokens_Bought, transaction.Tx_Hash, stage_number, stage_price, LAUNCH_PRICE, transaction.Input_Unit)
    with open('utils/picture.gif', 'rb') as gif:
        bot.send_animation(chat_id=CHAT_ID, animation=gif, caption=message, parse_mode='MarkDown')
    return {"message": "Transaction processed successfully", "transaction_data": transaction.dict()}
