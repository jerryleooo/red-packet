"""empty message

Revision ID: d006389943c8
Revises: 
Create Date: 2017-09-23 12:28:35.878905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd006389943c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('red_packet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('date_updated', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('token', sa.String(length=8), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_red_packet_date_created'), 'red_packet', ['date_created'], unique=False)
    op.create_index(op.f('ix_red_packet_date_updated'), 'red_packet', ['date_updated'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_red_packet_date_updated'), table_name='red_packet')
    op.drop_index(op.f('ix_red_packet_date_created'), table_name='red_packet')
    op.drop_table('red_packet')
    # ### end Alembic commands ###
