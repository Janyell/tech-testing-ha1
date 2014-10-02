import unittest
import mock
from source.lib import utils


class LibUtilsTestCase(unittest.TestCase):

    #daemonize
        #positive_tests
    def test_daemonize_parent(self):
        pid = 42
        with mock.patch('os.fork', mock.Mock(return_value=pid)) as os_fork:
            with mock.patch('os._exit', mock.Mock()) as os_exit:
                utils.daemonize()

        os_fork.assert_called_once_with()
        os_exit.assert_called_once_with(0)

    def test_daemonize_child_child(self):
        pid = 0
        with mock.patch('os.fork', mock.Mock(return_value=pid)) as os_fork:
            with mock.patch('os.setsid', mock.Mock()) as os_setsid:
                with mock.patch('os._exit', mock.Mock()) as os_exit:
                    utils.daemonize()

        os_setsid.assert_called_once_with()
        assert os_fork.called
        assert not os_exit.called

    def test_daemonize_child_parent(self):
        child_pid = 0
        parent_pid = 42
        with mock.patch('os.fork', mock.Mock(side_effect=[child_pid, parent_pid])):
            with mock.patch('os.setsid', mock.Mock()):
                with mock.patch('os._exit', mock.Mock()) as os_exit:
                    utils.daemonize()

        os_exit.assert_called_once_with(0)

        #negative_tests
    def test_daemonize_oserror(self):
        exc = OSError("err")
        with mock.patch('os.fork', mock.Mock(side_effect=exc)):
            self.assertRaises(Exception, utils.daemonize)

    def test_daemonize_child_oserror(self):
        pid = 0
        exc = OSError("err")
        with mock.patch('os.fork', mock.Mock(side_effect=[pid, exc])):
            with mock.patch('os._exit', mock.Mock()):
                with mock.patch('os.setsid', mock.Mock()):
                    self.assertRaises(Exception, utils.daemonize)

    #create_pidfile(pidfile_path)
        #positive_tests
    def test_create_pidfile(self):
        pid = 42
        pidfile = '/file/path'
        m_open = mock.mock_open()
        with mock.patch('source.lib.utils.open', m_open, create=True):
            with mock.patch('os.getpid', mock.Mock(return_value=pid)):
                utils.create_pidfile(pidfile)

        m_open.assert_called_once_with(pidfile, 'w')
        m_open().write.assert_called_once_with(str(pid))

    #load_config_from_pyfile(filepath)
        #positive_tests
    def test_load_config_from_pyfile(self):
        result = utils.load_config_from_pyfile('source/tests/test_config.py')
        self.assertEqual(result.TEST_KEY_1, 1)
        self.assertEqual(result.TEST_KEY_2, 'test_value_2')
        self.assertEqual(result.TEST_KEY_3, {
            'test_key_3_1': 'test_value_3_1',
            'test_key_3_2': 'test_value_3_2'
        })
        self.assertEqual(result.TEST_KEY_4, '')
        self.assertFalse(hasattr(result, 'test_key_5'))

    #parse_cmd_args(args, app_description='')
        #positive_tests
    #def test_parse_cmd_args(self):
