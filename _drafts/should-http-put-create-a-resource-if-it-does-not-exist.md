---
title: Should HTTP PUT create a resource if it does not exist?
date: 2021-03-26 10:00:00 Z
tags:
- http
layout: post
author: Cassio Mazzochi Molin
excerpt: This post demonstrates how to combine Jackson Streaming API and the data binding capabilities provided by ObjectMapper to parse JSON content.
image: "/assets/images/drafts/should-http-put-create-a-resource-if-it-does-not-exist/cover.jpg"
image_source: https://unsplash.com/photos/aHhhdKUP77M
---

I first came across this [same question in Stack Overflow](https://stackoverflow.com/q/56240547/1426227) and I did provide an [answer](https://stackoverflow.com/a/56241060/1426227) to it. As my answer has been getting some upvotes recently, I thought it would deserve a cross-post here.

So back to the question:

> Should HTTP `PUT` create a resource if it does not exist?

Well, it depends.

The ultimate decision comes down to **how the resource identifiers are generated**:

- If the server allows the client to generate resource identifiers, then it would be fine to use [`PUT`][3] for creating resources.
- On the other hand, if the server generates resource identifiers on behalf of the client, then [`POST`][2] should be used instead of [`PUT`][3] for creating resources. 

Some parts of the [`PUT`][3] method definition are quoted below and the last sentence suppors what I have just mentioned above (highlight is mine):

> [**4.3.4.  PUT**][3]
>
>The `PUT` method requests that the state of the target resource be created or replaced with the state defined by the representation enclosed in the request message payload.  [...]
>
> If the target resource does not have a current representation and the `PUT` successfully creates one, then the origin server MUST inform the user agent by sending a `201` (Created) response.  If the target resource does have a current representation and that representation is successfully modified in accordance with the state of the enclosed representation, then the origin server MUST send either a `200` (OK) or a `204` (No Content) response to indicate successful completion of the request. [...]
>
> Proper interpretation of a `PUT` request presumes that the user agent knows which target resource is desired.  **A service that selects a proper URI on behalf of the client, after receiving a state-changing request, SHOULD be implemented using the `POST` method rather than `PUT`.** [...]

## Additional details

Now, for the sake of completeness, I added below some relevant quotes on the [`POST`][2] method definition:

>[**4.3.3.  POST**][2]
>
> The `POST` method requests that the target resource process the representation enclosed in the request according to the resource's own specific semantics. For example, `POST` is used for the following functions (among others):
>
> [...]
>
> - Creating a new resource that has yet to be identified by the origin server;
>
> [...]
>
>If one or more resources has been created on the origin server as a result of successfully processing a `POST` request, the origin server SHOULD send a `201` (Created) response containing a `Location` header field that provides an identifier for the primary resource created and a representation that describes the status of the request while referring to the new resource(s).

While the [`201`][5] status code indicates that a new resource has been created, the [`Location`][6] header indicate where the newly created resource is located. If no [`Location`][6] header is provided, then the client should assume that the resource is identified by the effective request URI:

>[**6.3.2. 201 Created**][5]
>
>The `201` (Created) status code indicates that the request has been fulfilled and has resulted in one or more new resources being created. The primary resource created by the request is identified by either a `Location` header field in the response or, if no `Location` field is received, by the effective request URI. [...]

  [rfc7230]: https://tools.ietf.org/html/rfc7230
  [rfc7231]: https://tools.ietf.org/html/rfc7231
  [rfc7232]: https://tools.ietf.org/html/rfc7232
  [rfc7233]: https://tools.ietf.org/html/rfc7233
  [rfc7234]: https://tools.ietf.org/html/rfc7234
  [rfc7235]: https://tools.ietf.org/html/rfc7235


  [1]: https://www.mnot.net/blog/2014/06/07/rfc2616_is_dead
  [2]: https://tools.ietf.org/html/rfc7231#section-4.3.3
  [3]: https://tools.ietf.org/html/rfc7231#section-4.3.4
  [4]: https://tools.ietf.org/html/rfc7231#section-6.5.4
  [5]: https://tools.ietf.org/html/rfc7231#section-6.3.2
  [6]: https://tools.ietf.org/html/rfc7231#section-7.1.2



  [com.fasterxml.jackson.core.JsonFactory]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonFactory.html
  [com.fasterxml.jackson.core.JsonParser]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonParser.html
  [com.fasterxml.jackson.core.JsonParser.nextToken]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonParser.html#nextToken--
  [com.fasterxml.jackson.core.JsonGenerator]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonGenerator.html
  [com.fasterxml.jackson.databind.ObjectMapper]: https://fasterxml.github.io/jackson-databind/javadoc/2.9/com/fasterxml/jackson/databind/ObjectMapper.html
  [com.fasterxml.jackson.core.TreeNode]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/TreeNode.html
  
  [repo]: https://github.com/cassiomolin/using-jackson-streaming-api-with-objectmapper.git
  
  [stax]: https://docs.oracle.com/javase/tutorial/jaxp/stax/api.html
  
