<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PreviewController extends Controller
{
    public function show(Request $request)
    {
        $url = $request->input('url');
        $response = Http::get($url);

        return response($response->body(), 200);
    }
}
