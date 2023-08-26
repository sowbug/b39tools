# https://github.com/sowbug/b39tools/

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

  # Copy the PDF and howto files.  
  for f in DATA_FILES.values():
    with importlib.resources.path("b39tools.docs", f) as data_file_path:
      shutil.copy2(data_file_path, os.getcwd())

  # Give an overview and confirm that user is ready.
  print("\033[2J")
  print(f"""
BIP39 Account Generator

This utility will generate a BIP39 seed and passphrase and help you preserve it
safely. To proceed, you will need the following:

1. One printed copy of {DATA_FILES['seed']}, which has been copied to this
   directory.

2. One printed copy of {DATA_FILES['shamir']}, which has been copied to this
   directory.

3. At least one pen with permanent ink.

4. A pair of scissors.
""")
  if input("Enter y if you are ready to continue, or enter n to exit...") != 'y':
    sys.exit(0)

  # Display warnings.
  print("\033[2J")
  print("""\033[5mWARNING! Please read carefully.\033[0m]

BIP39 secrets are like cash. If you lose them, your funds will be gone forever.
If someone else takes them, they can spend the funds, and you will never get
your money back.

BIP39 secrets are also unlike cash. If someone sees them, or sees a photo of
them, or hears you reading them out loud, or finds a copy of them in email or on
a computer, then they can spend the funds, and you will never get your money
back.

These instructions help avoid these problems, but not if you take shortcuts.
Examples of shortcuts:

  - Taking a screenshot or photo of the secrets instead of writing them down.

  - Copying and pasting the secrets into an email to yourself instead of writing
    them down.

  - Not making four handwritten copies.

Remember: with digital currencies, there is no undo button. There is no customer
support. There is no manager to escalate to. If you lose your secrets, you lose
your money. If anyone or anything gets access to your secrets, you lose your
money.

Following these instructions does not guarantee safety of your funds. But taking
shortcuts with these instructions guarantees that you will eventually lose your
funds.

""")
  if input("Enter y if you understand...") != 'y':
    sys.exit(0)

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
  plaintext_md = (f"\033[1mBIP-39 Seed Phrase\033[0m\n\n\033[1m{bip39_words_as_matrix}" +
                  f"\033[0m\n\n\033[1mBIP-39 Passphrase\n\n\033[1m{bip39_passphrase}\033[0m\n\n")

  master_secret = secrets.token_bytes(MASTER_SECRET_LEN)
  master_secret_text = master_secret.hex()

  shamir_mnemonic_group = shamir_mnemonic.generate_mnemonics(
      1, [(3, SHARE_COUNT)], master_secret)[0]

  shamir_shares_md = ""
  i = 1
  for m in shamir_mnemonic_group:
    m_matrix = mdformatter.MarkdownFormatter.RenderWordListAsMatrix(m)
    shamir_shares_md += f"[{i}/{SHARE_COUNT}]\n\n\033[1m{m_matrix}\033[0m\n\n"
    i += 1

  keys = [PasswordKey(master_secret_text.encode("utf-8"))]
  plaintext_bytes = bytes(plaintext, encoding="utf-8")
  outbytes = io.BytesIO()
  with Encryptor(keys, outbytes) as encryptor:
    encryptor.write(plaintext_bytes)

  # some of this code is copied from
  # https://github.com/jojonas/pyage/blob/master/src/age/utils/asciiarmor.py I
  # couldn't for the life of me get AsciiArmoredOutput to work. It behaved as if
  # it were operating asynchronously, but only once the program ended.
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

  print("\033[2J")
  print("The name of this account is", account_name.upper())
  print(f"""
This information should be generated and displayed only on an air-gapped
computer. You should copy information by hand to paper as instructed. You should
keep the generated files as instructed.

\033[5mDo not photograph this text or otherwise attempt to copy it, except as
instructed.\033[0m

Read {DATA_FILES['create']} and {DATA_FILES['recover']} for more
instructions.""")
  print()
  input("Press Enter to continue...")

  print("\033[2J")
  print(f"""
Step 1: BIP-39 secrets

These are your BIP-39 seed words and passphrase. Copy them by hand to the paper
sheet that has four sections (the file {DATA_FILES['seed']} that you printed).

\033[01m{plaintext_md}\033[0m

You will not see these words again on this screen, so now is the time to copy
them on paper.

""")
  input("Press Enter when you have finished hand-writing the words on paper...")

  print("\033[2J")
  print(f"""
Step 2: Shamir Shares

These are your five Shamir shares that encode the Age secret. Copy them by hand
to the remaining paper sheet, which should have five sections (the file
{DATA_FILES['shamir']} that you printed).
""")
  print()
  print(shamir_shares_md)
  print("""You will not see these words again on this screen, so now is the time
to copy them on paper.
""")
  input("Press Enter when you have finished hand-writing the words on paper...")

  print("\033[2J")
  print(f"""
Step 3: Encrypted Backup

The file `{armored_text_filename}` has been written to this directory. It
contains an age-encrypted copy of the BIP-39 seed words and passphrase. It's OK
to print this or store it on a computer, but you should keep it as private as
possible.

Please copy this file somewhere safe.

Step 4: Public Keys and Initial Addresses 

Two files named {account_info_filename_hot} and {account_info_filename_cold}
have been written to this directory. They contain extra information that is
useful for monitoring your balances without needing to expose your BIP-39 seed
words on a computer.

Please copy these files somewhere safe. It's also OK to destroy these files, as
they can be regenerated from the seed and passphrase.

Step 6: Guard the pieces of paper

You're almost done. Read {DATA_FILES['create']} to understand what to do with
the pieces of paper. Once you've done all that, then it's OK to use the BIP-39
seed and passphrase, for example by entering them into a hardware wallet.
""")
