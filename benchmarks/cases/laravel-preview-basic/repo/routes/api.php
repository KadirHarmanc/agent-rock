<?php

use App\Http\Controllers\AdminUserController;
use App\Http\Controllers\PreviewController;
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::post('/users', [AdminUserController::class, 'store'])
    ->middleware(['auth:sanctum', 'can:create-users']);

Route::post('/preview', [PreviewController::class, 'show'])
    ->middleware('auth:sanctum');

Route::get('/me', [ProfileController::class, 'show'])
    ->middleware('auth:sanctum');
