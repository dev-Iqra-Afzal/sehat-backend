from sqlalchemy.orm import Mapped, mapped_column
from ..core.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(autoincrement=True, init=False, primary_key=True, index=True)

    hospital_name: Mapped[str] = mapped_column()
    hospital_username: Mapped[str] = mapped_column(nullable=False)
    icu_beds: Mapped[int] = mapped_column()
    ventilators: Mapped[int] = mapped_column()
    monitors: Mapped[int] = mapped_column()
    defibrillators: Mapped[int] = mapped_column()
    infusion_pumps: Mapped[int] = mapped_column()
    oxygen_cylinders: Mapped[int] = mapped_column()
    xray_machines: Mapped[int] = mapped_column()
    ultrasound_machines: Mapped[int] = mapped_column()
    ct_scanners: Mapped[int] = mapped_column()
    mri_machines: Mapped[int] = mapped_column()
    ecg_machines: Mapped[int] = mapped_column()
    dialysis_machines: Mapped[int] = mapped_column()

