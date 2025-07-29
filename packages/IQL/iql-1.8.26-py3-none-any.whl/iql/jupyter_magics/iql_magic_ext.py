def load_ipython_extension(ip):
    """Defer imports for non-ipython environments"""
    from IPython.core.getipython import get_ipython

    from .iql_magic import IqlMagic

    ip = get_ipython()
    ip.register_magics(IqlMagic)  # type: ignore
