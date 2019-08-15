---
title: Comparing JSON documents in Java with JSON-P
date: 2019-08-08 23:00:00 Z
tags:
- java
- json
- javax-json
layout: post
author: Cassio Mazzochi Molin
excerpt: This post demonstrates how to compare JSON documents in Java with JSON-P.
featured_image: "/assets/images/posts/owl.jpg"
featured_image_thumbnail: "/assets/images/posts/owl_small.jpg"
featured: true
hidden: true
redirect_from:
  - /comparing-json-documents-in-java-with-jsonp/
---



In a [previous post][blog.comparing-json-documents], I demonstrated how to compare JSON documents using Jackson and Gson, taking advantage of Java 8 streams and Guava for comparing the documents as flat maps.

In this post, I approach the comparison of JSON documents from another perspective, using _JSON-P_, also known as _Java API for JSON Processing_. <!-- TODO: An example is available on [GitHub][repo]. -->



<!--more-->



##### Table of contents 
{:.no_toc}

* TOC 
{:toc}



## Representing the differences between two JSON documents

While the approach described in the [previous post][blog.comparing-json-documents] simply focus in _listing_ the differences between two JSON documents, the approach described in this post focus in producing another JSON document that represents the differences between the two documents that have been compared. And the great thing about this is that the JSON document representing the differences can be applied to the first JSON document that has been compared, yielding the second JSON document that has been compared.

But before diving into the code to perform the comparison, let's have a look at two standard formats that can be used to represent the differences between JSON documents: _JSON Patch_ and _JSON Merge Patch_.

These formats are meant to represent set of instructions describing how the target document will be modified. Hence they are suitable for using as payload of [`PATCH`][rfc5789] requests (see this [post][blog.using-patch-in-spring] for further details).



### JSON Patch

[JSON Patch][rfc6902] is a format for expressing a sequence of operations to be applied to a JSON document. It is defined in the [RFC 6902][rfc6902] and is identified by the `application/json-patch+json` media type.

The JSON Patch document represents an array of objects and each object represents a single operation to be applied to the target JSON document. 

The evaluation of a JSON Patch document begins against a target JSON document and the operations are applied sequentially in the order they appear in the array. Each operation in the sequence is applied to the target document and the resulting document becomes the target of the next operation. The evaluation continues until all operations are successfully applied or until an error condition is encountered.

The operation objects must have exactly one `op` member, whose value indicates the operation to perform:

| Operation | Description |
| --------- | ----------- |
| [`add`][rfc6902.add] | Adds the value at the target location; if the value exists in the given location, it's replaced |
| [`remove`][rfc6902.remove] | Removes the value at the target location |
| [`replace`][rfc6902.replace] | Replaces the value at the target location |
| [`move`][rfc6902.move] | Removes the value at a specified location and adds it to the target location |
| [`copy`][rfc6902.copy] | Copies the value at a specified location to the target location |
| [`test`][rfc6902.test] | Tests that a value at the target location is equal to a specified value |

Any other values are considered errors.



### JSON Merge Patch

[JSON Merge Patch][rfc7396] is a format that describes the changes to be made to a target JSON document using a syntax that closely mimics the document being modified. It is defined in the [RFC 7396][rfc7396] is identified by the `application/merge-patch+json` media type.

The server processing a JSON Merge Patch document determine the exact set of changes being requested by comparing the content of the provided patch against the current content of the target document: 

- If the merge patch contains members that do not appear within the target document, those members are _added_.
- If the target does contain the member, the value is _replaced_.
- _null_ values in the merge patch indicate that existing values in the target document are to be _removed_.
- Other values in the target document will remain _untouched_.



## JSON-P: Java API for JSON Processing

[JSON-P][jsonp], also known as _Java API for JSON Processing_, defines portable APIs under the [`javax.json`][javax.json] package to parse, generate, transform, and query JSON using object model and streaming APIs.

JSON-P 1.0 was initially defined in the [JSR 353][jsr353] and brought what Oracle calls _official support_ for JSON processing in Java EE. Later, in the [JSR 374][jsr374], JSON-P has evolved and introduced support for JSON Patch and JSON Merge Patch formats to Java EE.

Let's have a quick look at the API to start getting familiar with it: 

| Type | Description |
| ---- | ----------- |
| [`Json`][javax.json.Json] | Factory class for creating JSON processing objects |
| [`JsonPatch`][javax.json.JsonPatch] | Represents an implementation of JSON Patch |
| [`JsonMergePatch`][javax.json.JsonMergePatch] | Represents an implementation of JSON Merge Patch |
| [`JsonValue`][javax.json.JsonValue] | Represents an immutable JSON value that can be an [_object_][javax.json.JsonObject], an [_array_][javax.json.JsonArray], a [_number_][javax.json.JsonNumber], a [_string_][javax.json.JsonString], [_`true`_][javax.json.JsonValue.TRUE], [_`false`_][javax.json.JsonValue.FALSE] or [_`null`_][javax.json.JsonValue.NULL] |
| [`JsonStructure`][javax.json.JsonStructure] | Super type for the two structured types in JSON: [_object_][javax.json.JsonObject] and [_array_][javax.json.JsonArray] |

Having said that, it's important to highlight that JSON-P is just a set of APIs and does nothing on it's own. To actually work with it, we need an implementation. There are some interesting implementation around and, for this example, we'll use [Apache Johnzon][apache.johnzon]:

```xml
<!-- JSON-P: Java API for JSON Processing (JSR 374) -->
<dependency>
    <groupId>javax.json</groupId>
    <artifactId>javax.json-api</artifactId>
    <version>${javax-json.version}</version>
</dependency>

<!-- Apache Johnzon: Implementation of the Java API for JSON Processing (JSR 374) -->
<dependency>
    <groupId>org.apache.johnzon</groupId>
    <artifactId>johnzon-core</artifactId>
    <version>${johnzon.version}</version>
</dependency>
```

For comparison purposes, JSON-P is to JPA as Apache Johnzon is to Hibernate.

And let me also highlight that our code won't get tied to any implementation, as we will use only types from the JSON-P API.



## Using JSON-P to create JSON documents representing the differences

The [`Json`][javax.json.Json] factory class can be used for creating JSON processing objects, and can be used to create representations of the differences between given source and target documents. And this document with the differences, when applied to the source document, yields the target document.



### Creating a JSON Patch document with the differences

To create JSON Patch document with the differences between a source and target documents, we can use the [`createDiff()`][javax.json.Json.createDiff] method:

```java
JsonPatch diff = Json.createDiff(source, target);
```



### Creating a JSON Merge Patch document with the differences

To create JSON Merge Patch document with the differences between a source and target documents, we can use the [`createMergeDiff()`][javax.json.Json.createMergeDiff] method:

```java
JsonMergePatch mergeDiff = Json.createMergeDiff(source, target);
```



## Example

For example purposes, let's consider two JSON documents that represent details of a contact:

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



### Pretty printing JSON documents using JSON-P

For better visualization, we'll pretty print the JSON documents using the following code:

```java
System.out.println(format(diff.toJsonArray()));
System.out.println(format(mergeDiff.toJsonValue()));
```

```java
public static String format(JsonValue jsonValue) {
    StringWriter stringWriter = new StringWriter();
    prettyPrint(jsonValue, stringWriter);
    return stringWriter.toString();
}

public static void prettyPrint(JsonValue jsonValue, Writer writer) {
    Map<String, Object> config = Collections.singletonMap(JsonGenerator.PRETTY_PRINTING, true);
    JsonWriterFactory writerFactory = Json.createWriterFactory(config);
    try (JsonWriter jsonWriter = writerFactory.createWriter(writer)) {
        jsonWriter.write(jsonValue);
    }
}
```



### Producing a JSON Patch document with the differences

To produce a JSON Patch with the differences between two JSON documents we can use:

```java
JsonValue source = Json.createReader(new StringReader(leftJsonDocument)).readValue();
JsonValue target = Json.createReader(new StringReader(rightJsonDocument)).readValue();

JsonPatch diff = Json.createDiff(source.asJsonObject(), target.asJsonObject());
System.out.println(format(diff.toJsonArray()));
```

And it will produce the following output:

```json
[
  {
    "op":"replace",
    "path":"/name/first",
    "value":"Jane"
  },
  {
    "op":"add",
    "path":"/name/nickname",
    "value":"Jenny"
  },
  {
    "op":"remove",
    "path":"/address"
  },
  {
    "op":"replace",
    "path":"/birthday",
    "value":"1990-01-01"
  },
  {
    "op":"remove",
    "path":"/company"
  },
  {
    "op":"replace",
    "path":"/occupation",
    "value":null
  },
  {
    "op":"replace",
    "path":"/phones/0/number",
    "value":"111111111"
  },
  {
    "op":"replace",
    "path":"/phones/0/type",
    "value":"mobile"
  },
  {
    "op":"remove",
    "path":"/phones/1"
  },
  {
    "op":"add",
    "path":"/favorite",
    "value":true
  },
  {
    "op":"add",
    "path":"/groups",
    "value":[
      "close-friends",
      "gym"
    ]
  }
]
```



### Producing a JSON Merge Patch document with the differences

To produce a JSON Merge Patch with the differences between two JSON documents we can use:

```java
JsonValue source = Json.createReader(new StringReader(leftJsonDocument)).readValue();
JsonValue target = Json.createReader(new StringReader(rightJsonDocument)).readValue();

JsonMergePatch mergeDiff = Json.createMergeDiff(source, target);
System.out.println(format(mergeDiff.toJsonValue()));
```

And the output will be:

```json
{
  "name":{
    "first":"Jane",
    "nickname":"Jenny"
  },
  "address":null,
  "birthday":"1990-01-01",
  "company":null,
  "occupation":null,
  "phones":[
    {
      "number":"111111111",
      "type":"mobile"
    }
  ],
  "favorite":true,
  "groups":[
    "close-friends",
    "gym"
  ]
}
```



### Applying the patch documents

Consider the following code that applies JSON Patch to a document:

```java
JsonPatch diff = ...
JsonValue patched = diff.apply(source.asJsonObject());
System.out.println(format(patched));
```

It produces:

```json
{
  "name":{
    "last":"Doe",
    "nickname":"Jenny",
    "first":"Jane"
  },
  "groups":[
    "close-friends",
    "gym"
  ],
  "favorite":true,
  "occupation":null,
  "birthday":"1990-01-01",
  "phones":[
    {
      "number":"111111111",
      "type":"mobile"
    }
  ]
}
```

Now consider the following code that applies JSON Merge Patch to a document:

```java
JsonMergePatch mergeDiff = ...
JsonValue patched = mergeDiff.apply(source);
System.out.println(format(patched));
```

It produces:

```json
{
  "name":{
    "first":"Jane",
    "last":"Doe",
    "nickname":"Jenny"
  },
  "birthday":"1990-01-01",
  "phones":[
    {
      "number":"111111111",
      "type":"mobile"
    }
  ],
  "favorite":true,
  "groups":[
    "close-friends",
    "gym"
  ]
}
```



### Different results when applying the patches

When the JSON Patch and the JSON Merge Patch documents are applied to the target document, the results are _slightly different_. Have a closer look to the documents shown above.

The order of the properties of the JSON object is different, but that shouldn't be taken into account, as a JSON object is an _unordered_ collection of zero or more name/value pairs, according to the [RFC 8259][rfc8259]:

{: .long}
> An object is an unordered collection of zero or more name/value pairs, where a name is a string and a value is a string, number, boolean, `null`, object, or array.

The key difference here is:

- In the first example, the `occupation` property is `null`.
- In the second example, the `occupation` property is omitted. 

And it happens due to the `null` semantics on JSON Merge Patch. Quoting the [RFC 7396][rfc7396] (highlight is mine):

{: .long}
> If the target does contain the member, the value is replaced. Null values in the merge patch are given special meaning to indicate the removal of existing values in the target. [...]
>
> This design means that merge patch documents are suitable for describing modifications to JSON documents that primarily use objects for their structure and do not make use of explicit null values.  **The merge patch format is not appropriate for all JSON syntaxes.**



## References

- [RFC 6902][rfc6902]: JSON Patch
- [RFC 7396][rfc7396]: JSON Merge Patch
- [`javax.json`][javax.json]: Java API for JSON processing


  [repo]: https://github.com/cassiomolin/comparing-json-documents

  [javax.json]: https://javaee.github.io/javaee-spec/javadocs/javax/json/package-summary.html
  [javax.json.JsonPatch]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonPatch.html
  [javax.json.JsonMergePatch]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonMergePatch.html
  [javax.json.Json]: https://javaee.github.io/javaee-spec/javadocs/javax/json/Json.html
  [javax.json.JsonValue]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonValue.html
  [javax.json.JsonValue.TRUE]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonValue.html#TRUE
  [javax.json.JsonValue.FALSE]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonValue.html#FALSE
  [javax.json.JsonValue.NULL]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonValue.html#NULL
  [javax.json.JsonStructure]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonStructure.html
  [javax.json.JsonObject]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonObject.html
  [javax.json.JsonArray]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonArray.html
  [javax.json.JsonNumber]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonNumber.html
  [javax.json.JsonString]: https://javaee.github.io/javaee-spec/javadocs/javax/json/JsonString.html
  [javax.json.Json.createDiff]: https://javaee.github.io/javaee-spec/javadocs/javax/json/Json.html#createDiff-javax.json.JsonStructure-javax.json.JsonStructure-
  [javax.json.Json.createMergeDiff]: https://javaee.github.io/javaee-spec/javadocs/javax/json/Json.html#createMergeDiff-javax.json.JsonValue-javax.json.JsonValue-

  [rfc6902]: https://tools.ietf.org/html/rfc6902
  [rfc6902.add]: https://tools.ietf.org/html/rfc6902#section-4.1
  [rfc6902.remove]: https://tools.ietf.org/html/rfc6902#section-4.2
  [rfc6902.replace]: https://tools.ietf.org/html/rfc6902#section-4.3
  [rfc6902.move]:https://tools.ietf.org/html/rfc6902#section-4.4
  [rfc6902.copy]: https://tools.ietf.org/html/rfc6902#section-4.5
  [rfc6902.test]: https://tools.ietf.org/html/rfc6902#section-4.6

  [rfc7396]: https://tools.ietf.org/html/rfc7396

  [rfc8259]: https://tools.ietf.org/html/rfc8259

  [rfc5789]: https://tools.ietf.org/html/rfc5789

  [jsonp]: https://javaee.github.io/jsonp
  [apache.johnzon]: https://johnzon.apache.org/

  [blog.comparing-json-documents]: https://cassiomolin.com/2018/07/23/comparing-json-documents-in-java/
  [blog.using-patch-in-spring]: https://cassiomolin.com/2019/06/10/using-http-patch-in-spring/

  [jsr353]: https://www.jcp.org/en/jsr/detail?id=353
  [jsr374]: https://www.jcp.org/en/jsr/detail?id=374
