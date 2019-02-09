# url-shortener-feed
**url-shortener-feed** uses Python 3.7 to serve a modified RSS or Atom feed such that all item links in the original
feed are replaced with `j.mp` short links provided by Bitly.
As a disclaimer, it has no affiliation with Bitly.

Support for Atom is nascent.

## Links
* [Project repo](https://github.com/ml-feeds/url-shortener-feed)
* [Sample unmodified RSS feed](https://us-east1-ml-feeds.cloudfunctions.net/kdnuggets)
* [**Sample modified RSS feed**](https://us-east1-ml-feeds.cloudfunctions.net/url-shortener?token=sample&url=https://us-east1-ml-feeds.cloudfunctions.net/kdnuggets)
* [Sample unmodified Atom feed](https://feeds.feedburner.com/blogspot/gJZg)
* [**Sample modified Atom feed**](https://us-east1-ml-feeds.cloudfunctions.net/url-shortener?token=sample&url=https://feeds.feedburner.com/blogspot/gJZg)

## Service deployment
Serverless deployment to [Google Cloud Functions](https://console.cloud.google.com/functions/) is configured.
It requires the following files:
* requirements.txt
* main.py (having callable `serve(request: flask.Request) -> Tuple[bytes, int, Dict[str, str]]`)

It requires the following environment variables:
* USF_TOKENS: a comma-separated list of tokens for access to this service
* BITLY_TOKENS: a comma-separated list of tokens for access to the Bitly service

Deployment version updates are not automated.
They can be performed manually by editing and saving the function configuration.

These deployment links require access:
* [Dashboard](https://console.cloud.google.com/functions/details/us-east1/url-shortener?project=ml-feeds)
* [Logs](https://console.cloud.google.com/logs?service=cloudfunctions.googleapis.com&key1=url-shortener&key2=us-east1&project=ml-feeds)
* [Repo](https://source.cloud.google.com/ml-feeds/github_ml-feeds_url-shortener-feed)

## Service usage
Due to security considerations, with the exception of the sample feed, use of the deployed service is restricted to
approved users only.
An approved user must provide the supplied secret `token` and a `url` as query parameters for a `GET` request.
The token must obviously not be committed to any public repository.

The output for a given URL is cached for 58 minutes.
