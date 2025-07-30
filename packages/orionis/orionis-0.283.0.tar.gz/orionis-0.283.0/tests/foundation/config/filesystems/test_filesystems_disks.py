from orionis.foundation.config.filesystems.entitites.aws import S3
from orionis.foundation.config.filesystems.entitites.disks import Disks
from orionis.foundation.config.filesystems.entitites.local import Local
from orionis.foundation.config.filesystems.entitites.public import Public
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigDisks(TestCase):
    """
    Test cases for the Disks filesystem configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Disks instance is created with correct default values.
        Verifies all default disk configurations are properly initialized.
        """
        disks = Disks()
        self.assertIsInstance(disks.local, Local)
        self.assertIsInstance(disks.public, Public)
        self.assertIsInstance(disks.aws, S3)

    async def testLocalTypeValidation(self):
        """
        Test local attribute type validation.
        Verifies that only Local instances are accepted for local attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Disks(local="not_a_local_instance")
        with self.assertRaises(OrionisIntegrityException):
            Disks(local=123)
        with self.assertRaises(OrionisIntegrityException):
            Disks(local=None)

    async def testPublicTypeValidation(self):
        """
        Test public attribute type validation.
        Verifies that only Public instances are accepted for public attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Disks(public="not_a_public_instance")
        with self.assertRaises(OrionisIntegrityException):
            Disks(public=123)
        with self.assertRaises(OrionisIntegrityException):
            Disks(public=None)

    async def testAwsTypeValidation(self):
        """
        Test aws attribute type validation.
        Verifies that only S3 instances are accepted for aws attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Disks(aws="not_an_s3_instance")
        with self.assertRaises(OrionisIntegrityException):
            Disks(aws=123)
        with self.assertRaises(OrionisIntegrityException):
            Disks(aws=None)

    async def testCustomDiskConfigurations(self):
        """
        Test that custom disk configurations are properly stored and validated.
        Verifies custom disk configurations are correctly handled.
        """
        custom_local = Local(path="custom/local/path")
        custom_public = Public(path="custom/public/path", url="assets")
        custom_aws = S3(bucket="custom-bucket", region="eu-west-1")

        disks = Disks(
            local=custom_local,
            public=custom_public,
            aws=custom_aws
        )

        self.assertEqual(disks.local.path, "custom/local/path")
        self.assertEqual(disks.public.path, "custom/public/path")
        self.assertEqual(disks.public.url, "assets")
        self.assertEqual(disks.aws.bucket, "custom-bucket")
        self.assertEqual(disks.aws.region, "eu-west-1")

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies all disk configurations are correctly included in dictionary.
        """
        disks = Disks()
        disks_dict = disks.toDict()

        self.assertIsInstance(disks_dict, dict)
        self.assertIsInstance(disks_dict['local'], dict)
        self.assertIsInstance(disks_dict['public'], dict)
        self.assertIsInstance(disks_dict['aws'], dict)

    async def testHashability(self):
        """
        Test that Disks maintains hashability due to unsafe_hash=True.
        Verifies that Disks instances can be used in sets and as dictionary keys.
        """
        disks1 = Disks()
        disks2 = Disks()
        disks_set = {disks1, disks2}

        self.assertEqual(len(disks_set), 1)

        custom_disks = Disks(local=Local(path="custom/path"))
        disks_set.add(custom_disks)
        self.assertEqual(len(disks_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Disks enforces keyword-only initialization.
        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Disks(Local(), Public(), S3())