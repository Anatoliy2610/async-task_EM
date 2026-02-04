from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'spimex_trading_results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('year', sa.Float),
        sa.Column('month_number', sa.Float),
        sa.Column('category', sa.String),
        sa.Column('count_contracts', sa.Float),
        sa.Column('count_value_contracts', sa.Float),
    )


def downgrade():
    op.drop_table('spimex_trading_results')
