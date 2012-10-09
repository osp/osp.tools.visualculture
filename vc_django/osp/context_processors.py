import settings

def compress_enabled(context):
    return {'COMPRESS_ENABLED': settings.COMPRESS_ENABLED}
