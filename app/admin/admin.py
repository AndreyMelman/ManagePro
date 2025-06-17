from sqladmin import (
    Admin,
    ModelView,
)

from core.models import (
    User,
    Team,
    Evaluation,
    TaskComment,
    Meeting,
    Task,
)
from core.models import db_helper
from core.schemas.task import TaskStatus


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.is_active,
        User.is_superuser,
        User.role,
    ]
    column_searchable_list = [User.email]
    column_sortable_list = [
        User.id,
        User.email,
        User.role,
        User.created_at,
        User.updated_at,
    ]
    column_details_exclude_list = [User.hashed_password]
    column_formatters = {
        User.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    form_columns = [User.email, User.role, User.team_id]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-user"


class TeamAdmin(ModelView, model=Team):
    column_list = [
        Team.id,
        Team.name,
        Team.description,
        Team.code,
        Team.admin_id,
        Team.created_at,
    ]
    column_searchable_list = [
        Team.name,
        Team.code,
    ]
    column_sortable_list = [
        Team.id,
        Team.name,
        Team.created_at,
    ]
    column_formatters = {
        Team.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    form_columns = [
        Team.name,
        Team.description,
        Team.code,
        Team.admin_id,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-users"


class TaskAdmin(ModelView, model=Task):
    column_list = [
        Task.id,
        Task.title,
        Task.status,
        Task.deadline,
        Task.creator_id,
        Task.assignee_id,
        Task.team_id,
        Task.created_at,
    ]
    column_searchable_list = [Task.title]
    column_sortable_list = [
        Task.id,
        Task.title,
        Task.status,
        Task.deadline,
        Task.created_at,
    ]
    column_formatters = {
        Task.deadline: lambda m, a: (
            m.deadline.strftime("%Y-%m-%d %H:%M:%S") if m.deadline else None
        ),
        Task.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    form_columns = [
        Task.title,
        Task.description,
        Task.deadline,
        Task.status,
        Task.creator_id,
        Task.assignee_id,
        Task.team_id,
    ]
    form_choices = {"status": [(status.value, status.value) for status in TaskStatus]}
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-tasks"


class MeetingAdmin(ModelView, model=Meeting):
    column_list = [
        Meeting.id,
        Meeting.title,
        Meeting.start_datetime,
        Meeting.end_datetime,
        Meeting.organizer_id,
        Meeting.team_id,
        Meeting.is_cancelled,
        Meeting.created_at,
    ]
    column_searchable_list = [Meeting.title]
    column_sortable_list = [
        Meeting.id,
        Meeting.title,
        Meeting.start_datetime,
        Meeting.created_at,
    ]
    column_formatters = {
        Meeting.start_datetime: lambda m, a: m.start_datetime.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        Meeting.end_datetime: lambda m, a: m.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        Meeting.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    form_columns = [
        Meeting.title,
        Meeting.description,
        Meeting.start_datetime,
        Meeting.end_datetime,
        Meeting.organizer_id,
        Meeting.team_id,
        Meeting.is_cancelled,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-calendar"


class TaskCommentAdmin(ModelView, model=TaskComment):
    column_list = [
        TaskComment.id,
        TaskComment.content,
        TaskComment.task_id,
        TaskComment.user_id,
        TaskComment.created_at,
    ]
    column_searchable_list = [TaskComment.content]
    column_sortable_list = [
        TaskComment.id,
        TaskComment.task_id,
        TaskComment.created_at,
    ]
    column_formatters = {
        TaskComment.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    form_columns = [
        TaskComment.content,
        TaskComment.task_id,
        TaskComment.user_id,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-comment"


class EvaluationAdmin(ModelView, model=Evaluation):
    column_list = [
        Evaluation.id,
        Evaluation.score,
        Evaluation.comment,
        Evaluation.task_id,
        Evaluation.evaluator_id,
        Evaluation.user_id,
        Evaluation.created_at,
    ]
    column_searchable_list = [Evaluation.comment]
    column_sortable_list = [
        Evaluation.id,
        Evaluation.score,
        Evaluation.created_at,
    ]
    column_formatters = {
        Evaluation.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    form_columns = [
        Evaluation.score,
        Evaluation.comment,
        Evaluation.task_id,
        Evaluation.evaluator_id,
        Evaluation.user_id,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    icon = "fa-solid fa-star"


def setup_admin(app):
    admin = Admin(app, db_helper.engine)
    admin.add_view(UserAdmin)
    admin.add_view(TeamAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(MeetingAdmin)
    admin.add_view(TaskCommentAdmin)
    admin.add_view(EvaluationAdmin)
