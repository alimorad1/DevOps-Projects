package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class AppTest {
    @Test
    public void testSayHello() {
        // استفاده از متد استاتیک
        assertEquals("Hello, DevOps!... this is a test form Moradi-maven-test", App.sayHello());
    }
}

