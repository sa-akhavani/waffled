package com.example.demo;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

// import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlRootElement;

// @JacksonXmlRootElement(localName = "BOOK", namespace = "genre")
@XmlRootElement(name = "BOOK", namespace = "genre")
public class Book {
    private MyField schema;
    private String field2;

    @XmlElement(namespace = "genre")
    public MyField getSchema() {
        return this.schema;
    }
    public void setSchema(MyField schema) {
        this.schema = schema;
    }

    public String getField2() {
        return this.field2;
    }
    public void setField2(String field2) {
        this.field2 = field2;
    }

    public String toString() {
        return this.schema.toString() + this.field2;
    }
}
