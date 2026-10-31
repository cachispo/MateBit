import SwiftUI
import WebKit

/// Muestra el juego (index.html, guardado dentro de la app) en un WKWebView.
///
/// El HTML se carga con una URL base https ficticia para que `localStorage` y `fetch`
/// se comporten como en una web normal (récord, reserva de puzles, llamadas a Lichess).
struct GameView: UIViewRepresentable {
    private static let baseURL = URL(string: "https://appassets.local/")!

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        let web = WKWebView(frame: .zero, configuration: config)
        web.navigationDelegate = context.coordinator
        web.isOpaque = false
        web.backgroundColor = .black
        web.scrollView.backgroundColor = .black
        web.scrollView.bounces = false
        // Con .never, el CSS recibe los márgenes seguros (muesca, isla dinámica) vía env(safe-area-inset-*).
        web.scrollView.contentInsetAdjustmentBehavior = .never

        if let url = Bundle.main.url(forResource: "index", withExtension: "html"),
           let html = try? String(contentsOf: url, encoding: .utf8) {
            web.loadHTMLString(html, baseURL: GameView.baseURL)
        }
        return web
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    func makeCoordinator() -> Coordinator { Coordinator() }

    final class Coordinator: NSObject, WKNavigationDelegate {
        /// Dentro de la app solo se navega por lo propio; cualquier enlace externo se bloquea.
        func webView(_ webView: WKWebView,
                     decidePolicyFor navigationAction: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            if navigationAction.navigationType == .other
                || navigationAction.request.url?.host == "appassets.local" {
                decisionHandler(.allow)
            } else {
                decisionHandler(.cancel)
            }
        }
    }
}
