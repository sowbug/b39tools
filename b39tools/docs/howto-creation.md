# BIP-39 Account Creation HOWTO

## What you need

- One printed copy of `b39tools/docs/bip-39-seed-sheet.pdf`,
- One printed copy of `b39tools/docs/slip-0039-shamir-share-sheet.pdf`,
- An air-gapped computer. Anything running [Tails](https://tails.boum.org/) is
  good.
- A USB drive.
- At least one pen.

## Instructions

1. Install this project using `pip3 install b39tools` on the air-gapped
   computer.

1. Insert the USB drive into the computer.

1. Open a terminal and `cd` to the USB drive.

1. In the terminal, run `create-bip39-account`.

1. Follow the tool's instructions. It's recommended to make four copies of the
   BIP-39 seed and passphrase (that's why the seed sheet is divided into four
   parts), and to use a different pen for each copy in case one pen's ink fades
   over the years.

1. At this point, you should have the following:

    - One sheet of paper with four handwritten copies of the BIP-39 seed and
      passphrase (the Seed Copies).
    - One sheet of paper with five unique handwritten Shamir shares (the Shamir
      Shares).
    - Several new files on the USB drive.

1. Restart the air-gapped computer. At this point, the only physical artifacts
   of your new BIP-39 account are the two pieces of paper and the files on the
   USB drive.

1. Make copies of the files on the USB drive. It's OK for them to be online
   (Google Drive, iCloud, etc.), but you shouldn't share them with anyone
   (except perhaps your attorney or spouse).

1. Cut the Seed Copies into four separate pieces of paper.

1. Cut the Shamir Shares into five separate pieces of paper.

1. Try the steps in `howto-recovery.md` to verify that the Shamir Shares can
   reconstitute the BIP-39 seed and passphrase. Compare the results to each of
   the four Seed Copies to verify that you didn't write any seed words
   incorrectly.

1. Protect each of the Shamir Shares, for example by laminating them. You should
   fold each piece of paper so that the security pattern is on the outside. This
   means that you won't be able to see the share words without cutting the
   lamination, which is good because casual snoopers won't be able to snap a
   quick picture with their phone if they happen upon a share.

1. Protect **three** of the four Seed Copies in the same manner (folding and
   laminating).

1. Give the Shamir Shares to five different people or institutions. For example,
   you might give one to an attorney. You might put another in a safe-deposit
   box. If you work somewhere that has a safe, you might put a third share in
   there. You should also give instructions for what to do with the shares. For
   example: "Please keep this document safe and secure, as you would your own
   birth certificate or passport. Don't let anyone see it. If I die, please give
   it to the executor of my estate. If I'm legally incapacitated, please give it
   to my legal guardian."

1. Put three of the Seed Copies in locations that are (1) geographically
   distributed, (2) safe from discovery, and (3) in places you'll remember.

1. If you have a will, add instructions to recover the Shamir Shares and
   transfer the assets to your loved ones. Include a printout of the `.age` file
   that you got from the USB drive. Your executor probably won't know where the
   shares are, so you should list who has them.

1. At this point, the following is true:

    - You have several semi-protected copies of the BIP-39 seed/passphrase. Be
      aware that these copies are a security risk because anyone who finds them
      will be able to take your assets.

    - You have a plan for passing your assets to your loved ones. The security
      risk with the Shamir Shares is that three of the holders will conspire to
      recover the seed/passphrase against your wishes. You can mitigate this
      risk by keeping the `.age` file from the five share holders. (But make
      sure that your loved ones can find that file when they need it!).

    - You have confidence that no other copies of your BIP-39 seed/passphrase
      exist in the world.

1. Now that your seed/passphrase is well-protected, it's time to use it! Using
   the fourth non-laminated Seed Copy, set up a hardware wallet (Trezor, Ledger,
   etc.) and fund your account.

1. It's up to you what to do with the fourth Seed Copy. You can laminate it like
   the other ones (which means you'll have to cut it open next time you need to
   set up your hardware wallet again), or destroy it. I recommend setting up
   several identical hardware wallets, then laminating the Seed Copy the same
   way you did with the other three.
