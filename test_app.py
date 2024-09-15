import unittest

from app import respond

class TestApp(unittest.TestCase):
    @unittest.skip("Too slow, skip for now")
    def test_respond_local_mode(self):
        # test call respond call
        for ret in respond(message="Please rpeat and only repeat what I say to you. 'HI'", history=[], use_local_model=True):
            self.assertTrue(ret is not None)

    def test_respond_api_mode(self):
        # test call respond call
        for ret in respond(message="Please rpeat and only repeat what I say to you. 'HI'", history=[], use_local_model=False):
            self.assertTrue(ret is not None)


if __name__ == "__main__":
    unittest.main()