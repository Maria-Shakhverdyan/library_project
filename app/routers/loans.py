from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.connection import get_db
from app.services.loans_service import (
    get_loans,
    get_loan_by_id,
    create_loan,
    update_loan,
    delete_loan,
    get_detailed_loans_info,
    count_active_loans_by_book,
)
from app.schemas.loans import LoanCreate, Loan, LoanDetail, LoanGroupByBook
from app.database.models.books import Book
from app.database.models.loans import Loan
from app.database.models.readers import Reader

router = APIRouter()

@router.get("/", response_model=list[Loan])
async def read_loans(db: AsyncSession = Depends(get_db)):
    """Retrieve all loans."""
    return await get_loans(db)

@router.get("/{loan_id}", response_model=Loan)
async def read_loan(loan_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a loan by its ID."""
    loan = await get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.post("/", response_model=Loan)
async def add_loan(loan: LoanCreate, db: AsyncSession = Depends(get_db)):
    """Add a new loan."""
    return await create_loan(db, loan)

@router.put("/{loan_id}", response_model=Loan)
async def update_loan_endpoint(loan_id: int, loan: LoanCreate, db: AsyncSession = Depends(get_db)):
    """Update a loan by its ID."""
    updated_loan = await update_loan(db, loan_id, loan)
    if not updated_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return updated_loan

@router.delete("/{loan_id}")
async def delete_loan_endpoint(loan_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a loan by its ID."""
    if not await delete_loan(db, loan_id):
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Loan deleted successfully"}

@router.get("/detailed", response_model=list[LoanDetail])
async def get_detailed_loans(db: AsyncSession = Depends(get_db)):
    """Retrieve detailed loan information, including book and reader details."""
    return await get_detailed_loans_info(db)

@router.get("/group-by-book", response_model=list[LoanGroupByBook])
async def group_loans_by_book(db: AsyncSession = Depends(get_db)):
    """Count active loans grouped by each book."""
    return await count_active_loans_by_book(db)

@router.get("/loans/details/", response_model=list[dict])
async def get_loan_details(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, le=100, description="Maximum number of records to retrieve"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve detailed loan information with book and reader details."""
    query = (
        select(Loan.id, Book.title.label("book_title"), Reader.name.label("reader_name"))
        .join(Book, Loan.book_id == Book.id)
        .join(Reader, Loan.reader_id == Reader.id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    loans = result.all()
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found")
    return loans
