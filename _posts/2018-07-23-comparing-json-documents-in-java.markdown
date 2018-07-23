---
title: Comparing JSON documents in Java
date: 2018-07-23 19:03:00 Z
tags:
- java
- json
- jackson
- gson
- guava
layout: post
author: Cassio Mazzochi Molin
excerpt: My insights on comparing JSON documents in Java.
image: "/images/comparing-json-documents-in-java.jpg"
imageSource: https://unsplash.com/photos/SQM0sS0htzw
---

I recently came across the challenge of comparing JSON documents in Java. Once JSON documents are a set of key/value pairs, my first approach was to read the JSON documents as [`Map<K, V>`][Map] instances and then compare them. 

Reading the JSON documents as [`Map<K, V>`][Map] it's pretty straightforward with both [Jackson] and [Gson], the most popular JSON parsers for Java:

```java
ObjectMapper mapper = new ObjectMapper();
TypeReference<HashMap<String, Object>> type = new TypeReference<>() {};

Map<String, Object> leftMap = mapper.readValue(leftJson, type);
Map<String, Object> rightMap = mapper.readValue(rightJson, type);
```

```java
Gson gson = new Gson();
Type type = new TypeToken<Map<String, Object>>(){}.getType();

Map<String, Object> leftMap = gson.fromJson(leftJson, type);
Map<String, Object> rightMap = gson.fromJson(rightJson, type);
```

Then I used [Guava]'s [`Maps.difference(Map<K, V>, Map<K, V>)`][Maps.difference] for comparing the maps. It returns a [`MapDifference<K, V>`][MapDifference] instance:

```java
MapDifference<String, Object> difference = Maps.difference(left, right);
```

Everything was good until I had to compare complex JSON documents, with nested objects and arrays. A JSON document with nested objects is represented as a map of maps and [`Maps.difference(Map<K, V>, Map<K, V>)`][Maps.difference] doesn't give nice comparison results for that.

My next approach was to flat the maps and then compare them. It provided me with better comparison results especially for complex JSON documents.

## Creating flat Maps for the comparison

To flat the map, I wrote this utility class:

```java
public final class FlatMapUtil {

    private FlatMapUtil() {
        throw new AssertionError("No instances for you!");
    }

    public static Map<String, Object> flatten(Map<String, Object> map) {
        return map.entrySet().stream()
                .flatMap(FlatMapUtil::flatten)
                .collect(LinkedHashMap::new, (m, e) -> m.put("/" + e.getKey(), e.getValue()), LinkedHashMap::putAll);
    }

    private static Stream<Map.Entry<String, Object>> flatten(Map.Entry<String, Object> entry) {

        if (entry == null) {
            return Stream.empty();
        }

        if (entry.getValue() instanceof Map<?, ?>) {
            return ((Map<?, ?>) entry.getValue()).entrySet().stream()
                    .flatMap(e -> flatten(new AbstractMap.SimpleEntry<>(entry.getKey() + "/" + e.getKey(), e.getValue())));
        }

        if (entry.getValue() instanceof List<?>) {
            List<?> list = (List<?>) entry.getValue();
            return IntStream.range(0, list.size())
                    .mapToObj(i -> new AbstractMap.SimpleEntry<String, Object>(entry.getKey() + "/" + i, list.get(i)))
                    .flatMap(FlatMapUtil::flatten);
        }

        return Stream.of(entry);
    }
}
```

It uses the _JSON Pointer_ notation defined in the [RFC 6901] for the keys, so I can easily locate the values.

## Example

Consider the following JSON documents:

```json
{
  "name": {
    "first": "John",
    "last": "Doe"
  },
  "address": null,
  "birthday": "1980-01-01",
  "company": "Acme",
  "occupation": "Software engineer",
  "phones": [
    {
      "number": "000000000",
      "type": "home"
    },
    {
      "number": "999999999",
      "type": "mobile"
    }
  ]
}
```

```json
{
  "name": {
    "first": "Jane",
    "last": "Doe",
    "nickname": "Jenny"
  },
  "birthday": "1990-01-01",
  "occupation": null,
  "phones": [
    {
      "number": "111111111",
      "type": "mobile"
    }
  ],
  "favorite": true,
  "groups": [
    "close-friends",
    "gym"
  ]
}
```

And the following code to compare them and show the differences:

```java
Map<String, Object> leftFlatMap = FlatMapUtil.flatten(leftMap);
Map<String, Object> rightFlatMap = FlatMapUtil.flatten(rightMap);

MapDifference<String, Object> difference = Maps.difference(leftFlatMap, rightFlatMap);

System.out.println("Entries only on the left\n--------------------------");
difference.entriesOnlyOnLeft().forEach((key, value) -> System.out.println(key + ": " + value));

System.out.println("\n\nEntries only on the right\n--------------------------");
difference.entriesOnlyOnRight().forEach((key, value) -> System.out.println(key + ": " + value));

System.out.println("\n\nEntries differing\n--------------------------");
difference.entriesDiffering().forEach((key, value) -> System.out.println(key + ": " + value));
```      

It will produce the following output:

```
Entries only on the left
--------------------------
/address: null
/phones/1/number: 999999999
/phones/1/type: mobile
/company: Acme


Entries only on the right
--------------------------
/name/nickname: Jenny
/groups/0: close-friends
/groups/1: gym
/favorite: true


Entries differing
--------------------------
/birthday: (1980-01-01, 1990-01-01)
/occupation: (Software engineer, null)
/name/first: (John, Jane)
/phones/0/number: (000000000, 111111111)
/phones/0/type: (home, mobile)
```

  [Map]: https://docs.oracle.com/javase/10/docs/api/java/util/Map.html
  [Jackson]: https://github.com/FasterXML/jackson
  [Gson]: https://github.com/google/gson
  [Guava]: https://github.com/google/guava
  [Maps.difference]: https://google.github.io/guava/releases/23.0/api/docs/com/google/common/collect/Maps.html#difference-java.util.Map-java.util.Map-
  [MapDifference]: https://google.github.io/guava/releases/23.0/api/docs/com/google/common/collect/MapDifference.html
  [RFC 6901]: https://tools.ietf.org/html/rfc6901