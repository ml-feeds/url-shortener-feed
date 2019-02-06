# url-shortener-feed
**url-shortener-feed** uses Python 3.7 to serve a modified RSS feed such that all item links in the original feed are
replaced with `j.mp` short links provided by Bitly.
As a disclaimer, it has no affiliation with Bitly.

## Links
* [Project repo](https://github.com/ml-feeds/url-shortener-feed)
* [Sample unmodified feed](https://us-east1-ml-feeds.cloudfunctions.net/kdnuggets)
* [**Sample modified feed**](https://us-east1-ml-feeds.cloudfunctions.net/url-shortener-feed?token=sample&url=https://us-east1-ml-feeds.cloudfunctions.net/kdnuggets)

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
Due to security considerations, use of the deployed service is restricted to approved users only.
An approved user must provide the supplied secret `token` and a `url` as parameters for a `GET` request.
The token must obviously not be committed to any public repository.

The output for a given URL is cached for 58 minutes.