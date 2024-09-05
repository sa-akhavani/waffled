<?php

namespace App\Http\Controllers;

use Exception;
use Illuminate\Http\Request;

class BookController extends Controller
{
    private $payload_one;
    private $payload_two;
    public $instance_number;

    public function __construct()
    {
        $this->instance_number = env("INSTANCE_NUMBER", 1);
        // $this->payload_two = env("PAYLOAD_ONE", "0 union select 'password is: ' || password from user limit 1 -- -");
        $this->payload_two = env("PAYLOAD_ONE", "' and 1=1 --");
        $this->payload_one = env("PAYLOAD_TWO", "<script>alert(document.cookie)</script>");
    }

    private function object2array($object) { return @json_decode(@json_encode($object),1); }

    private function successfull_bypass($collection)
    {
        foreach($collection as $field)
        {
            if (str_contains($field, $this->payload_one) || str_contains($field, $this->payload_two)) {
                return 1;
            }
        }
        return 0;
    }

    private function successfull_bypass_string($request_string)
    {
        if (str_contains($request_string, $this->payload_one) || str_contains($request_string, $this->payload_two)) {
            return 1;
        } else {
            return 0;
        }
    }

    public function index()
    {
        return response()->json('{"status": "200"}');
    }

    public function store(Request $request)
    {
        try {
            $request_content = $request->collect();
            $is_successfull_bypass = $this->successfull_bypass($request_content);
            $final_response = [];
            $final_response['parsedbody'] = $request_content;
            $final_response['instancenumber'] = $this->instance_number;
            $final_response['success'] = $is_successfull_bypass;
            return response()->json($final_response);
        } catch (Exception $e) {
            error_log($e);
            $final_response['instancenumber'] = $this->instance_number;
            $final_response['success'] = 0;
            return response()->json($final_response);
        }
    }

    public function storexml(Request $request)
    {
        try {
            $requst_string = $request->getContent();
            // $request_xml = simplexml_load_string($requst_string);
            $request_xml = simplexml_load_string($requst_string, null, 0, 'genre', true);
            $xml_array=$this->object2array($request_xml);
            $request_string = $request_xml->asXML();
            // foreach($xml_array as $field)
            // {
            //     error_log('for');
            //     // error_log(json_encode($field));
            // }
            $is_successfull_bypass = $this->successfull_bypass_string(json_encode($xml_array));
            $final_response = [];
            $final_response['parsedbody'] = $xml_array;
            $final_response['instancenumber'] = $this->instance_number;
            $final_response['success'] = $is_successfull_bypass;
            return response()->json($final_response);
        } catch (Exception $e) {
            error_log($e);
            $final_response['instancenumber'] = $this->instance_number;
            $final_response['success'] = 0;
            return response()->json($final_response);
        }
    }
}
