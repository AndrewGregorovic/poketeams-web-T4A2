"""Initial migration.

Revision ID: f1483054652d
Revises: 
Create Date: 2021-03-03 17:43:04.666371

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import CreateSequence, Sequence


# revision identifiers, used by Alembic.
revision = 'f1483054652d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('moves',
    sa.Column('move_id', sa.Integer(), nullable=False),
    sa.Column('move_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('move_id')
    )
    op.create_table('pokemon',
    sa.Column('pokeapi_id', sa.Integer(), nullable=False),
    sa.Column('pokemon_id', sa.Integer(), nullable=False),
    sa.Column('pokemon_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('pokeapi_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute(CreateSequence(Sequence('teams_pokemon_id_seq')))
    op.create_table('teams_pokemon',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('team_index', sa.Integer(), nullable=False),
    sa.Column('pokeapi_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pokeapi_id'], ['pokemon.pokeapi_id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'team_index'),
    sa.UniqueConstraint('id')
    )
    op.create_table('pokemon_moves',
    sa.Column('team_pokemon_id', sa.Integer(), nullable=False),
    sa.Column('pokeapi_id', sa.Integer(), nullable=False),
    sa.Column('pokemon_move_index', sa.Integer(), nullable=False),
    sa.Column('move_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['move_id'], ['moves.move_id'], ),
    sa.ForeignKeyConstraint(['pokeapi_id'], ['pokemon.pokeapi_id'], ),
    sa.ForeignKeyConstraint(['team_pokemon_id'], ['teams_pokemon.id'], ),
    sa.PrimaryKeyConstraint('team_pokemon_id', 'pokeapi_id', 'pokemon_move_index')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_moves')
    op.drop_table('teams_pokemon')
    op.drop_table('teams')
    op.drop_table('users')
    op.drop_table('pokemon')
    op.drop_table('moves')
    # ### end Alembic commands ###
