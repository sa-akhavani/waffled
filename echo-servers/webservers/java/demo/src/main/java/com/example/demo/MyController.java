package com.example.demo;

import org.springframework.http.MediaType;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

// import com.fasterxml.jackson.dataformat.xml.XmlMapper;

@RestController
public class MyController {

	@Value("${INSTANCE_NUMBER:1}")
	private int instance_number;
	@Value("${PAYLOAD_ONE:<script>alert(document.cookie)</script>}")
	private String attack_payload_xss;
	// @Value("${PAYLOAD_TWO:0 union select 'password is: ' || password from user limit 1 -- -}")
	@Value("${PAYLOAD_TWO:' and 1=1 --}")
	private String attack_payload_union;

	private int checkSuccessfulBypass(String requestString) {
		if (requestString.contains(this.attack_payload_xss) || requestString.contains(this.attack_payload_union)) {
			return 1;
		} else {
			return 0;
		}
	}

	@GetMapping("/")
	public MyResponse health() {
		return new MyResponse(this.instance_number, 0, "ok");
	}

	// @RequestMapping(value = "/storejson", method = POST, consumes = MediaType.APPLICATION_JSON_VALUE)
	@PostMapping(value = "/json", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	// public MyResponse storeAll(@RequestBody JsonRequest req) {
	public MyResponse storeJson(@RequestBody String reqString) {		
		System.err.println(reqString);
		int success = this.checkSuccessfulBypass(reqString);
		return new MyResponse(this.instance_number, success, reqString);
	}

	// https://www.baeldung.com/sprint-boot-multipart-requests
	@PostMapping(value = "/multipart", consumes = MediaType.MULTIPART_FORM_DATA_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	// public MyResponse storeMultipart(@RequestPart Part field1) {
	public MyResponse storeMultipart(@RequestParam(value = "field1", required=false) String field1, @RequestParam(value = "field2", required=false) String field2) {
		String outcome = field1 + " , " + field2;
		int success = this.checkSuccessfulBypass(outcome);
		return new MyResponse(this.instance_number, success, outcome);
	}

	@PostMapping(value = "/xml", consumes = MediaType.APPLICATION_XML_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	public MyResponse storexml(@RequestBody Book book) {
		try {
			String outcome = book.toString();
			// System.err.println(outcome);
			int success = checkSuccessfulBypass(outcome);
			return new MyResponse(this.instance_number, success, outcome);
		} catch (Exception e) {
			return new MyResponse(this.instance_number, 0, e.getMessage());
		}		
	}

	// @PostMapping(value = "/storexml2", consumes = MediaType.APPLICATION_XML_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	// @ResponseBody
	// public MyResponse storexml(@RequestBody String reqString) {
	// 	try {
	// 		XmlMapper xmlMapper = new XmlMapper();
	// 		Book myObject = xmlMapper.readValue(reqString, Book.class);		
	// 		System.err.println(myObject);
	// 	} catch (Exception e) {
	// 		System.err.println(e);
	// 	}			
	// 	return new MyResponse(this.instance_number, 0, "ok");
	// }	
}
