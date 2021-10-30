import pkg_resources

def version():
    """
    entry point for --version
    """
    print(
        "version pypodo : "
        + pkg_resources.get_distribution("pypodo").version
    )