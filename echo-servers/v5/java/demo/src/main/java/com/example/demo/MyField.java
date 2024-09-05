package com.example.demo;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name = "field1")
public class MyField {
    private String field1;

    public String getField1() {
        return field1;
    }

    public void setField1(String field1) {
        this.field1 = field1;
    }

    @Override
    public String toString() {
        return this.field1;
    }
}
