"""notification center

Revision ID: 61ded0c8fbf6
Revises: f20aa8756612
Create Date: 2023-01-11 19:24:20.511853+00:00

"""
from alembic import op
import sqlalchemy as sa

import bugcode

# revision identifiers, used by Alembic.
revision = '61ded0c8fbf6'
down_revision = 'dd3181b9b3e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_notification',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', bugcode.server.fields.JSONType(), nullable=False),
    sa.Column('processed', sa.Boolean(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('update_user_id', sa.Integer(), nullable=True),
    sa.Column('verbose', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['bugcode_user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['update_user_id'], ['bugcode_user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_notification',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('extra_data', bugcode.server.fields.JSONType(), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('subtype', sa.String(), nullable=False),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('update_user_id', sa.Integer(), nullable=True),
    sa.Column('triggered_by', bugcode.server.fields.JSONType(), nullable=False),
    sa.Column('links_to', bugcode.server.fields.JSONType(), nullable=True),
    sa.Column('event_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['bugcode_user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['update_user_id'], ['bugcode_user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['bugcode_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_notification_user_id'), 'user_notification', ['user_id'], unique=False)
    op.create_table('user_notification_settings',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('paused', sa.Boolean(), nullable=False),
    sa.Column('slack_id', sa.String(), nullable=True),
    sa.Column('no_self_notify', sa.Boolean(), nullable=False),
    sa.Column('agents_enabled', sa.Boolean(), nullable=False),
    sa.Column('agents_app', sa.Boolean(), nullable=False),
    sa.Column('agents_email', sa.Boolean(), nullable=False),
    sa.Column('agents_slack', sa.Boolean(), nullable=False),
    sa.Column('cli_enabled', sa.Boolean(), nullable=False),
    sa.Column('cli_app', sa.Boolean(), nullable=False),
    sa.Column('cli_email', sa.Boolean(), nullable=False),
    sa.Column('cli_slack', sa.Boolean(), nullable=False),
    sa.Column('comments_enabled', sa.Boolean(), nullable=False),
    sa.Column('comments_app', sa.Boolean(), nullable=False),
    sa.Column('comments_email', sa.Boolean(), nullable=False),
    sa.Column('comments_slack', sa.Boolean(), nullable=False),
    sa.Column('hosts_enabled', sa.Boolean(), nullable=False),
    sa.Column('hosts_app', sa.Boolean(), nullable=False),
    sa.Column('hosts_email', sa.Boolean(), nullable=False),
    sa.Column('hosts_slack', sa.Boolean(), nullable=False),
    sa.Column('users_enabled', sa.Boolean(), nullable=False),
    sa.Column('users_app', sa.Boolean(), nullable=False),
    sa.Column('users_email', sa.Boolean(), nullable=False),
    sa.Column('users_slack', sa.Boolean(), nullable=False),
    sa.Column('reports_enabled', sa.Boolean(), nullable=False),
    sa.Column('reports_app', sa.Boolean(), nullable=False),
    sa.Column('reports_email', sa.Boolean(), nullable=False),
    sa.Column('reports_slack', sa.Boolean(), nullable=False),
    sa.Column('vulnerabilities_enabled', sa.Boolean(), nullable=False),
    sa.Column('vulnerabilities_app', sa.Boolean(), nullable=False),
    sa.Column('vulnerabilities_email', sa.Boolean(), nullable=False),
    sa.Column('vulnerabilities_slack', sa.Boolean(), nullable=False),
    sa.Column('workspaces_enabled', sa.Boolean(), nullable=False),
    sa.Column('workspaces_app', sa.Boolean(), nullable=False),
    sa.Column('workspaces_email', sa.Boolean(), nullable=False),
    sa.Column('workspaces_slack', sa.Boolean(), nullable=False),
    sa.Column('pipelines_enabled', sa.Boolean(), nullable=False),
    sa.Column('pipelines_app', sa.Boolean(), nullable=False),
    sa.Column('pipelines_email', sa.Boolean(), nullable=False),
    sa.Column('pipelines_slack', sa.Boolean(), nullable=False),
    sa.Column('executive_reports_enabled', sa.Boolean(), nullable=False),
    sa.Column('executive_reports_app', sa.Boolean(), nullable=False),
    sa.Column('executive_reports_email', sa.Boolean(), nullable=False),
    sa.Column('executive_reports_slack', sa.Boolean(), nullable=False),
    sa.Column('planner_enabled', sa.Boolean(), nullable=False),
    sa.Column('planner_app', sa.Boolean(), nullable=False),
    sa.Column('planner_email', sa.Boolean(), nullable=False),
    sa.Column('planner_slack', sa.Boolean(), nullable=False),
    sa.Column('integrations_enabled', sa.Boolean(), nullable=False),
    sa.Column('integrations_app', sa.Boolean(), nullable=False),
    sa.Column('integrations_email', sa.Boolean(), nullable=False),
    sa.Column('integrations_slack', sa.Boolean(), nullable=False),
    sa.Column('other_enabled', sa.Boolean(), nullable=False),
    sa.Column('other_app', sa.Boolean(), nullable=False),
    sa.Column('other_email', sa.Boolean(), nullable=False),
    sa.Column('other_slack', sa.Boolean(), nullable=False),
    sa.Column('adv_high_crit_vuln', sa.Boolean(), nullable=False),
    sa.Column('adv_risk_score_threshold', sa.Integer(), nullable=False),
    sa.Column('adv_vuln_open_days', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('update_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['bugcode_user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['update_user_id'], ['bugcode_user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['bugcode_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_notification_settings')
    op.drop_index(op.f('ix_user_notification_user_id'), table_name='user_notification')
    op.drop_table('user_notification')
    op.drop_table('base_notification')
    # ### end Alembic commands ###
