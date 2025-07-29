import uuid


def objs2uuid(*obj):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, "".join([str(x) for x in obj]))).replace("-", "").upper()


def myuuid():
    return str(uuid.uuid4()).replace("-", "").upper()
