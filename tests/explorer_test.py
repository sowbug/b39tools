import unittest
import b39tools
from b39tools import explorer

BIP39_TEST_WORDS = "equip dress paper spoil cradle slam easily come monkey old master tiny before pave chapter page museum good consider busy avocado balance burden finger"
BIP39_TEST_PASSPHRASE = "passphrase#@)"
class TestBip32Explorer(unittest.TestCase):
  def testEquipDress(self):
    e = b39tools.explorer.Bip32Explorer()
    e.bip39_words = BIP39_TEST_WORDS

    # https://github.com/libbitcoin/libbitcoin-explorer
    #
    # bx mnemonic-to-seed $BIP39_TEST_WORDS
    self.assertEqual(
      e.bip39_seed,
      bytes.fromhex('d4881cf5659ad9fca9df72d6a32e82704a3b93ae46dde040682c05eece0744b1f1ed6b7c5e132983aa25327deea77ecc9f0395a191578d45ba362de5392c3a93'))

    # bx mnemonic-to-seed $BIP39_TEST_WORDS | bx hd-new
    self.assertEqual(
      'xprv9s21ZrQH143K2wQR8oXCUSaUXqta8WGsNHzJ6p1Bk2KH7gf6JRt7TzBSFxKQ4KtXssGiouKv82bDGbzsBQc2kHtMfXTScKJ47vSznLf6Zit',
      e.bip32_root_key.hwif(as_private=True))

    # $ bx mnemonic-to-seed $BIP39_TEST_WORDS | bx hd-new | \
    #   bx hd-private -d -i 44 | \
    #   bx hd-private -d -i 0 | \
    #   bx hd-public -d -i 0
    #
    # $ bx mnemonic-to-seed $BIP39_TEST_WORDS | bx hd-new | \
    #   bx hd-private -d -i 44 | \
    #   bx hd-private -d -i 0 | \
    #   bx hd-private -d -i 0 | \
    #   bx hd-private -i 0 | \
    #   bx hd-public -i 0 | \
    #   bx hd-to-ec | \
    #   bx ec-to-address
    self.assertEqual(
      'xpub6DUE4n3S4vQAT7n4TkGCEPTnGvU6fY9WCtmZjLuoeUsYpHBhwnkzCCvZpSkXCCLjCkKTtbjhJKyfkZFVHLSocsSmu22f9bbR1RSBksugsHu',
      e.xpub44.hwif())
    self.assertIn('15hpeQHdjgeTcxSnYZEDJXYeoUBXZC3M6P', e.chain44_addresses)

    self.assertEqual(
      'ypub6WrhoMx2uCteoYDUxgxFKLEEeibiwGtM2mBV7SuyVdx2poyktfjz2V7vna6mnyUfdd3dSi1VzFyU6bktxLAGJvKyqXQ1Skeh5cAD9agDbed',
      e.ypub49.hwif())
    self.assertIn('3PvhKs7iwNnCa4RzQMoUsyWEK2ULJzpXTB', e.chain49_addresses)

    self.assertEqual(
      'zpub6qjeyBYoFSwqBF6mQ7BTqnJxzaSZEFP712C7AQag2J4bDzkyzgjJ9UqNNtPyKLW9oqYDoTZVy4QiZ87pYLuStbw5jvnr6nGNxs8aTXQKaMW',
      e.zpub84.hwif())
    self.assertIn('bc1qxnxcckec39re4ght2mywn0mc7jsvaz66zf38gk', e.chain84_addresses)

    self.assertEqual(
      'xpub6DX7QjELNybnmeztsnSfqkQNdZeUn8tzJx8j4CSkj2FMGtn6mRhpJn5t4EZJukUkR4HbmCkobRqDJKAUDc4tDmKdcf7w4UG821kLcmCVgSy',
      e.xpub60.hwif())
    self.assertIn('0x738ef667e9c4dc13e2f3f6ed8047305cbcddcc73', e.chain60_addresses)

  def testEquipDressPassphrase(self):
    e = explorer.Bip32Explorer()
    e.bip39_words = BIP39_TEST_WORDS
    e.bip39_passphrase = BIP39_TEST_PASSPHRASE

    # bx mnemonic-to-seed -p $BIP39_PASSPHRASE $BIP39_TEST_WORDS
    self.assertEqual(
      e.bip39_seed,
      bytes.fromhex('10e339f5c569256d8e7bfae1354d881b6ada6eb89d7eeeb905feeec31c3a330d0f0358b5fbc0f6531ca5e9be2923c61b8466edcc2426f0fe0f3fda8b7e320e98'))

    self.assertEqual(
      'xprv9s21ZrQH143K2zwzLSJWf7BKmh8oFTgXw6W4sudc9pWRHPSgvigSMw2KEa7Bxuhe6x5mstM9SM2LXzVexsmWxf8nNu5Riyf1TR8DMkVnGvK',
      e.bip32_root_key.hwif(as_private=True))

    self.assertEqual(
      'xpub6CShsQnEsNdVDgk73s7CoR6FHNZzEYoLRMYS8WMZmzxqkRk4hdRzZcnTcDzeDHikJRA8MGMVcTXQEurbCWVwmQfQ1fmeFknRZFsoN8S1NB9',
      e.xpub44.hwif())
    self.assertIn('18Qd79mDUc9khLuzNESJwHwKZ7mpPKEWbP', e.chain44_addresses)

    self.assertEqual(
      'ypub6WWYTTtf7nuHakWiGtnio4FJXtg8Q6JzHy3oS51uYSMRkdF1azR2cFjZg8DkNrQWvAkispfZP6nbTC1MaqUjnwiq1F6YFYu6LPZ9n7FxYH5',
      e.ypub49.hwif())
    self.assertIn('3GFbBnEWVzAFZZ9tZqn1Qd7pvTWAn41gTq', e.chain49_addresses)

    self.assertEqual(
      'zpub6qNkJ7u9Q5VA3K37hzqZi4gL3RTsAjXZN4G8HonZUoFKvum93rNUn43sXCFXJ4ztMiBMJAKFNkDmFqsmKux75ZhCbUkbZTJjLy8KjZ7T3hs',
      e.zpub84.hwif())
    self.assertIn('bc1qsdt8z4lurpcth7lh7wa4gvyqswksv8qc3pca93', e.chain84_addresses)

    self.assertEqual(
      'xpub6CvENowM7TV3Ax4xatjtTHzqFqn7VUaAPneg295jJMMnd9eE7z5UC9UnRaJPmpk3phm4s8DvH7FGv5K9sgWkZAXUbBuXQP1HMSiiLYiGSUN',
      e.xpub60.hwif())
    self.assertIn('0xa45007b6e510000286ec1e29bce2e7f5b76b8c11', e.chain60_addresses)

  def testEquipDressDerivations(self):
    e = explorer.Bip32Explorer()
    e.xpub44 = 'xpub6DUE4n3S4vQAT7n4TkGCEPTnGvU6fY9WCtmZjLuoeUsYpHBhwnkzCCvZpSkXCCLjCkKTtbjhJKyfkZFVHLSocsSmu22f9bbR1RSBksugsHu'
    self.assertIn('15hpeQHdjgeTcxSnYZEDJXYeoUBXZC3M6P', e.chain44_addresses)

  def testFromSeed(self):
    # refuse fee shoulder bullet rain father renew ordinary top hint exile connect april fiscal enroll
    e = explorer.Bip32Explorer()
    e.bip39_seed = bytes.fromhex('e4eb4898bf9f09d78b2f1466a5256429d3cc4f04c65bfbfd1a75151e4c5282eba04f7e0a691332b6396c31b0e3cdd0fd74d8864ad2a02e4e1a53f71918778c31')
    self.assertEqual(
      'xprv9s21ZrQH143K2rkKxaybxoWogG4VEJjaZnJG8CncxgvpxCdyZ1so11BEeRBudMm2BFTGA1YjtsCRx3p2xS5ecNw7Q6EKKUpQSQe2gsom4zx',
      e.bip32_root_key.hwif(as_private=True))
    self.assertEqual(
      'xpub6Cya6UvBb8Lb2CUGFN7C9qV84K3g5zq5tmYjkyNYX9MR4zcqhC5nUM6rWcWsJp76ZUY5casW88aS4eJmqayz1RT8y1JUvtFKCh1QQzPDLCi',
      e.xpub44.hwif())
    self.assertEqual(
      'ypub6XUScZE62iYqhfYHzV52vvtKcfuf9XbHkHQiPhCNyPMZ4mFKXFKm4niycH7yhL9Wi97EsCtwXFoNziaN2psxNF7UWZsD6r1fKPJd5c9YVAa',
      e.ypub49.hwif())
    self.assertEqual(
      'zpub6qZoCekWJFJJnwYdMcE1cq7qaXibQZhPrMDZMW5LjbmdfCo1NZakHm7msr5CnCkRFTmKMrBDAypng81V8tQHa8pFmHh8jmFfU7Bjk2j5aeL',
      e.zpub84.hwif())
    self.assertEqual(
      'xpub6Bf9fX9te1TEnDmng51EziVCvRBjSrp9CZwNwvEfoNAMXqwUNMGG71znuQWt3Hv6CMQzd2c3noZMYWqGDgL8YAiYymHtnSJRSGiC6fk8q7w',
      e.xpub60.hwif()
    )
  
  def testFromAccountExtendedPublicKeys(self):
    # say suspect obvious opera fiber cushion tail deposit satisfy candy category knee reopen actress stick repeat comic brush property measure cargo

    # These xpubs are taken from https://iancoleman.io/bip39/ in the "Account Extended Public Key" field

    e = explorer.Bip32Explorer()
    e.xpub44 = 'xpub6CSscwauvLjWgWh7nTw5uv6Y1BojKYMP8CMbaoWviTmTT5gHf6u4fejvfqDFGUvwbUR7LzRL4mnzv5SXda5HjNxSnqML9Lw82LBd8hJ5jho'
    self.assertIn('19YNp5BYu9Su2ZcmvPVrHW4HRKaFKoDug', e.chain44_addresses)

    e = explorer.Bip32Explorer()
    e.ypub49 = 'ypub6XQmAQxts1gGuzhiavveTb3ti67FCG3rJc3q13JyHnAPZByJcED9CzNLdT7a5LAjZESaK6vFvNoZrPXADSsJqGZ8SwZFsbwEwD5VC6XTEeT'
    self.assertIn('3DHwLjy9aXFH9DwDwPEzLaPiuCwAZHUecV', e.chain49_addresses)

    e = explorer.Bip32Explorer()
    e.zpub84 = 'zpub6qpFikmA4HccKTU2WiDbs1huJ7rfEZiKN5uWDZwZ1sN2LWLj7N92F2UwB6AZVyPNcjGqcB2cW4wauXpqj7MBTBvGUDa6cBqZCkS1PPdciEM'
    self.assertIn('bc1qx0kq4arsunrkn9pdcdhtpjcw0z2x2lvyns2fng', e.chain84_addresses)

    e = explorer.Bip32Explorer()
    e.xpub60 = 'xpub6Bgi76jXZaxFuqVaruBfhHds12xpQBWrPtEYyBNU5NBnopvf1bp6P6eJGYJ7Qiuy77kwHELG9ByJYv7wbKXQoF8t9zgUt6yGxSduTtYAY6i'
    self.assertIn('0xa99f4299c5b75009d6bab914e0c6f29f9ad70224', e.chain60_addresses)

if __name__ == '__main__':
    unittest.main()
