from unifide_backend.tests.test_base import TestBase


class CPTests(TestBase):
    def test_init_menu(self):
        from unifide_backend.action.cp.action import init_cp_menu

        init_cp_menu()