# b39tools

Tools for working with [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) assets.

## Overview

`b39tools` helps with two situations.

1. You'd like to get into virtual currencies, and have a hardware wallet
   ready to set up, but you have heard frightening stories of people losing
   their 24-word seeds, getting tricked into giving their seed words to
   evildoers, losing their funds when someone finds their seed-word backup,
   or dying and leaving huge sums of Bitcoin inaccessible to their loved
   ones. You don't know what to do.

2. You'd like to be able to monitor your BIP-39 account balances, but aren't
   sure how to safely generate a list of addresses.

While `b39tools` isn't the only way to help, it's simple and it works.

## Installation

Clone or download this repository, then `pip3 install .` in the root of the
directory. As soon as I figure out how to publish this on Pypi, I will.

## Usage (Summary)

### Creating a BIP-39 account

`create-bip39-account` on an air-gapped computer, preferably running
[Tails](https://tails.boum.org/). Use `--help` to see options. This
will spit out a bunch of instructions, as well as some small files that
you should save. 

### Generating public information about a BIP-39 account

```python
$ python3
>>> import b39tools.explorer
>>> import b39tools.mdformatter
>>> e = b39tools.explorer.Bip32Explorer()
>>> e.GuessAndSetXpub("ypub6XHF56N2PSKGee9vLadyxHxCwp6geXc8qgYjsiBbsFMdkRbwVbY7fHZ4UZu63Hmpx5dfNMAkfSe8xyzQbbQJxkRnBAmrEQFoA5bR2vyhHtZ")
>>> 
>>> md = b39tools.mdformatter.MarkdownFormatter("my account", e)
>>> md.RenderAccount()
"### MY ACCOUNT\n#### m/49'/0'/0' (Segwit)\n* xpub:               `ypub6XHF56N2PSKGee9vLadyxHxCwp6geXc8qgYjsiBbsFMdkRbwVbY7fHZ4UZu63Hmpx5dfNMAkfSe8xyzQbbQJxkRnBAmrEQFoA5bR2vyhHtZ`\n- [`3HtNhiznwgWXvcBuX8STnVcvcga7ZeAK9K`](https://www.blockchain.com/btc/address/3HtNhiznwgWXvcBuX8STnVcvcga7ZeAK9K)\n- [`38oA5GJrjM2kLzJvTTxwYbRBCPaaKw3u76`](https://www.blockchain.com/btc/address/38oA5GJrjM2kLzJvTTxwYbRBCPaaKw3u76)\n- [`3CWfBBnGz9sKCrsjWQ3LzTAfAsQJ9weTpo`](https://www.blockchain.com/btc/address/3CWfBBnGz9sKCrsjWQ3LzTAfAsQJ9weTpo)\n- [`3KKWYLg3guk958ZjtqxJPxHaMCUnCyNc4Z`](https://www.blockchain.com/btc/address/3KKWYLg3guk958ZjtqxJPxHaMCUnCyNc4Z)\n- [`32LhqXVpf2uxWtqhtSucoaVjeV1h2kMCj9`](https://www.blockchain.com/btc/address/32LhqXVpf2uxWtqhtSucoaVjeV1h2kMCj9)\n\n"
```

That xpub (extended public key) is based on the [`ozone drill` BIP-39 test vector](https://github.com/trezor/python-mnemonic/blob/master/vectors.json), with the BIP-49 chain as derived from [Ian Coleman's BIP-39 tool](https://iancoleman.io/bip39/).

### Generating private information about a BIP-39 account

**Warning!** You should never type your BIP-39 seed words or passphrase into
a computer, unless you know what you're doing (for example, ensuring it's an
air-gapped machine).

```python
$ python3
>>> import b39tools.explorer
>>> import b39tools.mdformatter
>>> e = b39tools.explorer.Bip32Explorer()
>>> e.bip39_words="ozone drill grab fiber curtain grace pudding thank cruise elder eight picnic"
>>> e.bip39_passphrase="TREZOR"
>>> e.bip32_root_key.hwif()
'xpub661MyMwAqRbcFHdcyuiZBwXHanin8aTCMLdxeD6HZaK7d7ac4qc8HmBSrZT3zjHDYZYD1U8o8GDAfPGcbsJH2sNu2AXtXXqguVWY8MM4amq'
>>> e.chain60_addresses
['0xb592a90b5d4df30b4156d5ed87aea533cbf360d7', '0x2ea145aad5ccf7a5a9b8cc64b93e676d61e7113e', '0x29c8cc15c094223ef4851047f57e146b51423fe5', '0x41ef15129f874f6eae3791c508e60e8afdfb1ac8', '0x9b817ecdb56d1a628aa4a0eecbd3a4d7cb2816fa']
```

Two interesting points about this example: first, the `hwif()` shows that
the Bip32Explorer tool uses [pycoin](https://github.com/richardkiss/pycoin/)
and exposes some of its methods; and second, the tool knows about Bitcoin
legacy (`chain44addresses`), Bitcoin Segwit (`chain49addresses`), Bitcoin
Native Segwit (`chain84addresses`), and Ethereum (`chain60addresses`). Since
part of the power of BIP-32 and BIP-39 is that they're the basis of many
different kinds of virtual assets, you can use a single 24-word seed (and
optional passphrase) to derive sub-accounts for many asset types.

## Why creating a BIP-39 account safely is hard

This section discusses pitfalls of self-custody of a BIP-39 seed phrase and
passphrase (or "seed" for short), and then where the `create-bip39-account`
tool helps with a conscientious solution.

**If anyone gets your seed, they will steal your assets.** This particularly
includes the following:

* **Your good-for-nothing brother-in-law** who opens your desk drawer while
  you're out, and notices 24 words written on a scrap of paper. This is
  a simple variation of the [evil maid attack](https://en.wikipedia.org/wiki/Evil_maid_attack):
  someone is allowed access to your stuff, and they abuse that access.

* **The helpful customer service representative** who emails or calls you
  out of the blue about a Trezor or Ledger security issue, and needs your
  24 words to fix the problem. This is a [phishing attack](https://en.wikipedia.org/wiki/Phishing),
  also called a "social engineering" attack. The rep is fake. They're making
  up a story to trick you. It can also be classified as a
  [confused deputy problem](https://en.wikipedia.org/wiki/Confused_deputy_problem):
  your job is to protect your seed, and you think you're doing your job by
  telling it to that nice person on the phone.

* **Your phone, laptop, or PC.** You should assume that malware is on your
  devices. That malware is constantly scanning for seeds and uploading what
  it finds to thieves. The moment you type your seed into your PC, your
  Bitcoin disappears. *Everyone thinks their own machines are clean and that
  malware happens only to idiots.* But malware authors are way better at
  their job than you are at stopping them. Don't learn the hard way!

**If you lose your 24-word seed and passphrase, you will eventually lose access to your assets.** Examples:

* When you're setting up your Ledger or Trezor hardware wallet, you ignore
  the instructions to write down the seed. A year later, you can't find your
  hardware wallet. You cry.

* When you set up your hardware wallet, you're confused and write down just
  the PIN. A year later, you step on your hardware wallet and break it. No
  problem, you buy another one. During setup, it asks for your 24-word seed.
  At this moment, you understand for the first time in your life that the
  hardware-wallet PIN is different from the account seed. Enlightened, you
  cry.

* You write down the seed on a piece of paper and put it in your desk drawer.
  You lose your Ledger. You also remember that six months ago, you moved and
  tossed old papers, including all those scraps in your desk drawer. This
  memory causes you to cry uncontrollably. (By the way, even if you'd found
  the paper, you'd have discovered that your worthless brother-in-law (see
  above) had already found it last year and stolen your assets.)

* You write down the seed on page 273 of your college math textbook. Five
  years later, you remember you might have written it in a book. Or a
  notebook. Or was it the back of a photo of your ex-girlfriend? As you
  ponder these questions, you cry.

* You divide the 24 words into six groups of four, and carve them into six
  different parts of your house's wooden framing. Three years later, your
  house burns down while you cry on the sidewalk. (The fire actually didn't
  matter, because your home's security cameras recorded where you carved
  the words, and your troubled teen reviewed the footage and stole the funds
  18 months ago.)

* Needing your 24-word seed to recover your recently-erased Trezor, you
  confidently consult your written backup that you safely archived. The
  Trezor rejects your seed. Unbeknownst to you, eight years ago when
  you first got into Bitcoin, you cleverly omitted three words as a
  sort of [brain-wallet](https://en.bitcoin.it/wiki/Brainwallet)
  passphrase. Today, eight years later, you dimly remember something
  about needing to remember something. The tears well up; you cry.

**If you protect your seed too well, then nobody else will be able to find it when you die.**
With conventional financial assets such as bank accounts and real estate,
there is a well-established set of procedures to pass these things on to
your next of kin when you die or become incapacitated. Virtual assets are
based on cryptography, which means that if the secret is lost, the assets
are lost, too. That's good if you want to protect your assets from The Man.
It's bad if you die without passing on the secrets.

We can build all these concerns into a threat model:

* If the seed is on a computer, it will be stolen.
* If the seed is printed, artifacts of the seed will remain on the printer, or
  possibly be leaked during printing (e.g., over the network connecting the printer
  and computer).
* If the seed is on a physical medium, others might find it and steal it.
* If the seed is on a physical medium, physical disasters (fire, loss, etc.)
  will eventually destroy it.
* If recovering the seed requires human memory, the human will forget.
* The legal/probate system is incapable of moving your virtual assets when
  you die. Thus, you must have a method to pass the seed to your successors
  in interest, and non-technical people must be able to perform the method.

`create-bip39-account` does a reasonable job of addressing these threats.
Here's how it works (we assume that we're running the tool on an air-gapped
computer that leaves no traces when it shuts down):

1. It generates a 24-word phrase and passphrase (together, the "seed")
   using a
   [cryptographically strong random number generator](https://docs.python.org/3/library/secrets.html).
   If you don't trust it, you can substitute your own words and passphrase
   using `--bip39_words` and `--bip39_passphrase`.

1. It displays the seed on-screen, rather than writing it to disk, and instructs
   the user to write it down, by hand, on paper (suggested format for printed
   copy: `b39tools/docs/bip-39-seed-sheet.pdf`).

1. It generates *but does not display* a 128-bit symmetric-encryption
   passphrase. Rather, it encodes the passphrase into five 20-word shares
   using
   [a relatively standardized variant](https://github.com/satoshilabs/slips/blob/master/slip-0039.md)
   of Shamir's Secret Sharing Scheme. It instructs the user
   to write down each share on paper (suggested format: `b39tools/docs/slip-0039-shamir-share-sheet.pdf`).

1. It creates a file containing the seed, encrypted with the 128-bit
   passphrase. You'll need at least three of the Shamir shares to recover
   that passphrase, and then the `age` utility to decrypt the file with
   the passphrase.

1. It creates files containing public information describing the account,
   which is useful to monitor account balances without needing to expose the
   seed.

## Using create-bip39-account

See [howto-creation.md](b39tools/docs/howto-creation.md) for instructions, and then [howto-recovery.md](b39tools/docs/howto-recover.md) to see how to recover the seed/passphrase from the generated documents.

## Alternate solutions

* [Multisig](https://btcguide.github.io/) (also discussed
  [here](https://bitcoiner.guide/multisig/)). Potentially a lot more
  powerful than the relatively naive method described here, but because
  there are many more moving parts, it's more complicated.
* [Bitgo](https://www.bitgo.com/). An industrial-strength variant of
  multisig. Less DIY. Likely expensive.
* [Bulletproof Bitcoin](https://bulletproofbitcoin.com/). A good example of
  how to protect your BIP-39 seed from natural disasters, and a great read
  because it hammers home how important seed backup is. Not necessarily
  an alternate solution, but rather complementary as a more robust medium
  than laminated pieces of paper. Could work especially well with Shamir
  method, because your friends/family will be less likely to think a piece
  of metal is old garbage and throw it out.
