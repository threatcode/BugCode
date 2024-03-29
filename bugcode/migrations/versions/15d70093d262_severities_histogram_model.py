"""Severities histogram model

Revision ID: 15d70093d262
Revises: d8f0b32a5c0e
Create Date: 2021-11-08 13:57:28.099487+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
# from sqlalchemy import func, case

# from bugcode.server.models import VulnerabilityGeneric, SeveritiesHistogram, Workspace

revision = '15d70093d262'
down_revision = 'd8f0b32a5c0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('severities_histogram',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workspace_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('medium', sa.Integer(), nullable=False),
    sa.Column('high', sa.Integer(), nullable=False),
    sa.Column('critical', sa.Integer(), nullable=False),
    sa.Column('confirmed', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_severities_histogram_workspace_id'), 'severities_histogram', ['workspace_id'], unique=False)
    # ### end Alembic commands ###

    # # Init histogram
    # bind = op.get_bind()
    # session = sa.orm.Session(bind=bind)
    # workspaces = session.query(Workspace).all()
    # for workspace in workspaces:
    #     vulnerabilities = session.query(VulnerabilityGeneric) \
    #         .with_entities(func.date_trunc('day', VulnerabilityGeneric.create_date),
    #                        VulnerabilityGeneric.severity,
    #                        func.count(VulnerabilityGeneric.severity),
    #                        func.sum(case([(VulnerabilityGeneric.confirmed, 1)], else_=0)))\
    #         .filter(VulnerabilityGeneric.workspace_id == workspace.id,
    #                 VulnerabilityGeneric.status.notin_(['closed', 'risk-accepted']),
    #                 VulnerabilityGeneric.severity.in_(['medium', 'high', 'critical']))\
    #         .group_by(func.date_trunc('day', VulnerabilityGeneric.create_date), VulnerabilityGeneric.severity).all()
    #     for histogram_date, severity_type, severity_count, confirmed_count in vulnerabilities:
    #         severity_histogram = session.query(SeveritiesHistogram)\
    #             .filter(SeveritiesHistogram.date == histogram_date,
    #                     SeveritiesHistogram.workspace_id == workspace.id).first()
    #         if severity_histogram is None:
    #             severity_histogram = SeveritiesHistogram(date=histogram_date, workspace=workspace, medium=0, high=0, critical=0, confirmed=0)
    #             session.add(severity_histogram)
    #             session.commit()
    #         if severity_type == 'medium':
    #             severity_histogram.medium = severity_count
    #         if severity_type == 'high':
    #             severity_histogram.high = severity_count
    #         if severity_type == 'critical':
    #             severity_histogram.critical = severity_count
    #         severity_histogram.confirmed += confirmed_count
    #     session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_severities_histogram_workspace_id'), table_name='severities_histogram')
    op.drop_table('severities_histogram')
    # ### end Alembic commands ###
