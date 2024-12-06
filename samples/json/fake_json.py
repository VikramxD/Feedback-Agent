# pip install jsf <https://github.com/ghandic/jsf>
# can write a bunch of it to a file. TBD, all dates are above 1970, so should work

# Python port of faker-json js

from jsf import JSF

faker = JSF.from_json("../../analytics/schemas/keywords.json")

print(faker.generate())