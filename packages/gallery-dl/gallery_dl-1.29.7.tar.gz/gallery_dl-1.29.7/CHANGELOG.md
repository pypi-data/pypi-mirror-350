## 1.29.7 - 2025-05-23
### Extractors
#### Additions
- [mangadex] add `following` extractor ([#7487](https://github.com/mikf/gallery-dl/issues/7487))
- [pixeldrain] add support for filesystem URLs ([#7473](https://github.com/mikf/gallery-dl/issues/7473))
#### Fixes
- [bluesky] handle posts without `record` data ([#7499](https://github.com/mikf/gallery-dl/issues/7499))
- [civitai] fix & improve video downloads ([#7502](https://github.com/mikf/gallery-dl/issues/7502))
- [civitai] fix exception for images without `modelVersionId` ([#7432](https://github.com/mikf/gallery-dl/issues/7432))
- [civitai] make metadata extraction non-fatal ([#7562](https://github.com/mikf/gallery-dl/issues/7562))
- [fanbox] use `"browser": "firefox"` by default ([#7490](https://github.com/mikf/gallery-dl/issues/7490))
- [idolcomplex] fix pagination logic ([#7549](https://github.com/mikf/gallery-dl/issues/7549))
- [idolcomplex] fix 429 error during login by adding a 10s delay
- [instagram:stories] fix `post_date` metadata ([#7521](https://github.com/mikf/gallery-dl/issues/7521))
- [motherless] fix video gallery downloads ([#7530](https://github.com/mikf/gallery-dl/issues/7530))
- [pinterest] handle `story_pin_product_sticker_block` blocks ([#7563](https://github.com/mikf/gallery-dl/issues/7563))
- [subscribestar] fix `content` and `title` metadata ([#7486](https://github.com/mikf/gallery-dl/issues/7486) [#7526](https://github.com/mikf/gallery-dl/issues/7526))
#### Improvements
- [arcalive] allow overriding default `User-Agent` header ([#7556](https://github.com/mikf/gallery-dl/issues/7556))
- [fanbox] update API headers ([#7490](https://github.com/mikf/gallery-dl/issues/7490))
- [flickr] add `info` option ([#4720](https://github.com/mikf/gallery-dl/issues/4720) [#6817](https://github.com/mikf/gallery-dl/issues/6817))
- [flickr] add `profile` option
- [instagram:stories] add `split` option ([#7521](https://github.com/mikf/gallery-dl/issues/7521))
- [mangadex] implement login with client credentials
- [mangadex] send `Authorization` header only when necessary
- [mastodon] support Akkoma/Pleroma `/notice/:ID` URLs ([#7496](https://github.com/mikf/gallery-dl/issues/7496))
- [mastodon] support Akkoma/Pleroma `/objects/:UUID` URLs ([#7497](https://github.com/mikf/gallery-dl/issues/7497))
- [pixiv] Implement sanity handling for ugoira works ([#4327](https://github.com/mikf/gallery-dl/issues/4327) [#6297](https://github.com/mikf/gallery-dl/issues/6297) [#7285](https://github.com/mikf/gallery-dl/issues/7285) [#7434](https://github.com/mikf/gallery-dl/issues/7434))
- [twitter:ctid] reduce chance of generating the same ID
#### Metadata
- [civitai] provide proper `extension` for model files ([#7432](https://github.com/mikf/gallery-dl/issues/7432))
- [flickr] provide `license_name` metadata
- [sankaku] support new `tags` categories ([#7333](https://github.com/mikf/gallery-dl/issues/7333) [#7553](https://github.com/mikf/gallery-dl/issues/7553))
- [vipergirls] provide `num` and `count` metadata ([#7479](https://github.com/mikf/gallery-dl/issues/7479))
- [vipergirls] extract more metadata & rename fields ([#7479](https://github.com/mikf/gallery-dl/issues/7479))
### Downloaders
- [http] fix setting `mtime` per file ([#7529](https://github.com/mikf/gallery-dl/issues/7529))
- [ytdl] improve temp/part file handling ([#6949](https://github.com/mikf/gallery-dl/issues/6949) [#7494](https://github.com/mikf/gallery-dl/issues/7494))
### Cookies
- support Zen browser ([#7233](https://github.com/mikf/gallery-dl/issues/7233) [#7546](https://github.com/mikf/gallery-dl/issues/7546))
