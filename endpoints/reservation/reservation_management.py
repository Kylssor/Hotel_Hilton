from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from domain.utils.dependencies import get_current_user_from_token, get_db_context
from domain.service.reservation_service import ReservationService
from models.repository.unit_of_work import UnitOfWork
from models.context.persistence_context import PersistenceContext

router = APIRouter(prefix="/reservation-management", tags=["Reservation Management"])

@router.post("/{reservation_id}/complete")
def complete_reservation(
    reservation_id: UUID,
    db_context: PersistenceContext = Depends(get_db_context),
    current_user: dict = Depends(get_current_user_from_token)
):
    uow = UnitOfWork(db_context)
    try:
        service = ReservationService(uow)
        service.complete_reservation(reservation_id)
        uow.commit()
        return {"message": f"Reservation {reservation_id} marked as completed."}
    except Exception as e:
        uow.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        uow.close()


@router.post("/{reservation_id}/cancel")
def cancel_reservation(
    reservation_id: UUID,
    db_context: PersistenceContext = Depends(get_db_context),
    current_user: dict = Depends(get_current_user_from_token)
):
    uow = UnitOfWork(db_context)
    try:
        service = ReservationService(uow)
        service.cancel_reservation(reservation_id)
        uow.commit()
        return {"message": f"Reservation {reservation_id} has been cancelled."}
    except Exception as e:
        uow.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        uow.close()
