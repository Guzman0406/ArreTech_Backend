from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_roles_usuarios"
down_revision = None
branch_labels = None
depends_on = None

estado_usuario_enum = postgresql.ENUM("activo", "inactivo", name="estado_usuario", create_type=False)


def upgrade() -> None:
    estado_usuario_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
    )

    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id_rol", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("numero_empleado", sa.String(length=50), nullable=True),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("apellido", sa.String(length=50), nullable=False),
        sa.Column("correo", sa.String(length=255), nullable=False),
        sa.Column("contrasena_hash", sa.String(length=255), nullable=False),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.Column("estado", estado_usuario_enum, nullable=False, server_default="activo"),
    )

    op.create_index(
        "ix_usuarios_correo_activo",
        "usuarios",
        ["correo"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_usuarios_numero_empleado_activo",
        "usuarios",
        ["numero_empleado"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_usuarios_numero_empleado_activo", table_name="usuarios")
    op.drop_index("ix_usuarios_correo_activo", table_name="usuarios")
    op.drop_table("usuarios")
    op.drop_table("roles")
    estado_usuario_enum.drop(op.get_bind(), checkfirst=True)