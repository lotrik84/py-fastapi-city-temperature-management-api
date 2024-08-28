from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from temperature import crud
from temperature import schemas
from dependencies import get_db
from weather_fetcher import fetcher

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_all_temperatures(db: Session = Depends(get_db), city_id: int = None):
    return crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update/")
async def update_all_temperatures(db: Session = Depends(get_db)):
    await fetcher.main(db=db)
    return {"message": "Done"}
