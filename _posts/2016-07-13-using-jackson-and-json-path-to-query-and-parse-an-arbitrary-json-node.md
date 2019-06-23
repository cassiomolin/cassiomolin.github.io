---
title: Using Jackson and JSON Path to query and parse an arbitrary JSON node
date: 2016-07-13 13:19:05 Z
tags:
- java
- jackson
- json
layout: post
author: Cassio Mazzochi Molin
excerpt: Example of how to use JSON Path with Jackson.
featured_image: null
featured_image_thumbnail: null
---

_JSON Pointer_ is a string syntax for identifying a specific value within a JSON document, defined by the [RFC 6901][1]. Consider the following JSON:

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "address": {
    "street": "21 2nd Street",
    "city": "New York",
    "postalCode": "10021-3100",
    "coordinates": {
      "latitude": 40.7250387,
      "longitude": -73.9932568
    }
  }
}
```

The `coordinates` node can be identified by following JSON Pointer expression:

```nocode
/address/coordinates
```

Jackson 2.3.0 introduced support to JSON Pointer and it can be handy when we want to query a specific node from a JSON document:

```java
String json = "{\"firstName\":\"John\",\"lastName\":\"Doe\",\"address\":{\"street\":"
            + "\"21 2nd Street\",\"city\":\"New York\",\"postalCode\":\"10021-3100\","
            + "\"coordinates\":{\"latitude\":40.7250387,\"longitude\":-73.9932568}}}";

ObjectMapper mapper = new ObjectMapper();
JsonNode node = mapper.readTree(json);
JsonNode coordinatesNode = node.at("/address/coordinates");
```

Then the `coordinates` node could be parsed into a bean:

```java
public class Coordinates {

    private Double latitude;
    private Double longitude;

    // Getters and setters omitted
}
```

```java
Coordinates coordinates = mapper.treeToValue(coordinatesNode, Coordinates.class);
```

[1]: https://tools.ietf.org/html/rfc6901
[2]: https://github.com/jayway/JsonPath
[3]: http://jsonpath.com/
[4]: https://jsonpath.curiousconcept.com/
