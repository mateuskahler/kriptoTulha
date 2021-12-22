import unittest

from crypto.keyring import \
    generate_key


class KeyDerivation(unittest.TestCase):
    def setUp(self):
        self.passwords = [
            b"such_a_secret_pass.!1s4d23",
            b"1910ehA232!SNJK#2P",
            b"98.zx&8A(9g08S(*ADb n ."
        ]

        self.salts = [
            b'\xa4\xc3\xc0\xe7\xbc*\xbf\xd5\xc6\xe6\x8f\xed\x00\xea\x0c|',
            b'\xdc\xd2I*\xf13\t\xc2\x06@$\xdd\xb7\x95\xc72',
            b'Q\xe1bJ+\xa9!\xad\xc2\xe88B\xce\x1f\xc0\xdf',
            b'O\xec\xea\xe3\xbc\xfb\x13\x8b\xe4q\xc6\xf5\xbcL\xe0o',
            b'\x10\xb9m~\xd92Ts\xefH\x873^D\x19V'
        ]

        self.keys = [
            [
                b"<\x04\xfdNO\xe0\xf5\xa6M\xf7\x00Q\x9b\x94\xe0'\xc9\x17\x01\x9a\xae\xf2U\x0fYgV\x9a\xba>f\xee",
                b'\xaa\xf1\x0ct\xc2Z[\x96\xed\x1e\x06\xfd\x8a\x92\x94\xcb\x08_\xaf%[#=\xcf\xf2JH\xd7 L\x94i',
                b'\xf3\xa0\x00\xe8>v\x8b\xfc\xa5\xe4`\xf4\x11)\x197\xe0*RT~\x93\xf9hho\x87\xbb\xd4\x1b\xd1\xb4',
                b'HL\x83\xf4\xf868\xc2Y\xdb\xacgD\xc0e\xf5K\x8d\xfc\xc9\xa1]\x98\x99~\x8c}\xf0n\x94i\xe9',
                b'{\x8c\x99\xd9\x84H\x02LQ|\xa5\x88y\xdb\x99G\xc3\x92\x80\xfbb\xa4uWx\xc8\x90F\xdf\x88\x86\x99'
            ],

            [
                b'\xd4\xa2*N\x12\\\x84\xfa\x86$\x91\xccp1?m\x91h}\xc6\x86\xf7\xae]\x17Q\xb0\xef\xa4B\xbdB',
                b'S\x08\x9a\x13\xd4\xf4\xaa\xaf\xa2\xb9\x19\x97\xfc\x15;8~/\x9aC\x828\x12\xd9\xa3\x1d_|\x0e\xf2\xf8?',
                b'\xd4\x01\x1e.\xdfC\xab\xea^\xc5\xa4\xe5\r\xa6\x87\x00x\xd3\xfc\xcc\x18.\x90?\x81-Q\x1f\xb9\xf2y\xfb',
                b'\xc5\xc6`\x88\xb8\xc6\xa6\xc7\xb4\x8b\tT|Zcn-\xa1>\xa5\xa6\xee\xa4.\x9cxf\xc9\x9b\n\xf0g',
                b'\x9a\x96\xa1\xc6\xa8\xb2nbv\x81[H\xedJ\xee\r\xbe\xf6Y\xe9c\xe0:\x14Y\xdep\xcd\xe7I\x03\xe3'
            ],

            [
                b'Lt\xff\xa4\x82\xbe\xa4\x7f{SC\xfb\x1a\xd6\x89\x93\xe5F\xd2\x9a\xf8\x1a\x08n\x05!\x06\xc8kd\x96*',
                b'\x16\xa4m\x14\x8ap\x90 {,\t#\x1bsYw\xb8rS\x80\xd8@^<\xa0b\t\x10\xd65\xe7?',
                b'2|\x08m0\x842[\x1a \x80\xd1\xe2\xca]{H\xaf\xf0CD\x16\xcf8X\x0b8\xb3\xd8$\xbe\x19',
                b'n\xf7\xf8\x0f\xe9\xba\x17\xf7\xd4\xc1\xf0~\xc7\xabff\xef\xa2\x01\x93\xa9\xeb\xf0_7p`z\xf5\x8d\x9e\x1e',
                b'w\x1c\xff\xa7\x90\x8cW\xce\xa8\x8e\x9c[\xfb\x9d\x8a\xe5\x04u\xcdf4\x05\x05t\xf4Je\x08\xd4XH\x82'
            ]
        ]

        return super().setUp()

    def test_key_generation(self):
        """
        Generate some keys using predefined passwords and salts. 
        Checks generated keys against known correct values.
        """

        for p_index, p in enumerate(self.passwords):
            for s_index, s in enumerate(self.salts):
                key, salt = generate_key(p, s)
                self.assertEqual(s, salt)
                self.assertEqual(key, self.keys[p_index][s_index])

    def test_salt_verification(self):
        """
        Verifies that trying to generate a key using an invalid salt actually generates a new valid salt.
        """
        password_sample = b'0000010100111001'

        # trying to generate a key without salt
        key, salt = generate_key(password_sample)

        repeat_key, repeat_salt = generate_key(password_sample, salt)
        self.assertEqual(key, repeat_key)
        self.assertEqual(salt, repeat_salt)

        # trying to use empty string as salt
        invalid_salt = ''
        key, salt = generate_key(password_sample, invalid_salt)
        self.assertNotEqual(salt, invalid_salt)

        repeat_key, repeat_salt = generate_key(password_sample, salt)
        self.assertEqual(key, repeat_key)
        self.assertEqual(salt, repeat_salt)

        # trying to use dict as salt
        invalid_salt = {'dict': 'not allowed'}
        key, salt = generate_key(password_sample, invalid_salt)
        self.assertNotEqual(salt, invalid_salt)

        repeat_key, repeat_salt = generate_key(password_sample, salt)
        self.assertEqual(key, repeat_key)
        self.assertEqual(salt, repeat_salt)

        # trying to use a salt too small
        invalid_salt = b'ogg'
        key, salt = generate_key(password_sample, invalid_salt)
        self.assertNotEqual(salt, invalid_salt)

        repeat_key, repeat_salt = generate_key(password_sample, salt)
        self.assertEqual(key, repeat_key)
        self.assertEqual(salt, repeat_salt)

        # trying to use a salt too big
        invalid_salt = b'ogg_jj_kk_ll_oo_99_aa_ii_88_kk_12_77_99_00_!!_!!'
        key, salt = generate_key(password_sample, invalid_salt)
        self.assertNotEqual(salt, invalid_salt)

        repeat_key, repeat_salt = generate_key(password_sample, salt)
        self.assertEqual(key, repeat_key)
        self.assertEqual(salt, repeat_salt)
