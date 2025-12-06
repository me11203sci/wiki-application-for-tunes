"""Execution entry point for the `waft` application.

Todo.
"""

from textual.app import App

from application import Application

if __name__ == "__main__":
    application: App = Application()
    application.run()
