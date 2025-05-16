package main

import (
	"context"
	// "encoding/json" // No longer needed if not returning JSON
	"fmt" // For string formatting
	"log/slog"
	"net/http"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

// Response struct might not be needed if you're only serving HTML directly from this handler.
// If you were to use HTML templates, you might pass a struct to the template.
// type Response struct {
// 	Message string `json:"message"`
// 	Version string `json:"version"`
// }

func handler(ctx context.Context, req events.APIGatewayV2HTTPRequest) (events.APIGatewayV2HTTPResponse, error) {
	slog.Info("hello-go HTML invoked", "requestId", req.RequestContext.RequestID)

	// Construct your HTML string
	// You can make this more complex, load from a file, or use Go's html/template package
	pageTitle := "Hello from Lambda!"
	pageBody := "<h1>Welcome!</h1><p>This HTML page is served by a Go Lambda function.</p>"

	htmlBody := fmt.Sprintf(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%s</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        h1 { color: #0056b3; }
    </style>
</head>
<body>
    %s
    <hr>
    <p><em>Request ID: %s</em></p>
</body>
</html>
`, pageTitle, pageBody, req.RequestContext.RequestID)

	return events.APIGatewayV2HTTPResponse{
		StatusCode: http.StatusOK,
		Body:       htmlBody,                                                      // The HTML string directly
		Headers:    map[string]string{"Content-Type": "text/html; charset=utf-8"}, // Set Content-Type to HTML
	}, nil
}

func main() {
	lambda.Start(handler)
}
