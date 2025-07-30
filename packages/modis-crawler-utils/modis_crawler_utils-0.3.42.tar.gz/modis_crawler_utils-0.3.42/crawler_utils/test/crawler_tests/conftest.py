def pytest_addoption(parser):
    parser.addoption("--mock-mode", action="store_const", const=True, default=None)
    parser.addoption("--input-dir", action="store", help="Input directory for tests", default="./")
