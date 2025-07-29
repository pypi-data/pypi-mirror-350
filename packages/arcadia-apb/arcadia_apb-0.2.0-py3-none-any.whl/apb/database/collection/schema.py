import pandera as pa
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

from apb.types import aa_dtype, ss3_dtype

Base = declarative_base()


class Protein(Base):
    __tablename__ = "proteins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    sequence = Column(String)
    structure = Column(LargeBinary)
    source = Column(String)

    residues = relationship("Residue", back_populates="protein")
    residue_pairs = relationship("ResiduePair", back_populates="protein")


class Residue(Base):
    __tablename__ = "residues"
    id = Column(Integer, primary_key=True, autoincrement=True)
    protein_id = Column(Integer, ForeignKey("proteins.id"), index=True)
    residue_index = Column(Integer)
    amino_acid = Column(String)
    secondary_structure = Column(String)
    solvent_accessibility = Column(Float)
    relative_solvent_accessibility = Column(Float)

    protein = relationship("Protein", back_populates="residues")
    residue_pair1 = relationship(
        "ResiduePair",
        foreign_keys="[ResiduePair.residue1_id]",
        back_populates="residue1",
        overlaps="residue_pair2,residue1",
    )
    residue_pair2 = relationship(
        "ResiduePair",
        foreign_keys="[ResiduePair.residue2_id]",
        back_populates="residue2",
        overlaps="residue_pair1,residue2",
    )


class ResiduePair(Base):
    """Residue-to-residue measures

    This table holds information related to residue pairs. The most canonical example
    is the Euclidean distance between two residues.

    TODO currently unused
    """

    __tablename__ = "residue_pairs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    protein_id = Column(Integer, ForeignKey("proteins.id"), index=True)
    residue1_id = Column(Integer, ForeignKey("residues.id"))
    residue2_id = Column(Integer, ForeignKey("residues.id"))
    distance = Column(Float)

    protein = relationship("Protein", back_populates="residue_pairs")
    residue1 = relationship("Residue", foreign_keys=[residue1_id], uselist=False)
    residue2 = relationship("Residue", foreign_keys=[residue2_id], uselist=False)


residue_dataframe_schema = pa.DataFrameSchema(
    {
        Residue.residue_index.key: pa.Column("uint32"),
        Residue.amino_acid.key: pa.Column(aa_dtype),
        Residue.secondary_structure.key: pa.Column(
            ss3_dtype,
            nullable=True,
        ),
        Residue.solvent_accessibility.key: pa.Column(
            "float64",
            checks=[pa.Check.ge(0.0)],
            nullable=True,
        ),
        Residue.relative_solvent_accessibility.key: pa.Column(
            "float64",
            checks=[pa.Check.le(1.0), pa.Check.ge(0.0)],
            nullable=True,
        ),
    },
    coerce=True,
)
