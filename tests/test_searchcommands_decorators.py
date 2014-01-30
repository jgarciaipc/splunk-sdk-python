#!/usr/bin/env python
#
# Copyright 2011-2013 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from splunklib.searchcommands.search_command_internals import SearchCommandParser
from splunklib.searchcommands import Configuration, StreamingCommand

import logging

@Configuration()
class SearchCommand(StreamingCommand):

    def stream(self, records):
        pass


class TestSearchCommandsDecorators(unittest.TestCase):

    def setUp(self):
        super(TestSearchCommandsDecorators, self).setUp()
        return

    def test_builtin_options(self):

        # logging_level accepts all logging levels and returns their canonical
        # string values

        warning = logging.getLevelName(logging.WARNING)
        notset = logging.getLevelName(logging.NOTSET)
        command = SearchCommand()

        self.assertEquals(command.logging_level, warning)

        for level in logging._levelNames:
            if type(level) is int:
                command.logging_level = level
                level_name = logging.getLevelName(level)
                self.assertEquals(command.logging_level, warning if level_name == notset else level_name)
            else:
                level_name = logging.getLevelName(logging.getLevelName(level))
                for variant in level, level.lower(), level.capitalize():
                    command.logging_level = variant
                    self.assertEquals(command.logging_level, warning if level_name == notset else level_name)

        # show_configuration accepts Splunk boolean values

        boolean_values = {
            '0': False, '1': True,
            'f': False, 't': True,
            'n': False, 'y': True,
            'no': False, 'yes': True,
            'false': False, 'true': True}

        for value in boolean_values:
            for variant in [value, value.capitalize(), value.upper()]:
                command.show_configuration = variant
                self.assertEquals(command.show_configuration, boolean_values[value])

        for value in 'any-other-string', 13:
            try:
                command.show_configuration = value
            except ValueError:
                pass
            except Exception as e:
                self.fail('Expected ValueError, but a %s was raised' % type(e))
            else:
                self.fail('Expected ValueError, but show_configuration=%s' % command.show_configuration)

        # SearchCommandParser recognizes each built-in option

        for argv in ['logging_level=DEBUG'], ['show_configuration=true']:
            parser = SearchCommandParser()
            parser.parse(argv, command)

        return
