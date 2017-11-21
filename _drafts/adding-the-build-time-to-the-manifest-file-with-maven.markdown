---
title: Adding the build timestamp to the manifest file with Maven
date: 2017-11-21 00:00:00 Z
tags:
- java
- maven
layout: post
author: Cassio Mazzochi Molin
excerpt: How to add the build timestamp to the MANIFEST.MF file for your JAR/WAR files.
image: 
imageSource: 
---

Both [`maven-war-plugin`][maven-war-plugin] and [`maven-jar-plugin`][maven-jar-plugin] allows you to define the entries of the `MANIFEST.MF` file of your WAR/JAR file. If you need to track the build timestamp of a particular artifact, it's a good place to add such metadata and the configuration is quite simple:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-war-plugin</artifactId>
    <configuration>
        <failOnMissingWebXml>false</failOnMissingWebXml>
        <archive>
            <manifestEntries>
                <Build-Time>${maven.build.timestamp}</Build-Time>
                <Project-Version>${project.version}</Project-Version>
            </manifestEntries>
        </archive>
    </configuration>
</plugin>
```

The format of the build timestamp can be customized by declaring the property `maven.build.timestamp.format` as shown in the example below:

```xml
<properties>
    <maven.build.timestamp.format>yyyy-MM-dd'T'HH:mm:ss'Z'</maven.build.timestamp.format>
</properties>
```

The format pattern has to comply with the rules given in the API documentation for [`SimpleDateFormat`][SimpleDateFormat]. If the property is not present, the format defaults to `yyyy-MM-dd'T'HH:mm:ss'Z'`.


  [SimpleDateFormat]: https://docs.oracle.com/javase/9/docs/api/java/text/SimpleDateFormat.html
  [maven-war-plugin]: https://maven.apache.org/plugins/maven-war-plugin/
  [maven-jar-plugin]: https://maven.apache.org/plugins/maven-jar-plugin/