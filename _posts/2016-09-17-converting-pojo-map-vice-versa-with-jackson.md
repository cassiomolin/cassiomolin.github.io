---
title: Converting POJO to Map and vice versa with Jackson
date: 2016-09-17 08:21:54 Z
tags:
- java
- jackson
layout: post
author: Cassio Mazzochi Molin
excerpt: Jackson API makes it easy to covert Java objects to a map instance and vice versa.
image: '/images/posts/2016-09-17-converting-pojo-map-vice-versa-with-jackson/cover.jpg'
---

A quick look at how to convert a POJO from/to a [`Map<K, V>`][1] with Jackson:

```java
// Create ObjectMapper instance
ObjectMapper mapper = new ObjectMapper();

// Converting POJO to Map
Map<String, Object> map = mapper.convertValue(foo, new TypeReference<Map<String, Object>>() {});

// Convert Map to POJO
Foo anotherFoo = mapper.convertValue(map, Foo.class);
```

According to the Jackson [documentation][2], the `convertValue()` method is functionally similar to first serializing given value into JSON, and then binding JSON data into value of given type, but should be more efficient since full serialization does not (need to) occur. However, same converters (serializers and deserializers) will be used as for data binding, meaning same object mapper configuration works.

[1]: https://docs.oracle.com/javase/8/docs/api/java/util/Map.html
[2]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/ObjectMapper.html#convertValue(java.lang.Object,%20java.lang.Class)
