from rucio.common.config import config_get_bool
from rucio.tests.common_server import get_vo
from rucio.core.replica import add_replica, get_replica
from rucio.common.types import InternalAccount, InternalScope

def generator(prefix=None, suffix=None):
    import uuid
    u = uuid.uuid4().hex()[:4]
    if prefix: u = prefix + "_" + u
    if suffix: u = u + "_" + suffix
    return u

def create_files(nrfiles, scope, rse_id, bytes_=1):
    """
    Creates a number of test files and add replicas to rse

    :param nrfiles:  Number of files to create
    :param scope:    Scope to create the files in
    :param rse_id:   RSE to add the replica to
    :param bytes_:    Bytes of each file
    :returns:        List of dict
    """
    if config_get_bool('common', 'multi_vo', raise_exception=False, default=False):
        vo = {'vo': get_vo()}
    else:
        vo = {}

    files = []
    jdoe = InternalAccount('jdoe', **vo)
    for i in range(nrfiles):
        file = generator('file')
        if isinstance(rse_id, list):
            for r in rse_id:
                add_replica(rse_id=r, scope=scope, name=file, bytes_=bytes_, account=jdoe)
        else:
            add_replica(rse_id=rse_id, scope=scope, name=file, bytes_=bytes_, account=jdoe)
        files.append({'scope': scope, 'name': file, 'bytes': bytes_})
    return files
