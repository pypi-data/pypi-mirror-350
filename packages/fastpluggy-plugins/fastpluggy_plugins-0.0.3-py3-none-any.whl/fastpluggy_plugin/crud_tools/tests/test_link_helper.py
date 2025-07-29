import pytest

from tests.fake_app.domains.fake_module.models import UsersTestModeSQLAlchemyl
from fastpluggy.core.view_builer.components.button import ButtonView
from fastpluggy.core.view_builer.link_helper import LinkHelper


def test_link_helper_not_exist():
    with pytest.raises(ValueError, match="Invalid action"):
        LinkHelper.get_crud_link('model', 'not_exit_action')


def test_link_helper_exist():
    link = LinkHelper.get_crud_link('model', 'view')
    result = LinkHelper.link_has_label(link, "View")
    assert result is True

def test_link_helper_sqlalchemy_class():
    link = LinkHelper.get_crud_link(UsersTestModeSQLAlchemyl, 'create')
    assert link['url'] == f'/admin/crud/{UsersTestModeSQLAlchemyl.__name__}/create'

def test_link_helper_exist_object():
    link = LinkHelper.get_crud_link('model', 'view')
    button_view = ButtonView(**link)
    result = LinkHelper.link_has_label(button_view, "View")
    assert result is True
