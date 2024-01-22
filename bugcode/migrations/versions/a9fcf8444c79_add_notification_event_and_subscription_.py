"""add_notification_event_and_subscription_model

Revision ID: a9fcf8444c79
Revises: a4def820a5bb
Create Date: 2021-05-28 15:47:13.781453+00:00

"""
from alembic import op
import sqlalchemy as sa
from bogcode.server.fields import JSONType

# Added manually for inserts
from sqlalchemy import orm
from bogcode.server.models import (NotificationSubscription,
                                   NotificationSubscriptionWebSocketConfig,
                                   User)

# revision identifiers, used by Alembic.
revision = 'a9fcf8444c79'
down_revision = '97a9348d0406'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('async_event', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.execute('INSERT INTO event_type (name, async_event) VALUES (\'new_workspace\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_agent\', True)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_user\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_agentexecution\', True)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_executivereport\', True)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_vulnerability\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_command\', True)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_comment\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'update_workspace\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'update_agent\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'update_user\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'update_executivereport\', True)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'update_vulnerability\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'delete_workspace\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'delete_agent\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'delete_user\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'delete_executivereport\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'delete_vulnerability\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'new_vulnerabilityweb\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'update_vulnerabilityweb\', False)')
    op.execute('INSERT INTO event_type (name, async_event)  VALUES (\'delete_vulnerabilityweb\', False)')

    op.create_table('object_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.execute('INSERT INTO object_type ("name") VALUES (\'vulnerability\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'vulnerabilityweb\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'host\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'credential\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'service\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'source_code\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'comment\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'executivereport\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'workspace\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'task\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'agent\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'agentexecution\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'command\')')
    op.execute('INSERT INTO object_type ("name") VALUES (\'user\')')

    op.create_table('notification_subscription',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_type_id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('update_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['bogcode_user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['event_type_id'], ['event_type.id'], ),
    sa.ForeignKeyConstraint(['update_user_id'], ['bogcode_user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_subscription_event_type_id'), 'notification_subscription', ['event_type_id'], unique=False)
    op.create_table('notification_allowed_roles',
    sa.Column('notification_subscription_id', sa.Integer(), nullable=False),
    sa.Column('allowed_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['allowed_role_id'], ['bogcode_role.id'], ),
    sa.ForeignKeyConstraint(['notification_subscription_id'], ['notification_subscription.id'], )
    )
    op.create_table('notification_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_type_id', sa.Integer(), nullable=False),
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('object_type_id', sa.Integer(), nullable=False),
    sa.Column('notification_data', JSONType(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('workspace_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_type_id'], ['event_type.id'], ),
    sa.ForeignKeyConstraint(['object_type_id'], ['object_type.id'], ),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_event_event_type_id'), 'notification_event', ['event_type_id'], unique=False)
    op.create_index(op.f('ix_notification_event_object_type_id'), 'notification_event', ['object_type_id'], unique=False)
    op.create_index(op.f('ix_notification_event_workspace_id'), 'notification_event', ['workspace_id'], unique=False)
    op.create_table('notification_subscription_config_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.Integer(), nullable=False),
    sa.Column('role_level', sa.Boolean(), nullable=True),
    sa.Column('workspace_level', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('type', sa.String(length=24), nullable=True),
    sa.ForeignKeyConstraint(['subscription_id'], ['notification_subscription.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subscription_id', 'type', name='uix_subscriptionid_type')
    )
    op.create_index(op.f('ix_notification_subscription_config_base_subscription_id'), 'notification_subscription_config_base', ['subscription_id'], unique=False)
    op.create_table('notification_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('notification_event_id', sa.Integer(), nullable=False),
    sa.Column('notification_subscription_config_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=24), nullable=True),
    sa.ForeignKeyConstraint(['notification_event_id'], ['notification_event.id'], ),
    sa.ForeignKeyConstraint(['notification_subscription_config_id'], ['notification_subscription_config_base.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_base_notification_event_id'), 'notification_base', ['notification_event_id'], unique=False)
    op.create_index(op.f('ix_notification_base_notification_subscription_config_id'), 'notification_base', ['notification_subscription_config_id'], unique=False)
    op.create_table('notification_subscription_mail_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('user_notified_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['notification_subscription_config_base.id'], ),
    sa.ForeignKeyConstraint(['user_notified_id'], ['bogcode_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_subscription_mail_config_user_notified_id'), 'notification_subscription_mail_config', ['user_notified_id'], unique=False)
    op.create_table('notification_subscription_webhook_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['notification_subscription_config_base.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification_subscription_websocket_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_notified_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['notification_subscription_config_base.id'], ),
    sa.ForeignKeyConstraint(['user_notified_id'], ['bogcode_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_subscription_websocket_config_user_notified_id'), 'notification_subscription_websocket_config', ['user_notified_id'], unique=False)
    op.create_table('mail_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['notification_base.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('webhook_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['notification_base.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('websocket_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_notified_id', sa.Integer(), nullable=True),
    sa.Column('mark_read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['notification_base.id'], ),
    sa.ForeignKeyConstraint(['user_notified_id'], ['bogcode_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_websocket_notification_mark_read'), 'websocket_notification', ['mark_read'], unique=False)
    op.create_index(op.f('ix_websocket_notification_user_notified_id'), 'websocket_notification', ['user_notified_id'], unique=False)
    # ### end Alembic commands ###

    # Added manually for inserts
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    admin = User.ADMIN_ROLE
    pentester = User.PENTESTER_ROLE
    asset_owner = User.ASSET_OWNER_ROLE
    client = User.CLIENT_ROLE

    default_initial_notifications_config = [
        # Workspace
        {'roles': [admin], 'event_types': ['new_workspace', 'update_workspace', 'delete_workspace']},
        # Users
        {'roles': [admin], 'event_types': ['new_user', 'update_user', 'delete_user']},
        # Agents
        {'roles': [admin, pentester], 'event_types': ['new_agent', 'update_agent', 'delete_agent']},
        # Reports
        {'roles': [admin, pentester, asset_owner],
         'event_types': ['new_executivereport', 'update_executivereport', 'delete_executivereport']},
        # Agent execution
        {'roles': [admin, pentester, asset_owner], 'event_types': ['new_agentexecution']},
        # Commands
        {'roles': [admin, pentester, asset_owner], 'event_types': ['new_command']},
        # Vulnerability
        {'roles': [admin, pentester, asset_owner, client],
         'event_types': ['new_vulnerability', 'update_vulnerability', 'delete_vulnerability']},
        # Vulnerability Web
        {'roles': [admin, pentester, asset_owner, client],
         'event_types': ['new_vulnerabilityweb', 'update_vulnerabilityweb', 'delete_vulnerabilityweb']},
        # Comments
        {'roles': [admin, pentester, asset_owner, client], 'event_types': ['new_comment']},
    ]

    allowed_roles = sa.table(
        'notification_allowed_roles',
        sa.column('notification_subscription_id', sa.Integer),
        sa.column('allowed_role_id', sa.Integer)
    )

    res = bind.execute('SELECT name, id FROM event_type').fetchall()
    event_type_ids = dict(res)

    res = bind.execute('SELECT name, id FROM bogcode_role').fetchall()
    role_ids = dict(res)

    for config in default_initial_notifications_config:
        for event_type in config['event_types']:
            n = NotificationSubscription(event_type_id=event_type_ids[event_type])
            session.add(n)
            session.commit()
            ns = NotificationSubscriptionWebSocketConfig(subscription=n, active=True, role_level=True)
            session.add(ns)
            session.commit()
            for role_name in config['roles']:
                op.execute(
                    allowed_roles.insert().values({'notification_subscription_id': n.id, 'allowed_role_id': role_ids[role_name]})
                )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_websocket_notification_user_notified_id'), table_name='websocket_notification')
    op.drop_index(op.f('ix_websocket_notification_mark_read'), table_name='websocket_notification')
    op.drop_table('websocket_notification')
    op.drop_table('webhook_notification')
    op.drop_table('mail_notification')
    op.drop_index(op.f('ix_notification_subscription_websocket_config_user_notified_id'), table_name='notification_subscription_websocket_config')
    op.drop_table('notification_subscription_websocket_config')
    op.drop_table('notification_subscription_webhook_config')
    op.drop_index(op.f('ix_notification_subscription_mail_config_user_notified_id'), table_name='notification_subscription_mail_config')
    op.drop_table('notification_subscription_mail_config')
    op.drop_index(op.f('ix_notification_base_notification_subscription_config_id'), table_name='notification_base')
    op.drop_index(op.f('ix_notification_base_notification_event_id'), table_name='notification_base')
    op.drop_table('notification_base')
    op.drop_index(op.f('ix_notification_subscription_config_base_subscription_id'), table_name='notification_subscription_config_base')
    op.drop_table('notification_subscription_config_base')
    op.drop_index(op.f('ix_notification_event_workspace_id'), table_name='notification_event')
    op.drop_index(op.f('ix_notification_event_object_type_id'), table_name='notification_event')
    op.drop_index(op.f('ix_notification_event_event_type_id'), table_name='notification_event')
    op.drop_table('notification_event')
    op.drop_table('notification_allowed_roles')
    op.drop_index(op.f('ix_notification_subscription_event_type_id'), table_name='notification_subscription')
    op.drop_table('notification_subscription')
    op.drop_table('object_type')
    op.drop_table('event_type')
    # ### end Alembic commands ###
