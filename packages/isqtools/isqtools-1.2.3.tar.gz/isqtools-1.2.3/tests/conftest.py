def pytest_addoption(parser):
    parser.addoption(
        "--run-tianyan",
        action="store_true",
        default=False,
        help="Run tests that require TianyBackend",
    )
