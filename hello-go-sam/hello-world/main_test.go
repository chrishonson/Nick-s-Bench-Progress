package main

import (
	"context"
	"strings"
	"testing"

	"github.com/aws/aws-lambda-go/events"
)

func TestHandler(t *testing.T) {
	t.Run("Successful Request", func(t *testing.T) {
		// Create a test request
		req := events.APIGatewayV2HTTPRequest{
			RequestContext: events.APIGatewayV2HTTPRequestContext{
				RequestID: "test-request-id",
			},
		}

		// Call the handler
		resp, err := handler(context.Background(), req)
		if err != nil {
			t.Fatal("Handler should not return an error")
		}

		// Verify response
		if resp.StatusCode != 200 {
			t.Errorf("Expected status code 200, got %d", resp.StatusCode)
		}

		// Check content type
		if resp.Headers["Content-Type"] != "text/html; charset=utf-8" {
			t.Errorf("Expected Content-Type text/html; charset=utf-8, got %s", resp.Headers["Content-Type"])
		}

		// Verify HTML content
		body := resp.Body
		if !strings.Contains(body, "<!DOCTYPE html>") {
			t.Error("Response should contain HTML doctype")
		}
		if !strings.Contains(body, "Hello from Lambda!") {
			t.Error("Response should contain the page title")
		}
		if !strings.Contains(body, "test-request-id") {
			t.Error("Response should contain the request ID")
		}
	})

	t.Run("Empty Request Context", func(t *testing.T) {
		// Test with empty request context
		req := events.APIGatewayV2HTTPRequest{}

		resp, err := handler(context.Background(), req)
		if err != nil {
			t.Fatal("Handler should not return an error with empty context")
		}

		if resp.StatusCode != 200 {
			t.Errorf("Expected status code 200, got %d", resp.StatusCode)
		}

		// Verify HTML content still works
		if !strings.Contains(resp.Body, "<!DOCTYPE html>") {
			t.Error("Response should contain HTML doctype even with empty context")
		}
	})
}
