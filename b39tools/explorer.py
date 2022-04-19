import sha3
from mnemonic import Mnemonic
from pycoin.encoding.hexbytes import b2h, h2b
from pycoin.key.BIP32Node import BIP32Node
from pycoin.key.BIP49Node import BIP49Node
from pycoin.symbols.btc import network as BTC


class Bip32Explorer:
  def __init__(self, addresses_to_generate=5):
    self.__bip39_words = None
    self.__bip39_passphrase = None
    self.__bip39_seed = None
    self.__bip32_root_key = None
    self.__xpub44 = None
    self.__ypub49 = None
    self.__zpub84 = None
    self.__xpub60 = None
    self.__addresses_to_generate = addresses_to_generate

    self.__chain44addresses = []
    self.__chain49addresses = []
    self.__chain60addresses = []
    self.__chain84addresses = []

    self.__mnemonic = None

  def __initMnemonic(self):
    if self.__mnemonic is None:
      self.__mnemonic = Mnemonic("english")

  def GetBip32RootKey(self):
    return self.__bip32_root_key

  def SetBip32RootKey(self, key):
    if key != self.__bip32_root_key:
      self.__bip32_root_key = key
      self.SetXpub44(key.subkey_for_path("44p/0p/0p.pub"))
      self.SetXpub60(key.subkey_for_path("44p/60p/0p.pub"))
      self.SetYpub49(BTC.keys.bip49_deserialize(b"\0\0\0\0" +
                                                self.__bip32_root_key.subkey_for_path("49p/0p/0p.pub").serialize()))
      self.SetZpub84(BTC.keys.bip84_deserialize(b"\0\0\0\0" +
                                                self.__bip32_root_key.subkey_for_path("84p/0p/0p.pub").serialize()))

  def GetBip39Seed(self):
    return self.__bip39_seed

  def SetBip39Seed(self, seed):
    if seed != self.__bip39_seed:
      self.__bip39_seed = seed
      self.SetBip32RootKey(BTC.keys.bip32_seed(seed))

  def GetBip39Words(self):
    return self.__bip39_words

  def SetBip39Words(self, words):
    self.__initMnemonic()
    normalized_words = self.__mnemonic.normalize_string(words)
    if normalized_words != self.__bip39_words:
      self.__bip39_words = normalized_words
      self.SetBip39Seed(self.__mnemonic.to_seed(self.__bip39_words))

  def GetBip39Passphrase(self):
    return self.__bip39_passphrase

  def SetBip39Passphrase(self, passphrase):
    self.__initMnemonic()
    if passphrase != self.__bip39_passphrase:
      self.__bip39_passphrase = passphrase
      self.SetBip39Seed(self.__mnemonic.to_seed(
          self.__bip39_words, self.__bip39_passphrase))

  def GetChain44Addresses(self):
    return self.__chain44addresses

  def GetChain49Addresses(self):
    return self.__chain49addresses

  def GetChain60Addresses(self):
    return self.__chain60addresses

  def GetChain84Addresses(self):
    return self.__chain84addresses

  def GetXpub44(self):
    return self.__xpub44

  def SetXpub44(self, key):
    self.SetXpub44WithPath(key, "0/%d")

  def SetXpub44WithPath(self, key, path):
    if isinstance(key, str):
      key = BTC.parse(key)
    self.__xpub44 = key
    self.__chain44addresses = self.GenerateChainInfo(path, self.xpub44)

  def GetYpub49(self):
    return self.__ypub49

  def SetYpub49(self, key):
    self.SetYpub49WithPath(key, "0/%d")

  def SetYpub49WithPath(self, key, path):
    if isinstance(key, str):
      key = BTC.parse(key)
    self.__ypub49 = key
    self.__chain49addresses = self.GenerateChainInfo(path, self.ypub49)

  def GetXpub60(self):
    return self.__xpub60

  def SetXpub60(self, key):
    self.SetXpub60WithPath(key, "0/%d")

  def SetXpub60WithPath(self, key, path):
    if isinstance(key, str):
      key = BTC.parse(key)
    self.__xpub60 = key
    self.__chain60addresses = self.GenerateChainInfo(path, self.xpub60, True)

  def GetZpub84(self):
    return self.__zpub84

  def SetZpub84(self, key):
    self.SetZpub84WithPath(key, "0/%d")

  def SetZpub84WithPath(self, key, path):
    if isinstance(key, str):
      key = BTC.parse(key)
    self.__zpub84 = key
    self.__chain84addresses = self.GenerateChainInfo(path, self.zpub84)

  def GenerateChainInfo(self, path, pub, is_eth=False):
    key = BTC.parse(pub.hwif())
    addrs = []
    for n in range(0, self.__addresses_to_generate):
      subkey = key.subkey_for_path(path % n)
      if is_eth:
        x, y = subkey.public_pair()
        digest = sha3.keccak_256(x.to_bytes(
            32, 'big') + y.to_bytes(32, 'big')).digest()
        addrs.append('0x' + b2h(digest[-20:]))
      else:
        addrs.append(subkey.address())
    return addrs

  bip39_seed = property(GetBip39Seed, SetBip39Seed)
  bip39_words = property(GetBip39Words, SetBip39Words)
  bip39_passphrase = property(GetBip39Passphrase, SetBip39Passphrase)
  bip32_root_key = property(GetBip32RootKey, SetBip32RootKey)
  chain44_addresses = property(GetChain44Addresses)
  chain49_addresses = property(GetChain49Addresses)
  chain60_addresses = property(GetChain60Addresses)
  chain84_addresses = property(GetChain84Addresses)
  xpub44 = property(GetXpub44, SetXpub44)
  ypub49 = property(GetYpub49, SetYpub49)
  xpub60 = property(GetXpub60, SetXpub60)
  zpub84 = property(GetZpub84, SetZpub84)
