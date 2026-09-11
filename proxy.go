package main

import (
    "log"
    "net/http"
    "net/http/httputil"
    "net/url"
)

func main() {
    // The target API we are forwarding to
    targetURL := "https://agentrouter.org"
    target, err := url.Parse(targetURL)
    if err != nil {
        log.Fatal("Failed to parse target URL:", err)
    }

    // Create a built-in reverse proxy
    proxy := httputil.NewSingleHostReverseProxy(target)
    
    // Intercept and modify the request before it goes out
    originalDirector := proxy.Director
    proxy.Director = func(req *http.Request) {
        originalDirector(req)

        // Override Host header for proper SSL routing at the destination
        req.Host = target.Host

        // Inject the required Codex headers to bypass the WAF
        req.Header.Set("Originator", "codex_cli_rs")
        req.Header.Set("User-Agent", "codex_cli_rs/0.101.0 (Mac OS 26.0.1; arm64) Apple_Terminal/464")
        req.Header.Set("Version", "0.101.0")
    }

    // Start the server on port 8318
    port := ":8318"
    log.Printf("🚀 Proxy running on http://localhost%s\n", port)
    log.Printf("➡️ Configure your Discord bot Base URL to: http://localhost%s/v1\n", port)
    if err := http.ListenAndServe(port, proxy); err != nil {
        log.Fatal("Server error:", err)
    }
}
