import unittest
import mock
from source.lib import worker


class LibWorkerTestCase(unittest.TestCase):
    # get_redirect_history_from_task(task, timeout, max_redirects=30, user_agent=None)
    #positive_tests
    def test_get_redirect_history_from_task_error_and_not_recheck(self):
        task = mock.Mock()
        task.data = {
            'url': 'url',
            'recheck': False,
            'url_id': 'url_id',
            'suspicious': 'suspicious'
        }
        is_input = True
        data_modified = task.data.copy()
        data_modified['recheck'] = True
        timeout = 3
        with mock.patch(
                'source.lib.worker.get_redirect_history',
                mock.Mock(return_value=(['ERROR'], [], []))
        ) as get_redirect_history:
            self.assertEquals((is_input, data_modified), (worker.get_redirect_history_from_task(task, timeout)))

        get_redirect_history.assert_called_once()

    def test_get_redirect_history_from_task_else(self):
        task = mock.Mock()
        task.data = {
            'url': 'url',
            'recheck': True,
            'url_id': 'url_id'
        }
        return_value = [['ERROR'], [], []]
        is_input = False
        data_modified = {
            'url_id': task.data['url_id'],
            'result': return_value,
            'check_type': 'normal'
        }
        timeout = 3
        with mock.patch('source.lib.worker.get_redirect_history', mock.Mock(return_value=return_value)):
            self.assertEquals((is_input, data_modified), worker.get_redirect_history_from_task(task, timeout))

    def test_get_redirect_history_from_task_else_suspicious(self):
        task = mock.Mock()
        task.data = {
            'url': 'url',
            'recheck': False,
            'url_id': 'url_id',
            'suspicious': 'suspicious'
        }
        return_value = [[], [], []]
        is_input = False
        data_modified = {
            'url_id': task.data['url_id'],
            'result': return_value,
            'check_type': 'normal',
            'suspicious': task.data['suspicious']
        }
        timeout = 3
        with mock.patch('source.lib.worker.get_redirect_history', mock.Mock(return_value=return_value)):
            self.assertEquals((is_input, data_modified), worker.get_redirect_history_from_task(task, timeout))

            #worker(config, parent_pid)
            #positive_tests

    def test_worker_dead_parent(self):
        config = mock.MagicMock()
        parent_pid = 42
        tube = mock.MagicMock()
        with mock.patch('source.lib.worker.get_tube', tube):
            with mock.patch('os.path.exists', mock.Mock(return_value=False)):
                self.assertEquals(None, worker.worker(config, parent_pid))

    def test_worker_not_result(self):
        config = mock.MagicMock()
        parent_pid = 42
        tube = mock.MagicMock()
        with mock.patch('source.lib.worker.get_tube', tube):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])) as os_path_exists:
                with mock.patch('source.lib.worker.get_redirect_history_from_task',
                                mock.Mock(return_value=None)) as get_redirect_history_from_task:
                    self.assertEquals(None, worker.worker(config, parent_pid))
                    assert os_path_exists.call_count == 2
                    get_redirect_history_from_task.assert_called_once()

    def test_worker_result_is_input(self):
        config = mock.MagicMock()
        parent_pid = 42
        tube = mock.MagicMock()
        with mock.patch('source.lib.worker.get_tube', tube):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])) as os_path_exists:
                with mock.patch('source.lib.worker.get_redirect_history_from_task',
                                mock.Mock(return_value=['is_input', 'data'])) as get_redirect_history_from_task:
                    self.assertEquals(None, worker.worker(config, parent_pid))
                    assert os_path_exists.call_count == 2
                    get_redirect_history_from_task.assert_called_once()

    def test_worker_result_not_is_input(self):
        config = mock.MagicMock()
        parent_pid = 42
        tube = mock.MagicMock()
        with mock.patch('source.lib.worker.get_tube', tube):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])) as os_path_exists:
                with mock.patch('source.lib.worker.get_redirect_history_from_task',
                                mock.Mock(return_value=[None, 'data'])) as get_redirect_history_from_task:
                    self.assertEquals(None, worker.worker(config, parent_pid))
                    assert os_path_exists.call_count == 2
                    get_redirect_history_from_task.assert_called_once()

         #negative_tests
    def test_worker_not_result_database_error(self):
        from source.lib.worker import DatabaseError

        config = mock.MagicMock()
        parent_pid = 42
        tube = mock.MagicMock()
        tube.take = mock.MagicMock()
        tube.take.ack = mock.Mock(side_effect=DatabaseError)
        with mock.patch('source.lib.worker.get_tube', tube):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])) as os_path_exists:
                with mock.patch('source.lib.worker.get_redirect_history_from_task',
                                mock.Mock(return_value=None)) as get_redirect_history_from_task:
                    self.assertEquals(None, worker.worker(config, parent_pid))
                    assert os_path_exists.call_count == 2
                    get_redirect_history_from_task.assert_called_once()