from django.test import TestCase

# Create your tests here.
from users.tasks import test
if __name__ == '__main__':
    test.deplay()
