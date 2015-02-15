import os
import sys
import traceback

sys.path.insert(0,
    os.path.join(os.path.dirname(__file__), '..'))


if __name__ == "__main__":
    from marmoset import Marmoset
    from marmoset.core.key import get_user_info

    username, password = get_user_info()
    m = Marmoset(username=username, password=password)

    try:
        a0 = m.fetch('cs246', 'A0P0')
        a1 = m.fetch('cs246', 'A1P1a')
    except Exception as e:
        print traceback.format_exc()
        print 'Test Failed'
        exit(1)
    print 'Test Passed'
