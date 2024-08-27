from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_cities(db: Session):
    return db.query(models.DBCity).all()


def get_city_by_id(db: Session, city_id: int = None):
    queryset = db.query(models.DBCity)

    if city_id is not None:
        queryset = queryset.filter(models.DBCity.id == city_id)

    return queryset.first()


def update_city(db: Session, city: schemas.CityCreate, city_id: int = None):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int = None):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    if db_city is not None:
        db.delete(db_city)
        db.commit()
        return True
    return False


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_temperatures(db: Session, city_id: int = None):
    if city_id is None:
        return db.query(models.DBTemperature).all()

    return (
        db.query(models.DBTemperature)
        .filter(models.DBTemperature.city_id == city_id)
        .all()
    )
