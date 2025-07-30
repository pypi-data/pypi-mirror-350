from django.http import JsonResponse

class HTTP_Response_Status_Codes:

    #! DOCUMENTATION: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status#client_error_responses

    Version = "V0"
    Author = "https://github.com/zisia13"
    
    class Information:

        @staticmethod
        def Continue() -> JsonResponse:

            """
            This interim response indicates that the client should continue the request or ignore the response if the request is already finished.
            """

            return JsonResponse({"status" : True, "message" : "Continue"}, status = 100)
        
        @staticmethod
        def Switch_Protocols() -> JsonResponse:

            """
            This code is sent in response to an Upgrade request header from the client and indicates the protocol the server is switching to.
            """

            return JsonResponse({"status" : True, "message" : "Upgrade Header"}, status = 101)
        
        @staticmethod
        def Processing() -> JsonResponse:

            """
            This code was used in WebDAV contexts to indicate that a request has been received by the server, but no status was available at the time of the response.
            """

            return JsonResponse({"status" : True, "message" : "Processing"}, status = 102)
        
        @staticmethod
        def Early_Hint() -> JsonResponse:

            """
            This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response or preconnect to an origin from which the page will need resources.
            """

            return JsonResponse({"status" : True, "message" : "Early Hint"}, status = 103)
            
    class Success:

        @staticmethod
        def Ok() -> JsonResponse:

            """
            GET: The resource has been fetched and transmitted in the message body.
            HEAD: Representation headers are included in the response without any message body.
            PUT or POST: The resource describing the result of the action is transmitted in the message body.
            TRACE: The message body contains the request as received by the server.
            """

            return JsonResponse({"status" : True, "message" : "Success"}, status = 200)
        
        @staticmethod
        def Created() -> JsonResponse:

            """
            The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.
            """

            return JsonResponse({"status" : True, "message" : "Created"}, status = 201)
        
        @staticmethod
        def Accepted() -> JsonResponse:

            """
            The request has been received but not yet acted upon. It is noncommittal, since there is no way in HTTP to later send an asynchronous response indicating the outcome of the request. 
            It is intended for cases where another process or server handles the request, or for batch processing.
            """

            return JsonResponse({"status" : True, "message" : "Accepted"}, status = 202)

        @staticmethod
        def Non_Authoritative_Information() -> JsonResponse:

            """
            This response code means the returned metadata is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy. 
            This is mostly used for mirrors or backups of another resource. 
            Except for that specific case, the 200 OK response is preferred to this status.
            """
            
            return JsonResponse({"status" : True, "message" : "Non Authoritative Information"}, status = 203)
        
        @staticmethod
        def No_Content() -> JsonResponse:

            """
            There is no content to send for this request, but the headers are useful. 
            The user agent may update its cached headers for this resource with the new ones.
            """
            
            return JsonResponse({"status" : True, "message" : "No Content"}, status = 204)
        
        @staticmethod
        def Reset_Content() -> JsonResponse:

            """
            Tells the user agent to reset the document which sent this request.
            """
            
            return JsonResponse({"status" : True, "message" : "Reset Content"}, status = 205)

        @staticmethod
        def Partial_Content() -> JsonResponse:

            """
            This response code is used in response to a range request when the client has requested a part or parts of a resource.
            """
            
            return JsonResponse({"status" : True, "message" : "Partial Content"}, status = 206)
        
        @staticmethod
        def Multi_Status() -> JsonResponse:

            """
            Conveys information about multiple resources, for situations where multiple status codes might be appropriate.
            """
            
            return JsonResponse({"status" : True, "message" : "Multi Status"}, status = 207)
        
        @staticmethod
        def Already_Reported() -> JsonResponse:

            """
            Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection.
            """
            
            return JsonResponse({"status" : True, "message" : "Already Reported"}, status = 208)
        
        @staticmethod
        def Im_Used() -> JsonResponse:

            """
            The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.
            """
            
            return JsonResponse({"status" : True, "message" : "Im Used"}, status = 226)

    class Redirect:

        @staticmethod
        def Multiple_Choices() -> JsonResponse:

            """
            In agent-driven content negotiation, the request has more than one possible response and the user agent or user should choose one of them. 
            There is no standardized way for clients to automatically choose one of the responses, so this is rarely used.
            """
            
            return JsonResponse({"status" : True, "message" : "Multiple Choices"}, status = 300)
        
        @staticmethod
        def Moved_Permanently() -> JsonResponse:

            """
            The URL of the requested resource has been changed permanently. The new URL is given in the response.
            """
            
            return JsonResponse({"status" : True, "message" : "Moved Permanently"}, status = 301)
        
        @staticmethod
        def Found() -> JsonResponse:

            """
            This response code means that the URI of requested resource has been changed temporarily. 
            Further changes in the URI might be made in the future, so the same URI should be used by the client in future requests.
            """
            
            return JsonResponse({"status" : True, "message" : "Found"}, status = 302)
        
        @staticmethod
        def See_Other() -> JsonResponse:

            """
            The server sent this response to direct the client to get the requested resource at another URI with a GET request.
            """
            
            return JsonResponse({"status" : True, "message" : "See Other"}, status = 303)
        
        @staticmethod
        def Not_Modified() -> JsonResponse:

            """
            This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.
            """
            
            return JsonResponse({"status" : True, "message" : "Not Modified"}, status = 304)
        
        @staticmethod
        def Use_Proxy() -> JsonResponse:

            """
            Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy.
            It has been deprecated due to security concerns regarding in-band configuration of a proxy.
            """
            
            return JsonResponse({"status" : True, "message" : "Use Proxy"}, status = 305)
        
        @staticmethod
        def Unused() -> JsonResponse:

            """
            This response code is no longer used; but is reserved. It was used in a previous version of the HTTP/1.1 specification.
            """
            
            return JsonResponse({"status" : True, "message" : "Unused"}, status = 306)
        
        @staticmethod
        def Temporary_Redirected() -> JsonResponse:

            """
            The server sends this response to direct the client to get the requested resource at another URI with the same method that was used in the prior request. 
            This has the same semantics as the 302 Found response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the redirected request.
            """
            
            return JsonResponse({"status" : True, "message" : "Temporary Redirected"}, status = 307)
        
        @staticmethod
        def Permanent_Redirected() -> JsonResponse:

            """
            This means that the resource is now permanently located at another URI, specified by the Location response header. 
            This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request.
            """
            
            return JsonResponse({"status" : True, "message" : "Permanent Redirected"}, status = 308)

    class Client_Error:

        @staticmethod
        def Bad_Request() -> JsonResponse:

            """
            The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).
            """

            return JsonResponse({"status": False, "message": "Bad Request"}, status = 400)
        
        @staticmethod
        def Unauthorized() -> JsonResponse:

            """
            Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated". 
            That is, the client must authenticate itself to get the requested response.
            """

            return JsonResponse({"status": False, "message": "Unauthorized"}, status = 401)
        
        @staticmethod
        def Payment_Required() -> JsonResponse:

            """
            The initial purpose of this code was for digital payment systems, however this status code is rarely used and no standard convention exists.
            """

            return JsonResponse({"status": False, "message": "Payment_Required"}, status = 402)
        
        @staticmethod
        def Forbidden() -> JsonResponse:

            """
            The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. 
            Unlike 401 Unauthorized, the client's identity is known to the server.
            """

            return JsonResponse({"status": False, "message": "Forbidden"}, status = 403)
        
        @staticmethod
        def Not_Found() -> JsonResponse:

            """
            The server cannot find the requested resource. In the browser, this means the URL is not recognized. 
            In an API, this can also mean that the endpoint is valid but the resource itself does not exist. 
            Servers may also send this response instead of 403 Forbidden to hide the existence of a resource from an unauthorized client. 
            This response code is probably the most well known due to its frequent occurrence on the web.
            """

            return JsonResponse({"status": False, "message": "Not Found"}, status = 404)
        
        @staticmethod
        def Method_Not_Allowed() -> JsonResponse:

            """
            The request method is known by the server but is not supported by the target resource. 
            For example, an API may not allow DELETE on a resource, or the TRACE method entirely.
            """

            return JsonResponse({"status": False, "message": "Method Not Allowed"}, status = 405)
        
        @staticmethod
        def Not_Acceptable() -> JsonResponse:

            """
            This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent.
            """

            return JsonResponse({"status": False, "message": "Not Acceptable"}, status = 406)
        
        @staticmethod
        def Proxy_Authentivation_Required() -> JsonResponse:

            """
            This is similar to 401 Unauthorized but authentication is needed to be done by a proxy.
            """

            return JsonResponse({"status": False, "message": "Proxy Authentivation Required"}, status = 407)
        
        @staticmethod
        def Request_Timeout() -> JsonResponse:

            """
            This response is sent on an idle connection by some servers, even without any previous request by the client. 
            It means that the server would like to shut down this unused connection. 
            This response is used much more since some browsers use HTTP pre-connection mechanisms to speed up browsing. 
            Some servers may shut down a connection without sending this message.
            """

            return JsonResponse({"status": False, "message": "Request Timeout"}, status = 408)
        
        @staticmethod
        def Conflict() -> JsonResponse:

            """
            This response is sent when a request conflicts with the current state of the server. 
            In WebDAV remote web authoring, 409 responses are errors sent to the client so that a user might be able to resolve a conflict and resubmit the request.
            """

            return JsonResponse({"status": False, "message": "Conflict"}, status = 409)
        
        @staticmethod
        def Gone() -> JsonResponse:

            """
            This response is sent when the requested content has been permanently deleted from server, with no forwarding address. 
            Clients are expected to remove their caches and links to the resource. 
            The HTTP specification intends this status code to be used for "limited-time, promotional services". 
            APIs should not feel compelled to indicate resources that have been deleted with this status code.
            """

            return JsonResponse({"status": False, "message": "Gone"}, status = 410)
        
        @staticmethod
        def Length_Requred() -> JsonResponse:

            """
            Server rejected the request because the Content-Length header field is not defined and the server requires it.
            """

            return JsonResponse({"status": False, "message": "Length Requred"}, status = 411)

        @staticmethod
        def Precondition_Failed() -> JsonResponse:

            """
            In conditional requests, the client has indicated preconditions in its headers which the server does not meet. 
            """

            return JsonResponse({"status": False, "message": "Precondition Failed"}, status = 412)
        
        @staticmethod
        def Content_Too_Large() -> JsonResponse:

            """
            The request body is larger than limits defined by server. The server might close the connection or return an Retry-After header field.
            """

            return JsonResponse({"status": False, "message": "Content too large"}, status = 413)
        
        @staticmethod
        def URI_Too_Long() -> JsonResponse:

            """
            The URI requested by the client is longer than the server is willing to interpret.
            """

            return JsonResponse({"status": False, "message": "URI too long"}, status = 414)
        
        @staticmethod
        def Unsupported_Media_Type() -> JsonResponse:

            """
            The media format of the requested data is not supported by the server, so the server is rejecting the request.
            """

            return JsonResponse({"status": False, "message": "Unsupported Media Type"}, status = 415)
        
        @staticmethod
        def Range_Not_Satisfiable() -> JsonResponse:

            """
            The ranges specified by the Range header field in the request cannot be fulfilled. 
            It's possible that the range is outside the size of the target resource's data.
            """

            return JsonResponse({"status": False, "message": "Range Not Satisfiable"}, status = 416)
        
        @staticmethod
        def Expectation_Failed() -> JsonResponse:

            """
            This response code means the expectation indicated by the Expect request header field cannot be met by the server.
            """

            return JsonResponse({"status": False, "message": "Expectation Failed"}, status = 417)
        
        @staticmethod
        def Im_a_teapot() -> JsonResponse:

            """
            The server refuses the attempt to brew coffee with a teapot.
            """

            return JsonResponse({"status": False, "message": "Im a teapod"}, status = 418)
        
        @staticmethod
        def Misdirected_Request() -> JsonResponse:

            """
            The request was directed at a server that is not able to produce a response. 
            This can be sent by a server that is not configured to produce responses for the combination of scheme and authority that are included in the request URI.
            """

            return JsonResponse({"status": False, "message": "Misdirected Request"}, status = 421)
        
        @staticmethod
        def Unprocessable_Content() -> JsonResponse:

            """
            The request was well-formed but was unable to be followed due to semantic errors.
            """

            return JsonResponse({"status": False, "message": "Unprocessable Content"}, status = 422)
        
        @staticmethod
        def Locked() -> JsonResponse:

            """
            The resource that is being accessed is locked.
            """

            return JsonResponse({"status": False, "message": "Locked"}, status = 423)
        
        @staticmethod
        def Failed_Dependency() -> JsonResponse:

            """
            The request failed due to failure of a previous request.
            """

            return JsonResponse({"status": False, "message": "Failed Dependency"}, status = 424)

        @staticmethod
        def Too_Early() -> JsonResponse:

            """
            Indicates that the server is unwilling to risk processing a request that might be replayed.
            """

            return JsonResponse({"status": False, "message": "Too Early"}, status = 425)
        
        @staticmethod
        def Upgrade_Required() -> JsonResponse:

            """
            The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol. 
            The server sends an Upgrade header in a 426 response to indicate the required protocol(s).
            """

            return JsonResponse({"status": False, "message": "Upgrade Required"}, status = 426)
        
        @staticmethod
        def Precondition_Required() -> JsonResponse:

            """
            The origin server requires the request to be conditional. 
            This response is intended to prevent the 'lost update' problem, where a client GETs a resource's state, modifies it and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict.
            """

            return JsonResponse({"status": False, "message": "Precondition Required"}, status = 428)
        
        @staticmethod
        def Too_Many_Requests() -> JsonResponse:

            """
            The user has sent too many requests in a given amount of time (rate limiting).
            """

            return JsonResponse({"status": False, "message": "too many requests"}, status = 429)
        
        @staticmethod
        def Request_Header_Fields_Too_Large() -> JsonResponse:

            """
            The server is unwilling to process the request because its header fields are too large. 
            The request may be resubmitted after reducing the size of the request header fields.
            """

            return JsonResponse({"status": False, "message": "Request Header Fields Too Large"}, status = 431)
        
        @staticmethod
        def Unavailable_For_Legal_Reasons() -> JsonResponse:

            """
            The user agent requested a resource that cannot legally be provided, such as a web page censored by a government.
            """

            return JsonResponse({"status": False, "message": "Unavailable For Legal Reasons"}, status = 451)

    class Server_Error:

        @staticmethod
        def Internal_Server_Error() -> JsonResponse:

            """
            The server has encountered a situation it does not know how to handle. 
            This error is generic, indicating that the server cannot find a more appropriate 5XX status code to respond with.
            """

            return JsonResponse({"status": False, "message": "Internal Server Error"}, status = 500)
        
        @staticmethod
        def Not_Implemented() -> JsonResponse:

            """
            The request method is not supported by the server and cannot be handled. 
            The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD.
            """

            return JsonResponse({"status": False, "message": "Not Implemented"}, status = 501)
        
        @staticmethod
        def Bad_Gateway() -> JsonResponse:

            """
            This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response.
            """

            return JsonResponse({"status": False, "message": "Bad Gateway"}, status = 502)
        
        @staticmethod
        def Service_Unavailable() -> JsonResponse:

            """
            The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. 
            Note that together with this response, a user-friendly page explaining the problem should be sent. 
            This response should be used for temporary conditions and the Retry-After HTTP header should, if possible, contain the estimated time before the recovery of the service. 
            The webmaster must also take care about the caching-related headers that are sent along with this response, as these temporary condition responses should usually not be cached.
            """

            return JsonResponse({"status": False, "message": "Service Unavailable"}, status = 503)
        
        @staticmethod
        def Gateway_Timeout() -> JsonResponse:

            """
            This error response is given when the server is acting as a gateway and cannot get a response in time.
            """

            return JsonResponse({"status": False, "message": "Gateway Timeout"}, status = 504)
        
        @staticmethod
        def HTTP_Version_Not_Supported() -> JsonResponse:

            """
            The HTTP version used in the request is not supported by the server.
            """

            return JsonResponse({"status": False, "message": "HTTP Version Not Supported"}, status = 505)
        
        @staticmethod
        def Variant_Also_Negotiates() -> JsonResponse:

            """
            The server has an internal configuration error: during content negotiation, the chosen variant is configured to engage in content negotiation itself, which results in circular references when creating responses.
            """

            return JsonResponse({"status": False, "message": "Variant Also Negotiates"}, status = 506)

        @staticmethod
        def Insufficient_Storage() -> JsonResponse:

            """
            The method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request.
            """

            return JsonResponse({"status": False, "message": "Insufficient Storage"}, status = 507)

        @staticmethod
        def Loop_Detected() -> JsonResponse:

            """
            The server detected an infinite loop while processing the request.
            """

            return JsonResponse({"status": False, "message": "Loop Detected"}, status = 508)
        
        @staticmethod
        def Not_Extended() -> JsonResponse:

            """
            The client request declares an HTTP Extension (RFC 2774) that should be used to process the request, but the extension is not supported.
            """

            return JsonResponse({"status": False, "message": "Not Extended"}, status = 510)
        
        @staticmethod
        def Network_Authentication_Required() -> JsonResponse:

            """
            Indicates that the client needs to authenticate to gain network access.
            """

            return JsonResponse({"status": False, "message": "Network Authentication Required"}, status = 511)

    class Other: #! custom errors

        @staticmethod
        def Json_Error() -> JsonResponse:

            """
            Error with Json Formate.
            """

            return JsonResponse({"status": False, "error": "Error with Json"}, status = 422)
