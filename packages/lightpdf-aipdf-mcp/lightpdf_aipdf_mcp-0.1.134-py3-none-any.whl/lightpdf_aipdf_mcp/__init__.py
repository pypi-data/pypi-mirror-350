from . import server

def main():
    """Main entry point for the package."""
    server.cli_main()

# 只导出main函数
__all__ = ['main']