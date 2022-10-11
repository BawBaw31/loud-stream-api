"""Add album model

Revision ID: dbb7fe1cefe8
Revises: 901284fe86ca
Create Date: 2022-10-11 17:50:32.276538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbb7fe1cefe8'
down_revision = '901284fe86ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('cover_file_name', sa.String(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['artists.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cover_file_name')
    )
    op.create_index(op.f('ix_albums_id'), 'albums', ['id'], unique=False)
    op.create_index(op.f('ix_albums_title'), 'albums', ['title'], unique=False)
    op.drop_constraint('artists_stage_name_key', 'artists', type_='unique')
    op.add_column('musics', sa.Column('album_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'musics', 'albums', ['album_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'musics', type_='foreignkey')
    op.drop_column('musics', 'album_id')
    op.create_unique_constraint('artists_stage_name_key', 'artists', ['stage_name'])
    op.drop_index(op.f('ix_albums_title'), table_name='albums')
    op.drop_index(op.f('ix_albums_id'), table_name='albums')
    op.drop_table('albums')
    # ### end Alembic commands ###