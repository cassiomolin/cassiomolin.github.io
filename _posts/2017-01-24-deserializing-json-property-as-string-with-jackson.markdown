---
layout:  post
title:   Deserializing JSON property as String with Jackson
author:  Cássio Mazzochi Molin
date:    2017-01-24 15:04:58Z
excerpt: Writing a custom deserializer to read a JSON property as String with Jackson.
tags:    [java, json, jackson]
image:   /images/deserializing-json-property-as-string-with-jackson.jpg
---

A while ago I faced a situation that it was necessary to parse a JSON like this:

```json
{
  "payload": {
    "foo": "bar",
    "biz": [
      "lorem",
      "ipsum"
    ]
  },
  "signature": "somehmacsign"
}
```

Into this Java class:

```java
public class Request {

    private String payload;
    private String signature;

    // Getters and setters omitted
}
```

The challenge here is to read the content of the `payload` property (which can be any valid JSON object/array/value) into a string. That is, the content of the `payload` property must not be parsed into a POJO.

It could be achieved with the following custom deserializer:

```java
public class RawJsonDeserializer extends JsonDeserializer<String> {

    @Override
    public String deserialize(JsonParser jp, DeserializationContext ctxt)
           throws IOException, JsonProcessingException {

        ObjectMapper mapper = (ObjectMapper) jp.getCodec();
        JsonNode node = mapper.readTree(jp);
        return mapper.writeValueAsString(node);
    }
}
```

Then annotate the `payload` attribute with the [`@JsonDeserialize`][2] annotation, referencing the deserializer created above:

```java
public class Request {

    @JsonDeserialize(using = RawJsonDeserializer.class)
    private String payload;

    private String signature;

    // Getters and setters omitted
}
```

And parse the JSON using [`ObjectMapper`][1]:

```java
String json = "{\"payload\":{\"foo\":\"bar\",\"biz\":[\"lorem\","
            + "\"ipsum\"]},\"signature\":\"somehmacsign\"}";

ObjectMapper mapper = new ObjectMapper();
Request request = mapper.readValue(json, Request.class);
```

Since the deserializer defined above will parse the JSON into the Jackson tree model and then serialize it back to a string, the result may not be equal to the original content of the `payload` property. If you want to keep the spaces, tabs, line breaks and the order of the JSON properties, have a look at the following implementation, which won't parse the JSON into the Jackson tree model:

```java
public class RawJsonDeserializer extends JsonDeserializer<String> {

    @Override
    public String deserialize(JsonParser jp, DeserializationContext ctxt)
           throws IOException, JsonProcessingException {

        long begin = jp.getCurrentLocation().getCharOffset();
        jp.skipChildren();
        long end = jp.getCurrentLocation().getCharOffset();

        String json = jp.getCurrentLocation().getSourceRef().toString();
        return json.substring((int) begin - 1, (int) end);
    }
}
```

In both deserializers, an exception will be throw if the JSON is invalid.


[1]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/ObjectMapper.html
[2]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/annotation/JsonDeserialize.html
[3]: http://stackoverflow.com/q/38864072/1426227
