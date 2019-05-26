---
title: Cross field validation with Bean Validation
date: 2017-06-02 10:21:24 Z
tags:
- java
- bean-validation
layout: post
author: Cassio Mazzochi Molin
excerpt: Writing a custom validator to validate multiple fields.
featured_image: null
featured_image_thumbnail: null
---

[Bean Validation][2] provides a quite flexible API for writing your own validators, allowing cross field validation.

See the example below, where the ZIP code is validated according to the country code:

```java
@ValidAddress
public class Address {

    @NotNull
    @Size(max = 50)
    private String street1;

    @Size(max = 50)
    private String street2;

    @NotNull
    @Size(max = 10)
    private String zipCode;

    @NotNull
    @Size(max = 20)
    private String city;

    @Valid
    @NotNull
    private Country country;

    // Getters and setters
}
```

```java
public class Country {

    @NotNull
    @Size(min = 2, max = 2)
    private String iso2;

    // Getters and setters
}
```

```java
@Documented
@Target(TYPE)
@Retention(RUNTIME)
@Constraint(validatedBy = { MultiCountryAddressValidator.class })
public @interface ValidAddress {

    String message() default "{com.example.validation.ValidAddress.message}";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
```

```java
public class MultiCountryAddressValidator 
       implements ConstraintValidator<ValidAddress, Address> {

    public void initialize(ValidateAddress constraintAnnotation) {

    }

    @Override
    public boolean isValid(Address address, 
                           ConstraintValidatorContext constraintValidatorContext) {

        Country country = address.getCountry();
        if (country == null || country.getIso2() == null || address.getZipCode() == null) {
            return true;
        }

        switch (country.getIso2()) {
            case "FR":
                return // Check if address.getZipCode() is valid for France
            case "GR":
                return // Check if address.getZipCode() is valid for Greece
            default:
                return true;
        }
    }
}
```

  [2]: http://beanvalidation.org/