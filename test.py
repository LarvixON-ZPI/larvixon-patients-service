import logging

# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
logging.basicConfig()

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
logging.root.setLevel(logging.NOTSET)

# The following line sets the root logger level as well.
# It's equivalent to both previous statements combined:
logging.basicConfig(level=logging.NOTSET)


# You can either share the `logger` object between all your files or the
# name handle (here `my-app`) and call `logging.getLogger` with it.
# The result is the same.
handle = "my-app"
logger1 = logging.getLogger(handle)
logger2 = logging.getLogger(handle)
# logger1 and logger2 point to the same object:
# (logger1 is logger2) == True

logger = logging.getLogger("my-app")
# Convenient methods in order of verbosity from highest to lowest
logger.debug("this will get printed")
logger.info("this will get printed")
logger.warning("this will get printed")
logger.error("this will get printed")
logger.critical("this will get printed")


# In large applications where you would like more control over the logging,
# create sub-loggers from your main application logger.
component_logger = logger.getChild("component-a")
component_logger.info("this will get printed with the prefix `my-app.component-a`")

# If you wish to control the logging levels, you can set the level anywhere
# in the hierarchy:
#
# - root
#   - my-app
#     - component-a
#

# Example for development:
logger.setLevel(logging.DEBUG)

# If that prints too much, enable debug printing only for your component:
component_logger.setLevel(logging.DEBUG)


# For production you rather want:
logger.setLevel(logging.WARNING)
