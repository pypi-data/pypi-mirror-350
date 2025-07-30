import logging
from typing import Any, Callable

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session


class Transactions(BaseModel):
    table_type: type
    public_type: type
    create_type: type
    find_function: Callable

    def _find(
        self,
        session: Session,
        demand_model: Any,
    ) -> Any | None:
        result = None
        found = session.exec(self.find_function(demand_model)).all()

        if len(found) > 1:
            logging.warning(
                (
                    f"Found two or more {self.table_type.__name__}. "
                    "The uniqueness criteria should prevent this from happening."
                )
            )

        if found:
            result = self.public_type.model_validate(found[0])
            logging.info(f"Found {found[0]}")
        else:
            logging.debug(
                f"Did not find {self.table_type.__name__} with statement {self.find_function(demand_model)}"
            )

        return result

    def create(
        self,
        session: Session,
        create_model: Any,
    ) -> Any:
        created = self.table_type.model_validate(create_model)
        session.add(created)

        try:
            session.commit()
        except IntegrityError as e:
            logging.warning(
                f"Ignored duplicated and/or invalid entry. Exception caught: {e}"
            )

        session.refresh(created)

        if created.key is None:
            raise Exception(f"Failed at creating database object for {created}")

        result = self.public_type.model_validate(created)
        return result

    def demand(
        self,
        session: Session,
        demand_model: Any,
    ) -> Any:
        found = self._find(session=session, demand_model=demand_model)
        create_model = self.create_type.model_validate(demand_model)
        demanded = (
            found
            if found
            else self.create(
                session=session,
                create_model=create_model,
            )
        )
        return demanded
