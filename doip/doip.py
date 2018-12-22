class DoIP_Protocol(object):

    TCP_DATA = 13400                        #[DoIP-001]
    UDP_DISCOVERY = 13400                   #[DoIP-008]
    UDP_TEST_EQUIPMENT_REQUEST = 0          #[DoIP-135], dynamically assigned

    def __init__(self):
        print("""I'm DOIP""")