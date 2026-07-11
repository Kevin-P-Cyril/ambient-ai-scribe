import sys, traceback
try:
    import main
    print('IMPORT_OK')
except Exception:
    traceback.print_exc()
    sys.exit(1)
