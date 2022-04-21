# b39tools recovery HOWTO

You are reading this because you want to use a Seed Copy or Shamir Shares to set up a new hardware wallet.

## What you need

- Either (1) a Seed Copy, or (2) at least three Shamir Shares.
- If you're using the Shamir Shares, then you'll also need the `xxxxx-xxxxx.age` file on a USB drive.
- An air-gapped computer. Anything running [Tails](https://tails.boum.org/) is good.
- A hardware wallet (Ledger, Trezor, etc.) that is ready to be set up.

## Instructions (Seed Copy)

This is self-explanatory. Use the seed and passphrase to set up the wallet. You're done.

## Instructions (Shamir Shares)

1. Boot into Tails on a PC you trust.

1. Install `python-shamir-mnemonic` and `age`.

1. Using `shamir recover`, enter the share words as prompted. Note the passphrase it produces. It will be a long string of hexadecimal digits, like `000102030405060708090a0b0c0d0e0f`.

1. Using `age -d xxxxx-xxxxx.age` and the passphrase you recovered from the Shamir Shares, decrypt the `.age` file and note the BIP-39 seed and passphrase.

1. Set up your new hardware wallet using the recovered seed/passphrase.
