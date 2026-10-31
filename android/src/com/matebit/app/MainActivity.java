package com.matebit.app;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;

/**
 * Envoltorio mínimo: un WebView que sirve el juego guardado en assets/
 * bajo un origen https falso (appassets.local), para que localStorage y fetch
 * se comporten como en una web normal. El resto de hosts (Lichess) va por la red.
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.local";
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        web = new WebView(this);
        web.setBackgroundColor(0xFF000000);
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        s.setMediaPlaybackRequiresUserGesture(false);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return serve(request.getUrl());
            }

            @Override
            @SuppressWarnings("deprecation")
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                // Dentro de la app solo se navega por lo propio.
                return !HOST.equals(Uri.parse(url).getHost());
            }
        });

        web.loadUrl("https://" + HOST + "/index.html");
    }

    private WebResourceResponse serve(Uri uri) {
        if (!HOST.equals(uri.getHost())) {
            return null; // otras peticiones (API de Lichess) siguen su curso normal
        }
        String path = uri.getPath();
        if (path == null || path.equals("/") || path.equals("/index.html")) {
            try {
                InputStream in = getAssets().open("index.html");
                return new WebResourceResponse("text/html", "UTF-8", in);
            } catch (IOException e) {
                // cae al 404
            }
        }
        return new WebResourceResponse("text/plain", "UTF-8", 404, "Not Found",
                new HashMap<String, String>(), new ByteArrayInputStream(new byte[0]));
    }

    @Override
    protected void onPause() {
        super.onPause();
        web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
    }

    @Override
    protected void onDestroy() {
        if (web != null) {
            web.destroy();
        }
        super.onDestroy();
    }
}
