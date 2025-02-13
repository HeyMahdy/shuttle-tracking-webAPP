from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import String, ForeignKey, TIMESTAMP, text, Table, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

ModelBase = declarative_base()

class MainUser(ModelBase):
    __tablename__ = "Users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),  # Explicitly use PostgreSQL's UUID type
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(String, index=True, nullable=True)
    username: Mapped[str] = mapped_column(String, index=True, nullable=True)
    password: Mapped[str] = mapped_column(String,  index=True, nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=text("now()"), 
        onupdate=text("now()")
    )


    
