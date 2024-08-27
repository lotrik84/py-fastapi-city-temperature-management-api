import asyncio

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal
from weather_fetcher import fetcher

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cities/", response_model=list[schemas.City])
def get_all_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@app.get("/cities/{city_id}/", response_model=schemas.City)
def get_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(city_id=city_id, db=db)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@app.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.update_city(city_id=city_id, city=city, db=db)


@app.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_city(city_id=city_id, db=db)
    if is_deleted:
        return {"message": "City deleted"}

    return {"message": f"City with id {city_id} not found"}


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def get_all_temperatures(db: Session = Depends(get_db), city_id: int = None):
    return crud.get_all_temperatures(db=db, city_id=city_id)


@app.post("/temperatures/update/")
async def update_all_temperatures(db: Session = Depends(get_db)):
    await fetcher.main(db=db)
    return {"message": "Done"}
