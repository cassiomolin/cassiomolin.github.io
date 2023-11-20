---
title: Performing action when web application is starting and shutting down
date: 2016-09-09
tags:
- cdi
- ejb
- java
- servlet
summary: Examples of how to execute operations when the application starts up or shuts down using Servlets, CDI and EJB.
aliases:
- /2016/09/09/performing-action-when-web-application-is-starting-and-shutting-down/
---

There are at least three ways to perform actions when a web application is starting and shutting down:

## Using `ServletContextListener` from the Servlet API

Keeping things simple, you can implement [`ServletContextListener`][1]:

```java
@WebListener
public class StartupListener implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent event) {
        // Perform action during application's startup
    }

    @Override
    public void contextDestroyed(ServletContextEvent event) {
        // Perform action during application's shutdown
    }
}
```

## Using `@ApplicationScoped` and `@Observes` from CDI

If you have CDI enabled, you can use an [`@ApplicationScoped`][2]-bean and [`@Observes`][3] for hooking your code to application events:

```java
@ApplicationScoped
public class StartupListener {

    public void init(@Observes
                     @Initialized(ApplicationScoped.class) ServletContext context) {
        // Perform action during application's startup
    }

    public void destroy(@Observes
                        @Destroyed(ApplicationScoped.class) ServletContext context) {
        // Perform action during application's shutdown
    }
}
```

Please bear in mind you must use [`@ApplicationScoped`][2] from the `javax.enterprise.context` package and not [`@ApplicationScoped`][4] from the `javax.faces.bean` package.

## Using `@Startup` and `@Singleton` from EJB

If you rely on EJB, then you can use [`@Startup`][5] and [`@Singleton`][6], as follows:

```java
@Startup
@Singleton
public class StartupListener {

    @PostConstruct
    public void init() {
        // Perform action during application's startup
    }

    @PreDestroy
    public void destroy() {
        // Perform action during application's shutdown
    }
}
```

[1]: https://docs.oracle.com/javaee/7/api/javax/servlet/ServletContextListener.html
[2]: http://docs.oracle.com/javaee/7/api/javax/enterprise/context/ApplicationScoped.html
[3]: http://docs.oracle.com/javaee/7/api/javax/enterprise/event/Observes.html
[4]: http://docs.oracle.com/javaee/7/api/javax/faces/bean/ApplicationScoped.html
[5]: http://docs.oracle.com/javaee/7/api/javax/ejb/Startup.html
[6]: http://docs.oracle.com/javaee/7/api/javax/ejb/Singleton.html
