# CountryNames
This is a conversion tool that uses a web service API from Geonames to convert misspelled country names or names with alternate spellings into correctly spelled country names. How it works is that the first function (standardize_country) defines the name, username, and fuzzy level parameters. It then attempts to make an API call request and uses JSON to decode the API response. If the request is successful, it will then loop through the country names in the Geonames collection and return the country names if they match the names of independent countries. If no match is detected, it returns the default value.

For the second function (find_country_with_fuzzy), it simply loops through a range of numbers between 1 and 10 inclusively. It then divides the fuzzy value by 10 to output a random value between 0 and 1, where 0 is the strictest value and 1 is the most relaxed value. If no match is detected, it returns the default value.

For the tool to work without errors using the API, you need to create an account on Geonames. You can do so here: https://www.geonames.org/login. Once your account is created, you then need to enable free services on your account and assign your Geonames username to the username parameter variable (I.e., username == "Username goes here"). To test it out, simply type in any country name in quotes and deliberately misspell it (I.e., name == "Brzl").

Full list of countries: https://www.geonames.org/countries/
