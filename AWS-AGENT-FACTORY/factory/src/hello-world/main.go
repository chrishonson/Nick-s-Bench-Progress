
package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-lambda-go/lambda"
)

// HandleRequest is the main handler for the Lambda function.
func HandleRequest(ctx context.Context) (string, error) {
	return "Hello from the Action Group!", nil
}

func main() {
	lambda.Start(HandleRequest)
}
