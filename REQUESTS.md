<A name="toc1-0" title="/fieldreport/create" />
# /fieldreport/create

Fields:

* `latitude` (optional)
* `longitude` (optional)
* `description` required (big text)
* `uuid` (optional) - any duplicates here will be rejected, generation on the client side for each individual report allows retries on network issues to be done safely without risk of duplicates

<A name="toc1-10" title="/fieldreport/create_api" />
# /fieldreport/create_api

Fields:

* `username` (required)
* `password` (required)
* `uuid` is now required, wheras it is optional for /fieldreport/create.
* All other fields the same as those in /fieldreport/create.
