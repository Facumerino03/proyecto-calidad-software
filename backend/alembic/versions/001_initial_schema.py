"""Esquema inicial: archivos y tramites

Revision ID: 001
Revises:
Create Date: 2026-06-04

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "archivos",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("nombre_archivo", sa.String(length=255), nullable=False),
        sa.Column("tipo_mime", sa.String(length=100), nullable=False),
        sa.Column("tamano_bytes", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("fecha_subida", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tramites",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tracking_id", sa.String(length=20), nullable=False),
        sa.Column("tipo", sa.String(length=20), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("apellido", sa.String(length=100), nullable=False),
        sa.Column("dni", sa.String(length=20), nullable=False),
        sa.Column("mail", sa.String(length=255), nullable=False),
        sa.Column("telefono", sa.String(length=30), nullable=False),
        sa.Column("direccion", sa.String(length=500), nullable=False),
        sa.Column("archivo_id_1", sa.String(length=50), nullable=False),
        sa.Column("archivo_id_2", sa.String(length=50), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fecha_resolucion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("motivo_rechazo", sa.Text(), nullable=True),
        sa.Column("nota_interna", sa.Text(), nullable=True),
        sa.Column("resuelto_por", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tramites_tracking_id"), "tramites", ["tracking_id"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_tramites_tracking_id"), table_name="tramites")
    op.drop_table("tramites")
    op.drop_table("archivos")
