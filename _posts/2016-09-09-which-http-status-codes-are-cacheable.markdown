---
layout:       post
title:        Which HTTP status codes are cacheable?
author:       Cássio Mazzochi Molin
date:         2016-09-09 08:19:32Z
excerpt:      A summary of the HTTP status codes defined as cacheable, according to the RFC 7231.
tags:         [http]
image:        /images/which-http-status-codes-are-cacheable.jpg
imageSource:  https://unsplash.com/photos/rL7BHmjUV50
---

## Short answer

According to the [RFC 7231][1], the current reference for content and semantics of the HTTP/1.1 protocol, the following HTTP status codes are defined as _cacheable_ unless otherwise indicated by the [method definition][2] or [explicit cache controls][3]:

- [`200` OK][4]
- [`203` Non-Authoritative Information][5]
- [`204` No Content][6]
- [`206` Partial Content][7]
- [`300` Multiple Choices][8]
- [`301` Moved Permanently][9]
- [`404` Not Found][10]
- [`405` Method Not Allowed][11]
- [`410` Gone][12]
- [`414` URI Too Long][13]
- [`501` Not Implemented][14]

## Long answer

The [RFC 7231][1] states the following regarding the HTTP status codes that are cacheable by default:

> [**6.1\. Overview of Status Codes**][15]
>
> [...] Responses with status codes that are defined as cacheable by default (e.g., `200`, `203`, `204`, `206`, `300`, `301`, `404`, `405`, `410`, `414`, and `501` in this specification) can be reused by a cache with heuristic expiration unless otherwise indicated by the [method definition][2] or [explicit cache controls][3]; all other status codes are not cacheable by default. [...]

Once the HTTP status codes are extensible, recipient must note cache a response with an unrecognized status code:

> [**6\. Response Status Codes**][16]
>
> The status-code element is a three-digit integer code giving the result of the attempt to understand and satisfy the request.
> HTTP status codes are extensible. HTTP clients are not required to understand the meaning of all registered status codes, though such understanding is obviously desirable. However, a client MUST understand the class of any status code, as indicated by the first digit, and treat an unrecognized status code as being equivalent to the `x00` status code of that class, with the exception that a recipient MUST NOT cache a response with an unrecognized status code. [...]

The cache also depends on the HTTP method:

> [**4.2.3\. Cacheable Methods**][17]
>
> Request methods can be defined as "cacheable" to indicate that responses to them are allowed to be stored for future reuse. In general, safe methods that do not depend on a current or authoritative response are defined as cacheable; this specification defines `GET`, `HEAD`, and `POST` as cacheable, although the overwhelming majority of cache implementations only support `GET` and `HEAD`.

Regarding the `POST` method, there's an important detail:

> [**4.3.3\. POST**][18]
>
> [...] Responses to `POST` requests are only cacheable when they include [explicit freshness information][19] [...]

For more details, check the [definition of each method][2].

# Additional resources

- [RFC 7234][20]: Reference for caching in the HTTP/1.1 protocol
- [Check what browsers store in their cache][21]

[1]: https://tools.ietf.org/html/rfc7231
[10]: https://tools.ietf.org/html/rfc7231#section-6.5.4
[11]: https://tools.ietf.org/html/rfc7231#section-6.5.5
[12]: https://tools.ietf.org/html/rfc7231#section-6.5.9
[13]: https://tools.ietf.org/html/rfc7231#section-6.5.12
[14]: https://tools.ietf.org/html/rfc7231#section-6.6.2
[15]: https://tools.ietf.org/html/rfc7231#section-6.1
[16]: https://tools.ietf.org/html/rfc7231#section-6
[17]: https://tools.ietf.org/html/rfc7231#section-4.2.3
[18]: https://tools.ietf.org/html/rfc7231#section-4.3.3
[19]: https://tools.ietf.org/html/rfc7234#section-4.2.1
[2]: https://tools.ietf.org/html/rfc7231#section-4.3
[20]: https://tools.ietf.org/html/rfc7234
[21]: http://stackoverflow.com/a/38307389/1426227
[3]: https://tools.ietf.org/html/rfc7234#section-5.2
[4]: https://tools.ietf.org/html/rfc7231#section-6.3.1
[5]: https://tools.ietf.org/html/rfc7231#section-6.3.4
[6]: https://tools.ietf.org/html/rfc7231#section-6.3.5
[7]: https://tools.ietf.org/html/rfc7233#section-4.1
[8]: https://tools.ietf.org/html/rfc7231#section-6.4.1
[9]: https://tools.ietf.org/html/rfc7231#section-6.4.2
