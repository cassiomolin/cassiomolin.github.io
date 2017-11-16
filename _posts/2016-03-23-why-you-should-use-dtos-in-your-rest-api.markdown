---
layout:  post
title:   Why you should use DTOs in your REST API
author:  Cássio Mazzochi Molin
date:    2016-03-23 10:16:45Z
excerpt: Why you should consider using Data Transfer Objects instead of persistence models in your REST API.
tags:    [rest, java, dto]
image:   /images/why-you-should-use-dtos-in-your-rest-api.jpg
---

**DTO** stands for [**D**ata **T**ransfer **O**bject][1]. 

This pattern was created with a very well defined purpose: **transfer data to _remote interfaces_**, just like *web services*. This pattern fits very well in a REST API and DTOs will give you more *flexibility* in the long run. And your REST resources representations don't need to have the same attributes as the persistence objects.

Just to mention a few benefits: 

- DTOs can be *tailored* to your needs and they are great when exposing only a set of attributes of your persistence entities. You won't need annotations such as [`@XmlTransient`][2] and [`@JsonIgnore`][3] to avoid the serialization of some attributes.
- By using DTOs, you will avoid a *hell of annotations* in your persistence entities, that is, your persistence entities won't be bloated with non persistence related annotations;
- You will have *full control* over the attributes you are receiving when creating or updating a resource;
- If you are using [Swagger][4], you can use [`@ApiModel`][5] and [`@ApiModelProperty`][6] annotations to document your API models without messing your persistence entities;
- You can have different DTOs for each version of your API;
- You'll have more flexibility when mapping relationships;
- You can have different DTOs for different media types;
- Your DTOs can have a list of links for [HATEOAS][7]. That's the kind of thing that shouldn't be added to persistence objects.

## Mapping frameworks

You won't need to map your persistence entities to DTOs and vice versa *mannually*. There are [many mapping frameworks][8] you can use to do it. For instance, have a look at [MapStruct][9], which is annotation based and works as a Maven Annotation Processor. It also works in CDI and Spring-based applications.


  [1]: https://en.wikipedia.org/wiki/Data_transfer_object
  [2]: http://docs.oracle.com/javaee/7/api/javax/xml/bind/annotation/XmlTransient.html
  [3]: https://fasterxml.github.io/jackson-annotations/javadoc/2.7/com/fasterxml/jackson/annotation/JsonIgnore.html
  [4]: https://github.com/swagger-api/swagger-core
  [5]: https://github.com/swagger-api/swagger-core/wiki/Annotations-1.5.X#apimodel
  [6]: https://github.com/swagger-api/swagger-core/wiki/Annotations-1.5.X#apimodelproperty
  [7]: https://en.wikipedia.org/wiki/HATEOAS
  [8]: https://stackoverflow.com/a/1432956/1426227
  [9]: http://mapstruct.org/
  [10]: https://stackoverflow.com/a/35341664/1426227