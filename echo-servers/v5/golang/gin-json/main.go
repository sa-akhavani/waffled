package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

type myform struct {
	Field1 string `json:"field1"`
	Field2 string `json:"field2"`
}

func (f myform) String() string {
	return fmt.Sprintf("%s %s", f.Field1, f.Field2)
}

type myresponse struct {
	Success        int    `json:"success"`
	Instancenumber string `json:"instancenumber"`
	Parsedbody     myform `json:"parsedbody"`
}

// const attack_payload_xss = "<script>alert(document.cookie)</script>"
// const attack_payload_union = "0 union select 'password is: ' || password from user limit 1 -- -"
var instance_number = os.Getenv("INSTANCE_NUMBER")
var attack_payload_union = os.Getenv("PAYLOAD_ONE")
var attack_payload_xss = os.Getenv("PAYLOAD_TWO")

func successfull_bypass(parsedBody string) int {
	if attack_payload_union == "" {
		attack_payload_union = "0 union select 'password is: ' || password from user limit 1 -- -"
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
	port_number := os.Getenv("FORMIDABLE_PORT_NUMBER")

	if port_number == "" {
		port_number = "8624"
	}
	if instance_number == "" {
		instance_number = "1"
	}
	router := gin.Default()
	router.GET("/", healthCheck)
	router.POST("/", parseForm)
	router.Run("0.0.0.0:" + port_number)
}

func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, "")
}

func parseForm(c *gin.Context) {
	final_success := 0
	var newForm myform

	if err := c.BindJSON(&newForm); err != nil {
		fmt.Print(err)
		final_success = 0
	}

	final_success = successfull_bypass(newForm.String())

	// fmt.Println(reflect.ValueOf(form))
	// for k, v := range form.Value {
	// 	final_success += successfull_bypass(k)
	// 	final_success += successfull_bypass(strings.Join(v, " "))
	// 	// successfull_bypass(k + v)
	// 	// fmt.Printf("key[%s] value[%s]\n", k, v)
	// }

	var ress = []myresponse{
		{
			Success:        final_success,
			Instancenumber: instance_number,
			Parsedbody:     newForm,
		},
	}
	c.IndentedJSON(http.StatusOK, ress)
}
