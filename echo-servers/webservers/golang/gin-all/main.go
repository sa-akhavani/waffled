package main

import (
	"encoding/xml"
	"fmt"
	"mime/multipart"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

type jsonform struct {
	Field1 string `json:"field1"`
	Field2 string `json:"field2"`
}

func (f jsonform) String() string {
	return fmt.Sprintf("%s %s", f.Field1, f.Field2)
}

type xmlform struct {
	XMLName xml.Name `xml:"schema"`
	Field1  string   `xml:"field1"`
	Field2  string   `xml:"field2"`
}

func (f xmlform) String() string {
	return fmt.Sprintf("%s %s", f.Field1, f.Field2)
}

type multipartresponse struct {
	Success        int             `json:"success"`
	Instancenumber string          `json:"instancenumber"`
	Parsedbody     *multipart.Form `json:"parsedbody"`
}

type jsonresponse struct {
	Success        int      `json:"success"`
	Instancenumber string   `json:"instancenumber"`
	Parsedbody     jsonform `json:"parsedbody"`
}

type xmlresponse struct {
	Success        int     `json:"success"`
	Instancenumber string  `json:"instancenumber"`
	Parsedbody     xmlform `json:"parsedbody"`
}

// const attack_payload_xss = "<script>alert(document.cookie)</script>"
// const attack_payload_union = "0 union select 'password is: ' || password from user limit 1 -- -"
var instance_number = os.Getenv("INSTANCE_NUMBER")
var attack_payload_union = os.Getenv("PAYLOAD_ONE")
var attack_payload_xss = os.Getenv("PAYLOAD_TWO")

func successfull_bypass(parsedBody string) int {
	if attack_payload_union == "" {
		// attack_payload_union = "0 union select 'password is: ' || password from user limit 1 -- -"
		attack_payload_union = "' and 1=1 --"
	}
	if attack_payload_xss == "" {
		attack_payload_xss = "<script>alert(document.cookie)</script>"
	}
	if strings.Contains(parsedBody, attack_payload_union) || strings.Contains(parsedBody, attack_payload_xss) {
		return 1
	} else {
		return 0
	}
}

func main() {
	port_number := os.Getenv("GIN_PORT_NUMBER")
	if port_number == "" {
		port_number = "8635"
	}
	if instance_number == "" {
		instance_number = "1"
	}
	router := gin.Default()
	router.GET("/", healthCheck)
	router.POST("/json", parseJson)
	router.POST("/xml", parseXml)
	router.POST("/multipart", parseMultipart)
	router.Run("0.0.0.0:" + port_number)
}

func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, "")
}

func parseMultipart(c *gin.Context) {
	form, err := c.MultipartForm()
	final_success := 0
	for k, v := range form.Value {
		final_success += successfull_bypass(k)
		final_success += successfull_bypass(strings.Join(v, " "))
	}
	if err != nil {
		fmt.Print(err)
		final_success = 0
	} else {
		// fmt.Print(form)
	}
	var ress = []multipartresponse{
		{
			Success:        final_success,
			Instancenumber: instance_number,
			Parsedbody:     form,
		},
	}
	c.IndentedJSON(http.StatusOK, ress)
}

func parseJson(c *gin.Context) {
	final_success := 0
	var newForm jsonform
	if err := c.BindJSON(&newForm); err != nil {
		fmt.Print(err)
		final_success = 0
	}
	final_success = successfull_bypass(newForm.String())
	var ress = []jsonresponse{
		{
			Success:        final_success,
			Instancenumber: instance_number,
			Parsedbody:     newForm,
		},
	}
	c.IndentedJSON(http.StatusOK, ress)
}

func parseXml(c *gin.Context) {
	final_success := 0
	data, err := c.GetRawData()
	if err != nil {
		fmt.Print(err)
		final_success = 0
	}
	var newForm xmlform
	// Unmarshal the XML data into the Book instance
	err = xml.Unmarshal(data, &newForm)
	if err != nil {
		fmt.Print(err)
		final_success = 0
	}

	// if err := c.BindXML(&newForm); err != nil {
	// 	fmt.Print(err)
	// 	final_success = 0
	// } else {
	// 	fmt.Println(newForm)
	// }
	final_success = successfull_bypass(newForm.String())
	var ress = []xmlresponse{
		{
			Success:        final_success,
			Instancenumber: instance_number,
			Parsedbody:     newForm,
		},
	}
	c.IndentedJSON(http.StatusOK, ress)
}
