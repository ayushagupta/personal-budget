from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.schemas.transactions import TransactionResponse, TransactionsResponse, TransactionCreate, TransactionUpdate
from app.services.transactions import TransactionService
from app.database.database import get_db
from app.utils.responses import ResponseHandler
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

router = APIRouter(tags=["Transactions"], prefix="/transactions")
auth_scheme = HTTPBearer()

@router.get("/", response_model=TransactionsResponse)
def get_all_transactions(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page Number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
    ):
    try:
        transactions = TransactionService.get_all_transactions(db, page, limit, token)
        transactions_response = [TransactionResponse.model_validate(transaction, from_attributes=True).model_dump()
                                 for transaction in transactions]
        response = TransactionsResponse(total_count=len(transactions_response), data=transactions_response)
        return ResponseHandler.success_response(data=response.model_dump(), status_code=200)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(transaction_id: int, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    try:
        transaction = TransactionService.get_transaction_by_id(db, transaction_id, token)
        if not transaction:
            return ResponseHandler.not_found_response(message=f"Transaction with id {transaction_id} not found")
        
        transaction_response = TransactionResponse.model_validate(transaction, from_attributes=True)
        return ResponseHandler.success_response(data=transaction_response.model_dump(), message="Transaction found successfully")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal Server Error: {str(e)}", status_code=500)
    

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    try:
        created_transaction = TransactionService.create_transaction(db, transaction, token)
        created_transaction_response = TransactionResponse.model_validate(created_transaction, from_attributes=True)
        return ResponseHandler.success_response(data=created_transaction_response.model_dump(), message="Transaction created successfully", status_code=201)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal Server Error: {str(e)}", status_code=500)
    

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int, 
    transaction: TransactionUpdate,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db)
    ):
    try:
        updated_transaction = TransactionService.update_transaction(db, transaction_id, transaction, token)
        if not updated_transaction:
            return ResponseHandler.not_found_response(message=f"Transaction with id {transaction_id} not found")
        updated_transaction_response = TransactionResponse.model_validate(updated_transaction, from_attributes=True)
        return ResponseHandler.success_response(data=updated_transaction_response.model_dump(), message="Transaction updated successfully", status_code=200)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)


@router.delete("/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: int, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    try:
        deleted_transaction = TransactionService.delete_transaction(db, transaction_id, token)
        if not deleted_transaction:
            return ResponseHandler.not_found_response(message=f"Transaction with id {transaction_id} not found")
        return ResponseHandler.success_response(data=deleted_transaction, message="Transaction deleted successfully", status_code=200)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)