"""setup

Revision ID: 001
Revises: 
Create Date: 2024-07-03 07:47:24.228683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.Inspector.from_engine(conn)

    if 'ds_metrics' not in inspector.get_table_names():
        op.create_table(
            'ds_metrics',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('number_of_models', sa.String(length=120), nullable=True),
            sa.Column('number_of_features', sa.String(length=120), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    if 'fm_metrics' not in inspector.get_table_names():
        op.create_table(
            'fm_metrics',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('solver', sa.Text(), nullable=True),
            sa.Column('not_solver', sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    if 'user' not in inspector.get_table_names():
        op.create_table(
            'user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(length=256), nullable=False),
            sa.Column('password', sa.String(length=256), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )

    if 'zenodo' not in inspector.get_table_names():
        op.create_table(
            'zenodo',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )

    if 'ds_meta_data' not in inspector.get_table_names():
        op.create_table(
            'ds_meta_data',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('deposition_id', sa.Integer(), nullable=True),
            sa.Column('title', sa.String(length=120), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('publication_type', sa.Enum('NONE', 'ANNOTATION_COLLECTION', 'BOOK', 'BOOK_SECTION', 'CONFERENCE_PAPER', 'DATA_MANAGEMENT_PLAN', 'JOURNAL_ARTICLE', 'PATENT', 'PREPRINT', 'PROJECT_DELIVERABLE', 'PROJECT_MILESTONE', 'PROPOSAL', 'REPORT', 'SOFTWARE_DOCUMENTATION', 'TAXONOMIC_TREATMENT', 'TECHNICAL_NOTE', 'THESIS', 'WORKING_PAPER', 'OTHER', name='publicationtype'), nullable=False),
            sa.Column('publication_doi', sa.String(length=120), nullable=True),
            sa.Column('dataset_doi', sa.String(length=120), nullable=True),
            sa.Column('tags', sa.String(length=120), nullable=True),
            sa.Column('ds_metrics_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['ds_metrics_id'], ['ds_metrics.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'fm_meta_data' not in inspector.get_table_names():
        op.create_table(
            'fm_meta_data',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('uvl_filename', sa.String(length=120), nullable=False),
            sa.Column('title', sa.String(length=120), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('publication_type', sa.Enum('NONE', 'ANNOTATION_COLLECTION', 'BOOK', 'BOOK_SECTION', 'CONFERENCE_PAPER', 'DATA_MANAGEMENT_PLAN', 'JOURNAL_ARTICLE', 'PATENT', 'PREPRINT', 'PROJECT_DELIVERABLE', 'PROJECT_MILESTONE', 'PROPOSAL', 'REPORT', 'SOFTWARE_DOCUMENTATION', 'TAXONOMIC_TREATMENT', 'TECHNICAL_NOTE', 'THESIS', 'WORKING_PAPER', 'OTHER', name='publicationtype'), nullable=False),
            sa.Column('publication_doi', sa.String(length=120), nullable=True),
            sa.Column('tags', sa.String(length=120), nullable=True),
            sa.Column('uvl_version', sa.String(length=120), nullable=True),
            sa.Column('fm_metrics_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['fm_metrics_id'], ['fm_metrics.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'user_profile' not in inspector.get_table_names():
        op.create_table(
            'user_profile',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('orcid', sa.String(length=19), nullable=True),
            sa.Column('affiliation', sa.String(length=100), nullable=True),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('surname', sa.String(length=100), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id')
        )

    if 'author' not in inspector.get_table_names():
        op.create_table(
            'author',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=120), nullable=False),
            sa.Column('affiliation', sa.String(length=120), nullable=True),
            sa.Column('orcid', sa.String(length=120), nullable=True),
            sa.Column('ds_meta_data_id', sa.Integer(), nullable=True),
            sa.Column('fm_meta_data_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['ds_meta_data_id'], ['ds_meta_data.id'], ),
            sa.ForeignKeyConstraint(['fm_meta_data_id'], ['fm_meta_data.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'data_set' not in inspector.get_table_names():
        op.create_table(
            'data_set',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('ds_meta_data_id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['ds_meta_data_id'], ['ds_meta_data.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'ds_download_record' not in inspector.get_table_names():
        op.create_table(
            'ds_download_record',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('dataset_id', sa.Integer(), nullable=True),
            sa.Column('download_date', sa.DateTime(), nullable=False),
            sa.Column('download_cookie', sa.String(length=36), nullable=False),
            sa.ForeignKeyConstraint(['dataset_id'], ['data_set.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'ds_view_record' not in inspector.get_table_names():
        op.create_table(
            'ds_view_record',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('dataset_id', sa.Integer(), nullable=True),
            sa.Column('view_date', sa.DateTime(), nullable=False),
            sa.Column('view_cookie', sa.String(length=36), nullable=False),
            sa.ForeignKeyConstraint(['dataset_id'], ['data_set.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'feature_model' not in inspector.get_table_names():
        op.create_table(
            'feature_model',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('data_set_id', sa.Integer(), nullable=False),
            sa.Column('fm_meta_data_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['data_set_id'], ['data_set.id'], ),
            sa.ForeignKeyConstraint(['fm_meta_data_id'], ['fm_meta_data.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'file' not in inspector.get_table_names():
        op.create_table(
            'file',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=120), nullable=False),
            sa.Column('checksum', sa.String(length=120), nullable=False),
            sa.Column('size', sa.Integer(), nullable=False),
            sa.Column('feature_model_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['feature_model_id'], ['feature_model.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'file_download_record' not in inspector.get_table_names():
        op.create_table(
            'file_download_record',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('file_id', sa.Integer(), nullable=True),
            sa.Column('download_date', sa.DateTime(), nullable=False),
            sa.Column('download_cookie', sa.String(length=36), nullable=False),
            sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    if 'file_view_record' not in inspector.get_table_names():
        op.create_table(
            'file_view_record',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('file_id', sa.Integer(), nullable=False),
            sa.Column('view_date', sa.DateTime(), nullable=True),
            sa.Column('view_cookie', sa.String(length=36), nullable=True),
            sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_view_record')
    op.drop_table('file_download_record')
    op.drop_table('file')
    op.drop_table('feature_model')
    op.drop_table('ds_view_record')
    op.drop_table('ds_download_record')
    op.drop_table('data_set')
    op.drop_table('author')
    op.drop_table('user_profile')
    op.drop_table('fm_meta_data')
    op.drop_table('ds_meta_data')
    op.drop_table('zenodo')
    op.drop_table('user')
    op.drop_table('fm_metrics')
    op.drop_table('ds_metrics')
    # ### end Alembic commands ###
