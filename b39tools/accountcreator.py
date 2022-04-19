#!/bin/env python3

import argparse
import base64
import io
import re
import secrets
import sys
import typing

import base58
import mnemonic
import shamir_mnemonic
from age.file import Encryptor
from age.keys.password import PasswordKey
from age.utils.asciiarmor import AGE_PEM_LABEL, AsciiArmoredOutput

import b39tools.explorer as explorer

def main():
  MASTER_SECRET_LEN = 16
  BIP39_STRENGTH = 256
  BIP39_PASSPHRASE_LEN = 16
  SHARE_COUNT = 5

  parser = argparse.ArgumentParser(description='Makes it easier to get going with BIP-39.')
  parser.add_argument("--account_name", help="use provided account name")
  parser.add_argument("--bip39_words", help="use provided BIP-39 words")
  parser.add_argument("--bip39_passphrase", help="use provided BIP-39 passphrase")
  args = parser.parse_args()

  m = mnemonic.Mnemonic(language="english")
  if args.bip39_words:
    bip39_words = args.bip39_words
  else:
    bip39_entropy = secrets.token_bytes(BIP39_STRENGTH >> 3)
    bip39_words = m.to_mnemonic(bip39_entropy)

  if args.bip39_passphrase:
    bip39_passphrase = args.bip39_passphrase
  else:
    bip39_passphrase = base58.b58encode(secrets.token_bytes(BIP39_PASSPHRASE_LEN)).decode("utf-8")

  plaintext    = f"{'BIP 39:':<12} {bip39_words}\n{'Passphrase:':<12} {bip39_passphrase}\n"
  plaintext_md = f"BIP 39: `{bip39_words}`\n\nPassphrase: `{bip39_passphrase}`\n"

  master_secret = secrets.token_bytes(MASTER_SECRET_LEN)
  master_secret_text = master_secret.hex()

  shamir_mnemonic_group = shamir_mnemonic.generate_mnemonics(1, [(3, SHARE_COUNT)], master_secret)[0]

  shamir_shares = ''
  i = 1
  for m in shamir_mnemonic_group:
    shamir_shares += f"[{i}/{SHARE_COUNT}] `{m}`\n\n"
    i += 1

  keys = [PasswordKey(master_secret_text.encode("utf-8"))]
  plaintext_bytes = bytes(plaintext, encoding='utf-8')
  outbytes = io.BytesIO()
  with Encryptor(keys, outbytes) as encryptor:
    encryptor.write(plaintext_bytes)

  # some of this code is copied from https://github.com/jojonas/pyage/blob/master/src/age/utils/asciiarmor.py
  # I couldn't for the life of me get AsciiArmoredOutput to work. It behaved as if it were operating asynchronously,
  # but only once the program ended.
  armored_text = io.StringIO()
  label = AGE_PEM_LABEL
  armored_text.write(f"-----BEGIN {label}-----\n")
  encoded = base64.b64encode(outbytes.getvalue()).decode("ascii")
  for i in range(0, len(encoded), 64):
    chunk = encoded[i : i + 64]
    armored_text.write(chunk)
    armored_text.write("\n")
  armored_text.write(f"-----END {label}-----\n")
  armored_text.seek(0)
  armored_text = armored_text.read()

  shamir_mnemonic_parts = shamir_mnemonic_group[0].split()
  if args.account_name:
    account_name = args.account_name.strip().lower()
    if not re.search(r"[\w+ ]+", account_name):
      print("error: account name must consist only of letters, numbers, and spaces")
      sys.exit(-1)
  else:
    account_name = shamir_mnemonic_parts[0] + " " + shamir_mnemonic_parts[1]
  basename = account_name.replace(" ", "-")
  armored_text_filename = basename + ".age"
  with open(armored_text_filename, "w") as f:
    f.write(armored_text)

  def render_account(u):
    xpub = u.zpub84.hwif()
    addr = u.chain84_addresses[0]
    return f"* {'xpub:':<16} `{xpub}`\n* {'First address:':<16} `{addr}`\n"

  def write_account_file(u, filename):
    xpub = u.zpub84.hwif()
    addr = u.chain84_addresses[0]
    with open(filename, "w") as f:
      f.write(f"{'xpub:':<16} {xpub}\n{'First address:':<16} {addr}\n")

  u = explorer.Bip32Explorer()
  u.bip39_words = bip39_words
  hot_account = render_account(u)
  account_info_filename_hot = basename + "-hot.txt"
  account_info_filename_cold = basename + "-cold.txt"
  write_account_file(u, account_info_filename_hot)
  u.bip39_passphrase = bip39_passphrase
  cold_account = render_account(u)
  write_account_file(u, account_info_filename_cold)

  print("#", account_name.upper())
  print("* This information should be generated and displayed only on an air-gapped computer.")
  print("* You should copy information by hand to paper as instructed.")
  print("* You should keep the generated files as instructed.")
  print("* Do not photograph this text or otherwise attempt to copy it, except as instructed.")
  print()

  print("## BIP-39")
  print("* These are your BIP-39 seed words and passphrase.")
  print("* Anyone who has these words has full access to your assets.")
  print("* Copy them by hand to at least one paper backup.")
  print("* Protect the paper backups as carefully as you'd protect a million-dollar bill.")
  print("* Never type these words into a computer.")
  print("* Never tell these words to anyone.")
  print()
  print(plaintext_md)

  print("## Shamir")
  print("* These are your five Shamir shares that encode the Age secret.")
  print("* You need the python-shamir-mnemonic utility (`pip3 install shamir-mnemonic`) and at least three of the shares to recover the Age secret (`shamir recover`).")
  print("* Copy them by hand to five pieces of paper.")
  print("* Distribute the paper copies to people you trust. If three of them join their shares, they will have full access to your assets.")
  print()
  print(shamir_shares)

  print("## Encrypted Backup")
  print(f"* This is an age-encrypted copy of the BIP-39 seed words and passphrase. It is stored in this directory as `{armored_text_filename}`.")
  print( "* It's OK to print this or store it on a computer, but keep it as private as possible.")
  print(f"* You need the age encryption utility (`apt install age`) and the Age secret to decrypt it (`age -d {armored_text_filename}`).")
  print()
  print(f"```\n{armored_text}```")

  print("## Bitcoin xpub and addresses")
  print("* This information is useful for monitoring your balances without needing your BIP-39 seed words.")
  print(f"* Two files containing this information have been written to this directory. They are called `{account_info_filename_hot}` and  `{account_info_filename_cold}`.")
  print()
  print("### Hot account (no BIP-39 passphrase)")
  print(hot_account)
  print("### Cold account (BIP-39 passphrase)")
  print(cold_account)
