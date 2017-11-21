---
title: Using CDI with Weld in a Java SE environment
date: 2017-11-21 00:00:00 Z
tags:
- java
- weld
- cdi
layout: post
author: Cassio Mazzochi Molin
excerpt: How to bootstrap the Weld container in a Java SE environment.
image: 
imageSource: 
---

```java
public class Application {
    
    public static void main(String[] args) {

        // Initialize the container
        Weld weld = new Weld();
        WeldContainer container = weld.initialize();
        
        // Select a bean and invoke a business method
        container.select(MyApplicationBean.class).get().helloWorld();
        
        // Shut the container down
        container.shutdown();
    }
}
```

```java
@ApplicationScoped
public class MyApplicationBean {
    
    public void helloWorld() {
        System.out.println("Hello World!")
    }
}
```

Check the [Weld documentation][Weld documentation] for more details.

 [Weld documentation]: https://docs.jboss.org/weld/reference/latest/en-US/html/environments.html#_bootstrapping_cdi_se