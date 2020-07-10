from sqlalchemy import Boolean, CheckConstraint, Column, Text
from ATE.org.database.ORM import Base


class Flow(Base):
    __tablename__ = 'flows'
    __table_args__ = (
        CheckConstraint("base=='PR' OR base=='FT'"),
    )

    name = Column(Text, primary_key=True)
    base = Column(Text, nullable=False)
    target = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    is_enabled = Column(Boolean)