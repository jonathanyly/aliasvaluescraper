# Alias Sneaker Price Checker for VAT registered companies

This python repository is used to check for sneaker prices.
It takes in a given webhook and your countries VAT amount (e.g. Germany -> 19% VAT -> 1.19 as input)
It deducts VAT from the bought shoe.

The checker includes:
- Sales Volume for each size -> Calcualtes the days it took to sell 10 pairs.
- Profit after all fees
- Price in euro, taken from current exchange rate USD/EUR

You can check a sneaker by sending a webhook in your channel with:
!a {SKU} {price}
where SKU is the sneakers SKU and price is the sneakers price you paid for it.

Example webhook with following input:

!a 408452-017 150

<img width="526" alt="Bildschirm­foto 2023-06-12 um 16 46 44" src="https://github.com/jonathanyly/aliaschecker/assets/114871601/89a76698-e400-4e68-a98a-63640a591706">

