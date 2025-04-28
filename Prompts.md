# Samples prompts


## Second LL prompts

parse the text between "------" and "------". In it there is a list of tariffs code that are good matches for "Teddy Bears". Prints them as a JSON array, containing only the codes. Output only the json nothing else.

------
Based on the product name "Teddy bears", I would identify the following best matches from the provided list:

* 39269016 Pacifiers (Note: Pacifiers are typically small, stuffed animals that resemble human-like faces. While they share some 
similarities with teddy bears, there might be a slight difference in design or purpose.)
* 95030000 Toys, including riding toys o/than bicycles, puzzles, reduced scale models (This code is broad and includes various types 
of toys, but it's the closest match to "Teddy bears" among all the options)

The other codes listed appear to be unrelated to teddy bears. For example:

* 33061000 Dentifrices are oral care products.
* 20079970 Currant and berry fruit jellies are a type of food product.
* 08042060 Figs, fresh or dried, whole, in immediate containers weighing with their contents 0.5 kg or less is also a type of food 
product.
* 87050000 Baby carriages (including strollers) and parts thereof might be related to another type of baby-related product.

Keep in mind that the best match can be subjective and may depend on specific characteristics, designs, or purposes of the "Teddy 
bears" product.
------

```json
[
  "39269016",
  "95030000"
]
```



parse the text between "------" and "------". In it there is a list of tariffs code that are good matches for "Wooden beds". Prints them as a JSON array, containing only the codes. Output only the json nothing else.

------
To determine the best match for a product named "Wooden beds", I'll analyze each possible tariff code:

1. **94035090 Furniture (o/than seats) of wood (o/than bentwood), of a kind used in the bedroom & not designed for motor vehicle use**: This code is close, but it mentions furniture that's not specifically designed as beds.
2. **94014100 Seats nesoi, convertible into beds (o/than garden seats or camping equip.), of wood**: This code seems more relevant, as it explicitly mentions "convertible into beds" and includes wood as the material.
3. **94014900 Seats nesoi, convertible into beds (o/than garden seats or camping equip.), not of wood**: Similar to the previous one, but this code requires the product to be made of other materials besides wood.
4. **94035060 Furniture (o/than seats) of wood (o/than bentwood), of a kind used in the bedroom & designed for motor vehicle use**: This code is similar to the first one, but with an added design element that's not relevant for "beds".
5. **44212020 Wooden coffins not bamboo**: This code is clearly unrelated to beds.
6. **94035040 Furniture (o/than seats) of bentwood nesoi, of a kind used in the bedroom**: This code seems more focused on furniture made from bent wood, which might be too specific for "beds".
7. **63041910 Bedspreads, not knitted or crocheted, of cotton, nesoi**: This code is related to bedding and bed linens, but it's specifically about bedspreads, not beds.
8. **63021000 Bed linen, knitted or crocheted**: Same as the previous one; this code is about bed linens, not beds themselves.
9. **63041905 Bedspreads, not knitted or crocheted, of cotton, containing any embroidery, lace, etc.**: Again, related to bedding and bed linens.
10. **63041930 Bedspreads, not knitted or crocheted, other than those of cotton or man-made fibers, excluding those of heading 9404**: More general, but still about bed linens and not beds themselves.
11. **63041110 Bedspreads of cotton, knitted or crocheted, excluding those of heading 9404**: This code is specific to cotton bed linens.
12. **44149000 Wooden frames for paintings, photographs, mirrors or similar objects, not of tropical wood**: Clearly unrelated to beds.
13. **44141000 Wooden frames for paintings, photographs, mirrors or similar objects, of tropical wood**: Same as the previous one; no connection to beds.
14. **44209020 Wooden cigar and cigarette boxes**: Another unrelated code.

Considering all options, I would recommend using either **94014100 Seats nesoi, convertible into beds (o/than garden seats or camping equip.), of wood** or a combination of **94014100** with additional descriptive text to make it clear that the product is indeed "Wooden beds".

Please note that the accuracy of this answer depends on how the Harmonized System categorizes "beds" and whether these codes specifically cover the intended use case.
------

```json
[
  "94014100",
  "94035090"
]
```


parse the text between "------" and "------". In it there is a list of tariffs code that are good matches for "Airplane Seats". Prints them as a JSON array, containing only the codes. Output only the json nothing else.
