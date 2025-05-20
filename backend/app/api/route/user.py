from fastapi import APIRouter, Depends, HTTPException   

router = APIRouter()

@router.post("/create_user")
async def create_user(user: dict):
    pass