import logging


def logger_config(log_level):
    """Logger settings

    Args:
        log_level (int): log level
    """
    # logging settings
    logging_level = log_level
    main_logger = logging.getLogger()
    main_logger.setLevel(logging_level)

    # ignore logs
    ignore_logs = []
    for ignore_log in ignore_logs:
        logging.getLogger(ignore_log).setLevel(logging.ERROR)

    # stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging_level)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s %(lineno)s: %(message)s"
    )
    stream_handler.setFormatter(formatter)

    # Add handler to logger
    main_logger.addHandler(stream_handler)
    return main_logger
