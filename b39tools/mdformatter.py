import sys

import b39tools.explorer as explorer

class MarkdownFormatter():
  def __init__(self, account_name, account_explorer):
    self.__account_name = account_name
    self.__account_explorer = account_explorer

  def render_account_header(self):
    return f"# {self.__account_name.upper()}\n" 

  def render_chain(self, path_label, xpub, addresses):
    md = ''

    md += f"### {path_label}\n"
    md += self.render_xpub(xpub)

    for a in addresses:
        if a.startswith("0x"):
            link = "https://etherscan.io/address/%s" % a
        else:
            link = "https://www.blockchain.com/btc/address/%s" % a
        md += f"- [`{a}`]({link})\n"

    return md

  def render_words(self, text):
    return f"* {'BIP-39 words:':<16}`{text}`\n"

  def render_passphrase(self, text):
    return f"* {'BIP-39 passphrase:':<16}`{text}`\n"

  def render_seed(self, text):
    text = text.hex()
    return f"* {'BIP-39 seed:':<16}`{text}`\n"

  def render_xpub(self, text):
    return f"* {'xpub:':<16}`{text}`\n"

  def render_xprv(self, text):
    return f"* {'xprv:':<16}`{text}`\n"

  def RenderAccount(self, include_private=False):
    md = ''
    e = self.__account_explorer

    md += self.render_account_header()
    if include_private:
      if e.bip39_words:
        md += self.render_words(e.bip39_words)
      if e.bip39_passphrase:
        md += self.render_passphrase(e.bip39_passphrase)
      if e.bip39_seed:
        md += self.render_seed(e.bip39_seed)
      if e.bip32_root_key:
        md += self.render_xprv(e.bip32_root_key.hwif(as_private=True))

    if e.xpub44:
      md += self.render_chain("m/44'/0'/0'", e.xpub44.hwif(), e.chain44_addresses)
    if e.ypub49:
      md += self.render_chain("m/49'/0'/0'", e.ypub49.hwif(), e.chain49_addresses)
    if e.zpub84:
      md += self.render_chain("m/84'/0'/0'", e.zpub84.hwif(), e.chain84_addresses)
    if e.xpub60:
      md += self.render_chain("m/44'/60'/0'", e.xpub60.hwif(), e.chain60_addresses)

    return md
