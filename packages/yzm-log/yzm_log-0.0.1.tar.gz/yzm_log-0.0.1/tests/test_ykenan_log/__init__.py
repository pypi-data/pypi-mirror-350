# -*- coding: utf-8 -*-

from yzm_log import Logger


class TestLog:

    def test_info(self):
        log = Logger("Test log", is_form_file=False)
        log.info("Test log info")
