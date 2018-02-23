from uuid import UUID
def is_valid_uuid(val, version=4):
    try:
        uuid_obj = UUID(val, version=version)
    except:
        return False
    return str(uuid_obj) == val