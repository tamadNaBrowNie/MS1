import logging


class DeadSessionException(Exception):
    def __init__(self, message = "Session Died", errors = None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
def timeout(req):
    logger = logging.getLogger('auth')
    if 'data' not in req.session:
        logger.info('user timed out')
        raise DeadSessionException