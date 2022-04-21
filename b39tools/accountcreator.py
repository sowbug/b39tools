import argparse
import base64
import importlib.resources
import io
import os
import re
import secrets
import shutil
import sys
import typing

import base58
import mnemonic
import shamir_mnemonic
from age.file import Encryptor
from age.keys.password import PasswordKey
from age.utils.asciiarmor import AGE_PEM_LABEL, AsciiArmoredOutput

import b39tools.explorer as explorer
import b39tools.mdformatter as mdformatter


def main():
  MASTER_SECRET_LEN = 16
  BIP39_STRENGTH = 256
  BIP39_PASSPHRASE_LEN = 16
  SHARE_COUNT = 5

  DATA_FILES = {
    'seed': "bip-39-seed-sheet.pdf",
    'shamir': "slip-0039-shamir-share-sheet.pdf",
    'create': "howto-creation.md",
    'recover': "howto-recovery.md",
  }

  parser = argparse.ArgumentParser(
      description="Makes it easier to get going with BIP-39.")
  parser.add_argument("--account_name", help="use provided account name")
  parser.add_argument("--bip39_words", help="use provided BIP-39 words")
  parser.add_argument("--bip39_passphrase",
                      help="use provided BIP-39 passphrase")
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
    bip39_passphrase = base58.b58encode(
        secrets.token_bytes(BIP39_PASSPHRASE_LEN)).decode("utf-8")

  bip39_words_as_matrix = mdformatter.MarkdownFormatter.RenderWordListAsMatrix(bip39_words)
  plaintext = f"{'BIP-39 Seed Phrase:':<12} {bip39_words}\n{'BIP-39 Passphrase:':<12} {bip39_passphrase}\n"
  plaintext_md = f"### BIP-39 Seed Phrase\n```\n{bip39_words_as_matrix}```\n### BIP-39 Passphrase\n```\n{bip39_passphrase}\n```\n"

  master_secret = secrets.token_bytes(MASTER_SECRET_LEN)
  master_secret_text = master_secret.hex()

  shamir_mnemonic_group = shamir_mnemonic.generate_mnemonics(
      1, [(3, SHARE_COUNT)], master_secret)[0]

  shamir_shares_md = ""
  i = 1
  for m in shamir_mnemonic_group:
    m_matrix = mdformatter.MarkdownFormatter.RenderWordListAsMatrix(m)
    shamir_shares_md += f"[{i}/{SHARE_COUNT}]\n```\n{m_matrix}```\n\n"
    i += 1

  keys = [PasswordKey(master_secret_text.encode("utf-8"))]
  plaintext_bytes = bytes(plaintext, encoding="utf-8")
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
    chunk = encoded[i: i + 64]
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

  def write_account_info_to_file(info, filename):
    with open(filename, "w") as f:
      f.write(info)

  e = explorer.Bip32Explorer()

  e.bip39_words = bip39_words
  md = mdformatter.MarkdownFormatter(account_name + " Hot", e)
  hot_account = md.RenderAccount()
  account_info_filename_hot = basename + "-hot.txt"
  write_account_info_to_file(hot_account, account_info_filename_hot)

  e.bip39_passphrase = bip39_passphrase
  md = mdformatter.MarkdownFormatter(account_name + " Cold", e)
  cold_account = md.RenderAccount()
  account_info_filename_cold = basename + "-cold.txt"
  write_account_info_to_file(cold_account, account_info_filename_cold)

  for f in DATA_FILES.values():
    with importlib.resources.path("b39tools.docs", f) as data_file_path:
      shutil.copy2(data_file_path, os.getcwd())

  print("#", account_name.upper())
  print("* This information should be generated and displayed only on an air-gapped computer.")
  print("* You should copy information by hand to paper as instructed.")
  print("* You should keep the generated files as instructed.")
  print("* Do not photograph this text or otherwise attempt to copy it, except as instructed.")
  print(f"* Read `{DATA_FILES['create']}` and `{DATA_FILES['recover']}` for more instructions.")
  print()

  print("## BIP-39")
  print("* These are your BIP-39 seed words and passphrase.")
  print(f"* Copy them by hand to at least one paper backup. Use `{DATA_FILES['seed']}` as a template.")
  print()
  print(plaintext_md)

  print("## Shamir")
  print("* These are your five Shamir shares that encode the Age secret.")
  print(f"* Copy them by hand to five pieces of paper. Use `{DATA_FILES['shamir']}` as a template.")
  print()
  print(shamir_shares_md)

  print("## Encrypted Backup")
  print(f"The file `{armored_text_filename}` has been written to this directory.")
  print("It contains an age-encrypted copy of the BIP-39 seed words and passphrase.")
  print("It's OK to print this or store it on a computer, but you should keep it as private as possible.")
  print()

  print("## Account Extended Public Keys and addresses")
  print(f"Two files named `{account_info_filename_hot}` and `{account_info_filename_cold}` have been written to this directory.")
  print("They contain extra information that is useful for monitoring your balances without needing to expose your BIP-39 seed words on a computer.")
  print()
