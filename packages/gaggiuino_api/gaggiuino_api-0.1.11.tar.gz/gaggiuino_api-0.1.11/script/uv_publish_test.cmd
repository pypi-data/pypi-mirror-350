
@echo off
call secrets.cmd

call %~dp0\uv_publish.cmd --username=__token__ --password=%PYPI_TEST_TOKEN% --publish-url=https://test.pypi.org/legacy/
