import homekeeper.config
import homekeeper.test_case
import json
import pytest


class TestConfig(homekeeper.test_case.TestCase):
    @pytest.fixture
    def os(self):
        return self.os

    def setup_method(self):
        super(TestConfig, self).setup_method()
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.config = homekeeper.config.Config()
        self.config_path = self.os.path.join(self.home(), '.homekeeper.json')

    def test_load(self, os):
        base_directory = os.path.join(self.home(), 'base')
        dotfiles_directory = os.path.join(self.home(), 'dotfiles')
        excludes = ['.git']
        data = {
            'base_directory': base_directory,
            'dotfiles_directory': dotfiles_directory,
            'excludes': excludes
        }
        self.fs.CreateFile(self.config_path, contents=json.dumps(data))
        self.config.load(self.config_path)
        assert base_directory == self.config.base_directory
        assert dotfiles_directory == self.config.dotfiles_directory
        assert excludes == self.config.excludes
        assert self.config.override

    def test_load_with_defaults(self, os):
        dotfiles_directory = os.path.join(self.home(), 'dotfiles')
        self.fs.CreateFile(self.config_path, contents=json.dumps({}))
        self.config.load(self.config_path)
        assert not self.config.base_directory
        assert dotfiles_directory == self.config.dotfiles_directory
        assert [] == self.config.excludes
        assert not self.config.override

    def test_save(self, os):
        self.setup_directory(os.path.dirname(self.config_path))
        self.config.base_directory = None
        self.config.dotfiles_directory = os.path.join(self.home(), 'custom')
        self.config.excludes = ['.idea']
        self.config.override = False
        self.config.save(self.config_path)
        with self.fopen(self.config_path, 'r') as f:
            data = json.loads(f.read())
            assert data['base_directory'] == self.config.base_directory
            assert data['dotfiles_directory'] == self.config.dotfiles_directory
            assert data['excludes'] == self.config.excludes
            assert 'override' not in data
